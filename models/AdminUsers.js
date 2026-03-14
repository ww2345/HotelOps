const mongoose = require("mongoose");

const adminLoginSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    maxLength: 25
  },
  password: {
    type: String,
    required: true,
    minLength: 5
  }
});

// Use the existing `users` collection (your saved credentials are there).
const admin = mongoose.model("Admin", adminLoginSchema, "users");

module.exports = admin;
