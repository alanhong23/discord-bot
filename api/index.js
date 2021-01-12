const express = require("express")
const mongoose = require("mongoose")
const app = express()
require("dotenv/config")

//connect to database
mongoose.connect(
    process.env.db_connect,
    {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    },
    () => console.log("connect to database")
)

//change req.body to json format
app.use(express.json())

//import routes
const tag_route = require("./routes/tags")
const word_route = require("./routes/ban_words")
const channel_role_route = require("./routes/channel_role")
const delete_message = require("./routes/delete_message")

//middleware
app.use("/tags", tag_route)
app.use("/words", word_route)
app.use("/channel_role", channel_role_route)
app.use("/delete_message", delete_message)

app.listen(3000)