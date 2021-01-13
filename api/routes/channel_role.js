const router = require("express").Router()
const Channel_role = require("../models/channel_role")


//post new message
router.post("/", async (req,res) => {

    //check if the channel already has a channel role
    const exist_channel_id = Channel_role.findOne({ channel_id: req.body.channel_id })
    if (exist_channel_id) return res.status(400).send({ message: "channel id exist" })

    //create new channel role proototype
    const channel_role = new Channel_role({
        message_id: req.body.message_id,
        channel_role_id: req.body.channel_role_id,
        channel_id: req.body.channel_id,
        emoji: req.body.emoji
    })

    try {
        const saved_data = await channel_role.save()
        res.send({ id: saved_data._id })
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//get specific channel role information
router.get("/", async (req,res) => {
    id = req.query.message_id

    data = await Channel_role.find({ message_id: id })
    if ( data.length === 0 ) return res.status(400).send({ message: "found none" })

    try {
        res.send(data)
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//delete the channel role information along with the message
router.delete("/", async (req,res) => {
    mes_id = req.query.message_id

    try {
        await Channel_role.deleteMany({ message_id: mes_id })
        res.send({ message: `${mes_id} deleted` })
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


module.exports = router
