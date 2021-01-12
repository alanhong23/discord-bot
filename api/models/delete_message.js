const mongoose = require("mongoose")

const delete_message_schema = new mongoose.Schema({
    channel_id: {
        type: String,
        required: true
    },
    guild_id: {
        type: String,
        required:true
    },
    date: {
        type: Date,
        default: Date.now
    }
})

module.exports = mongoose.model("Delete_message", delete_message_schema)