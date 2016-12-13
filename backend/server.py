import operations

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test method"""
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add gets called with %d and %d" % (a, b)
        return a + b

    """Search properties"""
    @pyjsonrpc.rpcmethod
    def searchArea(self, text):
        print "search() gets called with text=[%s]" % text
        return operations.searchArea(text)

    """
    The following methods provide more way to fetch data.
    """

    """Search properties by zip code"""
    @pyjsonrpc.rpcmethod
    def searchAreaByZip(self, zipcode):
        print "searchAreaByZip() gets called with zipcode=[%s]" % str(zipcode)
        return operations.searchAreaByZip(zipcode)

    """Search properties by city and state"""
    @pyjsonrpc.rpcmethod
    def searchAreaByCityState(self, city, state):
        print "searchAreaByCityState() gets called with city=[%s] and state=[%s]" % (city, state)
        return operations.searchAreaByCityState(city, state)

    """Search a property with specific address and citystatezip"""
    @pyjsonrpc.rpcmethod
    def searchByAddress(self, address, citystatezip):
        print "searchByAddress() gets called with address=[%s] and citystatezip=[%s]" % (address, citystatezip)
        return operations.searchByAddress(address, citystatezip)

    """Retrieve details by zillow property ID (zpid)"""
    @pyjsonrpc.rpcmethod
    def getDetailsByZpid(self, zpid):
        print "getDetailsByZillowId() gets called with zpid=[%s]" % (zpid)
        return operations.getDetailsByZpid(zpid)

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server..."
print "Listening on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
