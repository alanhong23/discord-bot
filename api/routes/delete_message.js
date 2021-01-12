const Delete_message = require("../models/delete_message")
const router = require("express").Router()


router.post("/", async (req, res) => {

    const exist_channel_id = await Delete_message.findOne({ channel_id: req.body.channel_id })
    if (exist_channel_id) return res.status(400).send({ message: "this channel already is deleted message channel" })

    const exist_guild_id = await Delete_message.findOne({ guild_id: req.body.guild_id })
    if (exist_guild_id) return res.status(400).send({ message: "this server already had a deleted message channel" })

    const channel_information = new Delete_message({
        channel_id: req.body.channel_id,
        guild_id: req.body.guild_id
    })

    try {
        const saved_data = await channel_information.save()
        res.send({ id: saved_data._id })
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


router.get("/", async (req, res) => {

    const channel = await Delete_message.findOne({ guild_id: req.query.guild_id })
    if (!channel) return res.status(400).send({ message: "found none" })

    try{
        res.send({ channel_id: channel.channel_id })
    } catch( error ){
        res.status(400).send({ message: error })
    }
})


router.delete("/", async (req, res) => {
    const chan_id = req.query.channel_id
    const gui_id = req.query.guild_id

    const guild = await Delete_message.findOne({ guild_id: gui_id })
    if (!guild) return res.status(400).send({ message: "this server doesn't has delete message channel" })

    const channel = await Delete_message.findOne({ channel_id: chan_id })
    if (!channel) return res.status(400).send({ message: "this is not delete message channel" })

    try {
        await channel.deleteOne()
        res.send({ message: `deleted ${chan_id}` })
    } catch (error) {
        req.status(400).send({ message: error })
    }
})


module.exports = router