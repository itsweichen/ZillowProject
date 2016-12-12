var express = require('express');
var passwordHash = require('password-hash');
var session = require('client-sessions');
var User = require('../model/user');

var router = express.Router();

TITLE = 'Smart Zillow';

// Index page
router.get('/', function(req, res, next) {
  res.render('index', {title: TITLE});
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
  var password = req.body.password;

  User.find({email: email}, function(err, users) {
    if (err) throw err;
    if (users.length == 0) {
      // if the email doesn't not exist
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
      res.redirect('/'); // TODO
    }
  });
});

// login submit
router.post('/login', function(req, res, next){
  var email = req.body.email;
  var password = req.body.password;


});



module.exports = router;
