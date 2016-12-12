var jayson = require('jayson');

// create a client connected to backend server
var client = jayson.client.http({
  hostname: 'localhost',
  port: 4040
});

// test RPC method add()
function add(a, b, callback) {
  client.request('add', [a, b], function(err, error, response) {
    // err: call error; error: RPC function running error; reponse: result
    if (err) throw err;
    console.log(response);
    callback(response);
  });
}

// search area
function searchArea(query, callback) {
  client.request('searchArea', [query], function(err, error, response) {
    if (err) throw err;
    console.log(response);
    callback(response);
  });
}



module.exports = {
  add: add,
  searchArea: searchArea
};
