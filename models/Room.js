const mongoose = require("mongoose");

const roomSchema = new mongoose.Schema(
  {
    room: {
      type: Number,
      required: true
    },
    status: {
      type: String,
      required: true
    },
    price: {
      type: Number,
      required: true
    }
  }

);

const Room = mongoose.model("Room", roomSchema);

module.exports = Room;

