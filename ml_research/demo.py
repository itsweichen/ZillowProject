import math
import numpy as np
import pandas
import sys
import tensorflow as tf

# Training Parameter
LEARNING_RATE = 200

STEPS = 10000
TEST_STEPS = 10

CSV_FILE_PATH = '''./1218_sample.csv'''
CSV_FILE_FORMAT = {
    'zipcode': str,
    'longitude': np.float32,
    'latitude': np.float32,
    'is_for_sale': bool,
    'property_type': str,
    'bedroom': np.float32,
    'bathroom': np.float32,
    'size': np.float32,
    'list_price': np.float32,
    'last_update': np.float32
}

# Feature, Label, Column
COLUMNS = ['zipcode', 'longitude', 'latitude', 'is_for_sale', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price']
CATEGORICAL_COLUMNS = ['zipcode', 'property_type']
CONTINUOUS_COLUMNS = ['bedroom', 'bathroom', 'size']
LABEL_COLUMN = 'list_price'
FEATURE_COLUMNS = ['zipcode', 'property_type', 'bedroom', 'bathroom', 'size', 'list_price']

# input_fn return format: (feature_columns, label)
# feature_columns: {column_name : tf.constant}
# label: tf.constant
def input_fn(df):
	continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
	categorical_cols = {k: tf.SparseTensor(
		indices=[[i, 0] for i in range(df[k].size)],
		values=df[k].values,
		shape=[df[k].size, 1])
			for k in CATEGORICAL_COLUMNS}
	feature_columns = dict(continuous_cols.items() + categorical_cols.items())
	label = tf.constant(df[LABEL_COLUMN].values)
	return feature_columns, label


# Load in the data from CSV files.
property_dataframe = pandas.read_csv(CSV_FILE_PATH, dtype=CSV_FILE_FORMAT)

# Randomize the index.
property_dataframe = property_dataframe.reindex(
    np.random.permutation(property_dataframe.index))

print "Data set loaded and randomized.\n"

# Pick out the columns we care about.
property_dataframe = property_dataframe[COLUMNS]

# Clean up data
property_dataframe = property_dataframe[property_dataframe['is_for_sale'] == True]
property_dataframe = property_dataframe[property_dataframe['list_price'] != 0]
# Drop rows with any value NaN
property_dataframe = property_dataframe.dropna()

# Split the data into test and train
train_dataframe = property_dataframe.sample(frac=0.9)
test_dataframe = property_dataframe.drop(train_dataframe.index)

train_features_label = train_dataframe[FEATURE_COLUMNS]
test_features_label = test_dataframe[FEATURE_COLUMNS]

# Prepare features
zipcode = tf.contrib.layers.sparse_column_with_hash_bucket("zipcode", hash_bucket_size=1000)
property_type = tf.contrib.layers.sparse_column_with_hash_bucket("property_type", hash_bucket_size=100)
bedroom = tf.contrib.layers.real_valued_column("bedroom")
bathroom = tf.contrib.layers.real_valued_column("bathroom")
size = tf.contrib.layers.real_valued_column("size")
size_buckets = tf.contrib.layers.bucketized_column(size, boundaries=np.arange(6000, step=200).tolist())

feature_columns = [zipcode, property_type, bedroom, bathroom, size_buckets]

targets = property_dataframe['list_price']

linear_regressor = tf.contrib.learn.LinearRegressor(
    feature_columns=feature_columns,
    optimizer=tf.train.AdamOptimizer(learning_rate=LEARNING_RATE))

print "Training model..."

def input_fn_train():
    return input_fn(train_features_label)

linear_regressor.fit(input_fn=input_fn_train, steps=STEPS)

print "Model training finished."

print "Evaluating"
def input_fn_test():
    return input_fn(test_features_label)

results = linear_regressor.evaluate(input_fn=input_fn_test, steps=TEST_STEPS)
for key in sorted(results):
    print "%s: %s" % (key, results[key])
print "Evaluation done!"

print "LEARNING_RATE", LEARNING_RATE
print "STEPS", STEPS
