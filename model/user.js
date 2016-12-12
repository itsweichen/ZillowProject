var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var userSchema = new Schema({
  email: {type: String, require: true, unique: true},
  password: {type: String, required: true}, // can use passwordhash library
  created_at: Date,
  updated_at: Date
});

// On every save, update the timestamp
userSchema.pre('save', function(next) {
  var currentDate = new Date();

  this.updated_at = currentDate;

  if (!this.created_at) {
    this.created_at = currentDate;
  }

  next(); // save data
});

var User = mongoose.model('users', userSchema);

module.exports = User;
