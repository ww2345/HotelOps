const mongoose = require("mongoose");

const roomSchema = new mongoose.Schema(
  {
    number: { type: Number, required: true, unique: true, index: true },
    floor: { type: Number, required: true },
    type: { type: String, required: true },
    status: { type: String, required: true },
    housekeeping: { type: String, required: true },
    rate: { type: Number, required: true },
  },
  { timestamps: true }
);

const Room = mongoose.model("Room", roomSchema);

module.exports = Room;

