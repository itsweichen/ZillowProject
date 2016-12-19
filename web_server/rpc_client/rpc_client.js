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
    console.log("got response from searchArea");
    callback(response);
  });
}

// get property details
function getDetailsByZpid(id, callback) {
  client.request('getDetailsByZpid', [id, true], function(err, error, response) {
    if (err) throw err;
    console.log("got response from getDetailsByZpid");
    callback(response);
  });
}


// get watch list
function getWatchList(email, callback) {
  client.request('getWatchList', [email], function(err, error, response) {
    if (err) throw err;
    console.log("got response from getWatchList");
    callback(response);
  });
}

// update user watchlist
function updateWatchList(email, callback) {
  client.request('updateWatchList', [email], function(err, error, response) {
    if (err) throw err;
    console.log("got response from updateWatchlist");
    callback(response);
  })
}

module.exports = {
  add: add,
  searchArea: searchArea,
  getDetailsByZpid: getDetailsByZpid,
  getWatchList: getWatchList,
  updateWatchList: updateWatchList
};
