const mongoose = require("mongoose")

const word_schema = new mongoose.Schema({
    word: {
        type: String,
        required: true
    },
    author: {
        name: {
            type: String
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

module.exports = mongoose.model("Ban_words", word_schema)