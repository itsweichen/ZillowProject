var redis = require("redis");
var client = redis.createClient();

AUTOCOMPLETE_KEY = 'autocomplete'
AUTOCOMPLETE_LIMIT = '6'

// test method
function test(callback) {
  console.log("redis_client: test() gets called. Should print 'bar'");
  client.set('foo', "bar");
  client.get('foo', function(err, response) {
    if (err) throw err;
    callback(response);
  });
}

function getAutocomplete(query, callback) {
  console.log("redis_client: getAutocomplete() gets called with query=" + query);
  client.zrangebylex(AUTOCOMPLETE_KEY, '[' + query, '[' + query + '\xff',
    "LIMIT", "0", AUTOCOMPLETE_LIMIT, function(err, response){
      if (err) throw err;
      callback(response);
    });
}

module.exports = {
  test: test,
  getAutocomplete: getAutocomplete
};
