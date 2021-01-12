const router = require("express").Router()
const Tag = require("../models/tags")


//post new tag
router.post("/", async (req, res) => {
    //check if tag name is exist 
    const exist_tag = await Tag.findOne({ tag_name: req.body.tag_name })
    if( exist_tag ) return res.status(400).send({ message: "tag name already exist" })

    //create new tag
    const tag = new Tag({
        tag_name: req.body.tag_name,
        data: req.body.data,
        author: {
            name: req.body.author.name,
            id: req.body.author.id
        }
    })

    try {
        const saved_data = await tag.save()
        res.send({ id: saved_data._id })
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//get specific tag
router.get("/", async(req, res) => {
    const name = req.query.tag_name
    const amount = req.query.amount
    let tag 

    try {
        if ( amount === "all" && name === undefined ){
            tag = await Tag.find().sort({ tag_name: 1 })
        }else if ( amount === "one" && name !== undefined ){
            tag = await Tag.findOne({ tag_name: name })
        }else{
            res.status(400).send({ message: "invalid query parameters" })
        }

        if ( !tag || tag.length === 0) return res.status(400).send({ message: "invalid tag name" })

        res.send(tag)
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//change specific tag
router.put("/:tag_name", async (req, res) => {
    const tag = req.params.tag_name

    //check if new tag name is exist 
    const exist_tag = await Tag.findOne({ tag_name: req.body.tag_name })
    if( exist_tag ) return res.status(400).send({ message: "tag name already exist" })

    //check if tag name is invalid
    const request_name = await Tag.findOne({ tag_name: tag })
    if( !request_name ) return res.status(400).send({ message: "tag name not found" })

    //check if the information is not about to change
    const t_name = req.body.tag_name === undefined ? request_name.tag_name : req.body.tag_name 
    const data = req.body.data === undefined ? request_name.data : req.body.data

    try {
        await Tag.updateOne(
            { tag_name: tag },
            {
                tag_name: t_name,
                data: data,
                date: Date.now()
            }
        )
        res.send({ message: `updated ${tag}` })
    } catch (error) {
        res.status(400).send({ message: error })   
    }
})


//delete specific tag
router.delete("/:tag_name", async (req,res) => {
    const tag = req.params.tag_name
    
    try {
        await Tag.deleteOne({ tag_name: tag })
        res.send({ message: `deleted ${tag}` })
    } catch (error) {
        res.status(400).send({ message: error }) 
    }
})

module.exports = router