import pyjsonrpc

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add gets called with %d and %d" % (a, b)
        return a + b

    @pyjsonrpc.rpcmethod
    def searchArea(self, query):
        if query.isdigit():
            # TODO: search in db for zipcode
            pass
        else:
            query_split = query.split(',')
            city = query_split[0].strip()
            state = query_split[1].strip()
            # TODO: search in db
        return ["House_1", "Condo_2"]


http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server..."
print "Listening on %s:%d", (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
