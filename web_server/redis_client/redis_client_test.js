var client = require('./redis_client');

client.test(function(response) {
  console.log("client respoonse: " + response);
});

client.getAutocomplete("s", function(response) {
  console.log(response);
});
