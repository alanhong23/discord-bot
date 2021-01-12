const mongoose = require("mongoose")

const Tags_schema = new mongoose.Schema({
    tag_name: {
        type: String,
        required: true
    },
    data: {
        type: String,
        required: true
    },
    author: {
        name: {
            type: String,
        },
        id: {
            type: Number,
            required: true
        }
    },
    date: {
        type: Date,
        default: Date.now
    }
})

module.exports = mongoose.model("Tags", Tags_schema)