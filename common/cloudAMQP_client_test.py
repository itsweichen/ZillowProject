from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://kdflangt:w3wO5ExwRgGqixP6q-4Y9HDy2aGXETCG@hyena.rmq.cloudamqp.com/kdflangt'
QUEUE_NAME = 'test_queue'

# init a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# send a message
# client.sendDataFetcherTask({'name': 'test message'})

# receive a message
client.getDataFetcherTask()
