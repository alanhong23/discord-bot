const mongoose = require("mongoose")

const channel_role_schema = new mongoose.Schema({
    message_id: {
        type: Number,
        required: true
    },
    channel_role_id: {
        type: String,
        required: true
    },
    channel_id: {
        type: String,
        required: true
    },
    emoji: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        default: Date.now
    }
})

module.exports = mongoose.model("Channel_roles", channel_role_schema)