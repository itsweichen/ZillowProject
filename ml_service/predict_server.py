import pyjsonrpc

from ml_common import *

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

MODEL_DIR = './model'
MODEL_UPDATE_LAG = 5

linear_regressor = tf.contrib.learn.LinearRegressor(
    feature_columns=feature_columns,
    model_dir=MODEL_DIR)

print "Model loaded"

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def predict(self, zipcode, property_type, bedroom, bathroom, size):
        sample = pandas.DataFrame({
            'zipcode': zipcode,
            'property_type': property_type,
            'bedroom': bedroom,
            'bathroom': bathroom,
            'size': size,
            'list_price': 0}, index=[0])

        def input_fn_predict():
            return input_fn(sample)

        prediction = linear_regressor.predict(input_fn=input_fn_predict)
        print prediction
        return prediction[0].item()

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting predicting server ..."
print "URL: http://" + str(SERVER_HOST) + ":" + str(SERVER_PORT)

http_server.serve_forever()
