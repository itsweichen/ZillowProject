var express = require('express');
var router = express.Router();
var User = require('../model/user');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {title: 'Smart Zillow'});
});

router.get('/login', function(req, res, next) {
  res.render('login', {title: 'Smart Zillow'});
});

router.get('/register', function(req, res, next){
  res.render('register', {title: 'Smart Zillow'});
});

router.post('/register', function(req, res, next){
  var email = req.body.email; // according to [name]
  var password = req.body.password;
  console.log(User);
  console.log(typeof User);
  User.find({email: email}, function(err, users) {
    if (err) throw err;
    if (users.length == 0) {
      var newUser = User({
        email: email,
        password: password
      });
      newUser.save(function(err) { // non-blocking way
        if (err) throw err;
        res.redirect('/');
      });
    } else {
      res.redirect('/'); // TODO
    }
  });
});

module.exports = router;
