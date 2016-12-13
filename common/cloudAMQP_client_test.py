from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://kdflangt:w3wO5ExwRgGqixP6q-4Y9HDy2aGXETCG@hyena.rmq.cloudamqp.com/kdflangt'
QUEUE_NAME = 'dataFetcherTaskQueue'

# init a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# send a message
client.sendDataFetcherTask({'zpid': '83154148'})

# receive a message
# client.getDataFetcherTask()
