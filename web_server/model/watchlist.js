var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var watchlistSchema = new Schema({
  email: {type: String, required: true}, // how about user id?
  zpid: {type: String, required: true},
  created_price: Number,
  created_at: Date,

  // how about this design?
  // list: [
  //   {
  //     zpid: String,
  //     add_price: Number,
  //     add_date: Date,
  //     new_price: Number,
  //     new_date: Date
  //   }
  // ]
});

// On every save, update the timestamp
watchlistSchema.pre('save', function(next) {
  var currentDate = new Date();
  
  if (!this.created_at) {
    this.created_at = currentDate;
  };

  next(); // save data
});

var Watchlist = mongoose.model('watchlist', watchlistSchema, 'watchlist');

module.exports = Watchlist;
