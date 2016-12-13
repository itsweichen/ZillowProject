var express = require('express');
var passwordHash = require('password-hash');
var session = require('client-sessions');
var User = require('../model/user');
var rpc_client = require('../rpc_client/rpc_client');

var router = express.Router();

TITLE = 'Smart Zillow';

// Index page
router.get('/', function(req, res, next) {
  var user = checkLoggedIn(req);
  res.render('index', {title: TITLE, logged_in_user: user});
});

// search
router.get('/search', function(req, res, next) {
  var query = req.query.search_text; //req.query returns a json
  console.log("search text: " + query);

  rpc_client.searchArea(query, function(response) {
    if (response == undefined || response === null) {
      console.log("No results found.");
    }

    res.render('search_result', {
      title: TITLE,
      query: query,
      results: response
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
        res.redirect('/');
      });
    } else {
      // TODO
      // if false, render the page
      res.render('register', {
        title: TITLE,
        message: 'Email already existed.'
      });
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
      res.render('login', {
        title: TITLE,
        message: "User not found."
      })
    } else {
      // user found
      if (passwordHash.verify(password, user.password)) {
        console.log(req.session);
        req.session.user = user.email;
        res.redirect('/');
      } else {
        res.render('login', {
          title: TITLE,
          message: "Password is incorrect."
        });
      }
    }
  });
});

// logout submit
router.get('/logout', function(req, res, next) {
  req.session.reset();
  res.redirect('/');
});

function checkLoggedIn(req) {
  if (req.session && req.session.user) {
    return req.session.user;
  }
  return null;
}


module.exports = router;
