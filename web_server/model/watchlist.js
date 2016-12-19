var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var watchlistSchema = new Schema({
  email: {type: String, required: true},
  zpid: {type: String, required: true},
  created_price: Number,
  created_at: Date
});

// On every save, update the timestamp
watchlistSchema.pre('save', function(next) {
  var currentDate = new Date();

  if (!this.created_at) {
    this.created_at = currentDate;
  };

  next();
});

var Watchlist = mongoose.model('watchlist', watchlistSchema, 'watchlist');

module.exports = Watchlist;
