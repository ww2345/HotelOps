const mongoose = require("mongoose");

const bookingSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true
    },
    room: {
      type: Number,
      required: true
    },
    contactno: {
      type: Number,
      required: true
    },
    checkin: {
      type: String
    },
    checkout: {
      type: String
    }
  }
);

const Booking = mongoose.model("Booking", bookingSchema);

module.exports = Booking;

