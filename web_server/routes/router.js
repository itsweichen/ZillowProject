var express = require('express');
var passwordHash = require('password-hash');
var session = require('client-sessions');
var User = require('../model/user');
var Watchlist = require('../model/watchlist');
var rpc_client = require('../rpc_client/rpc_client');
var redis_client = require('../redis_client/redis_client');
var mongoose = require('mongoose');
var router = express.Router();

TITLE = 'Smart Zillow';
PROPERTY_TABLE_NAME = 'property';

// Index page
router.get('/', function(req, res, next) {
  var user = checkLoggedIn(req);
  res.render('index', {title: TITLE, logged_in_user: user});
});

// autocomplete for search bar
router.get('/autocomplete', function(req, res, next) {
  var query = req.query.query;
  redis_client.getAutocomplete(query, function(response) {
    res.json(response);
  });
});

router.get('/mylist', function(req, res, next){
  var user_email = checkLoggedIn(req);
  rpc_client.getWatchList(user_email, function(response) {
    console.log(response);

    if (response == undefined || response === null) {
      console.log("No results found.");
    }

    res.render('watch_list', {
      title: TITLE,
      results: response,
      logged_in_user: user_email
    });
  });
})

router.post('/addToList', function(req, res, next){
  var email = req.body.user_email;
  var zpid = req.body.property_zpid;
  var created_price = req.body.created_price;
  var updated_price = req.body.created_price;
  var newList = Watchlist({
    email: email,
    zpid: zpid,
    created_price: created_price
  });

  newList.save(function(err) {
      if (err) throw err;
      req.session.user = email;
      res.status(202).end();
    });
});

// search
router.get('/search', function(req, res, next) {
  logged_in_user = checkLoggedIn(req);

  var query = req.query.search_text; //req.query returns a json
  console.log("search text: " + query);

  rpc_client.searchArea(query, function(response) {
    if (response == undefined || response === null) {
      console.log("No results found.");
    }

    res.render('search_result', {
      title: TITLE,
      query: query,
      results: response,
      logged_in_user: logged_in_user
    });
  });
});

// detail page
router.get('/detail', function(req, res, next) {
  logged_in_user = checkLoggedIn(req);

  var id = req.query.id;
  console.log("detail for id: " + id);

  var is_watched = false;
  // check whether in watchlist
  Watchlist.findOne({email: logged_in_user, zpid: id}, function(err, data) {
    if (err) throw err;
    console.log("Is in list");
    console.log(data);
    if (data) {
      is_watched = true;
    }
  });

  rpc_client.getDetailsByZpid(id, function(response) {
    property = {}
    if (response === undefined || response === null) {
      console.log("No results found");
    } else {
      property = response;
    }

    // Handle predicted value
    var predicted_value = parseInt(property['predicted_value']);
    var list_price = parseInt(property['list_price']);
    property['predicted_change'] = ((predicted_value - list_price) / list_price * 100).toFixed(2);

    // add thousands separator for numbers
    addThousandSeparatorForSearchResult(property);

    // split facts and additional facts
    splitFacts(property, 'facts');
    splitFacts(property, 'additional_facts');

    res.render('detail', {
      title: TITLE,
      query: '',
      logged_in_user: logged_in_user,
      property: property,
      id: id,
      is_watched: is_watched
    });
  });
});

// Login page
router.get('/login', function(req, res, next) {
  res.render('login', {title: TITLE});
});

// Register page
router.get('/register', function(req, res, next){
  res.render('register', {title: TITLE});
});

// Register submit
router.post('/register', function(req, res, next){
  var email = req.body.email; // according to [name]
  var password = passwordHash.generate(req.body.password);
  console.log('register called');
  User.find({email: email}, function(err, users) {
    if (err) throw err;
    if (users.length == 0) {
      // if the email doesn't not exist, create new user
      var newUser = User({
        email: email,
        password: password
      });
      newUser.save(function(err) { // non-blocking way
        if (err) throw err;
        req.session.user = email;
        res.status(202).end();
      });
    } else {
      res.status(400).json({message: 'Email already existed.'});
    }
  });
});

// login submit
router.post('/login', function(req, res, next){
  var email = req.body.email;
  var password = req.body.password;

  User.findOne({email: email}, function(err, user) {
    if (err) throw err;
    if (!user) {
      // user not found
      res.status(400).json({message: "User not found."});
    } else {
      // user found
      if (passwordHash.verify(password, user.password)) {
        console.log(req.session);
        req.session.user = user.email;
        res.status(202).end();
      } else {
        res.status(400).json({message: "Password invalid."});
      }
    }
  });
});

// logout submit
router.get('/logout', function(req, res, next) {
  req.session.reset();
  res.redirect('/');
});

// find mongodb items without using mongoose modal(schema)
function find(collec, query, callback) {
    mongoose.connection.db.collection(collec, function (err, collection) {
    collection.find(query).toArray(callback);
  });
}

function checkLoggedIn(req) {
  if (req.session && req.session.user) {
    return req.session.user;
  }
  return null;
}

function addThousandSeparatorForSearchResult(searchResult) {
  for (var i = 0; i < searchResult.length; i++) {
    addThousandSeparator(searchResult[i]);
  }
}

function addThousandSeparator(property) {
  property['list_price'] = numberWithCommas(property['list_price']);
  property['size'] = numberWithCommas(property['size']);
  property['predicted_value'] = numberWithCommas(property['predicted_value'])
}

function numberWithCommas(x) {
  if (x != null) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
}

function splitFacts(property, field_name) {
  // console.log("splitFacts: \n" + JSON.stringify(property));
  facts_groups = [];
  group_size = property[field_name].length / 3;
  facts_groups.push(property[field_name].slice(0, group_size));
  facts_groups.push(property[field_name].slice(group_size, group_size + group_size));
  facts_groups.push(property[field_name].slice(group_size + group_size));
  property[field_name] = facts_groups;
}

module.exports = router;
