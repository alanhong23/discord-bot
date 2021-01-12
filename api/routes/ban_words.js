const router = require("express").Router()
const Words = require("../models/ban_words")

//post new ban word
router.post("/", async (req, res) => {
    //check if word is exist 
    const exist_word = await Words.findOne({ word: req.body.word})
    if( exist_word ) return res.status(400).send({ message: "word already exist" })

    //create new ban word
    const word = new Words({
        word: req.body.word,
        author: {
            name: req.body.author.name,
            id: req.body.author.id
        }
    })

    try {
        const saved_data = await word.save()
        res.send({ id: saved_data._id })
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//get specific ban word
router.get("/", async(req, res) => {
    const word = req.query.word
    const amount = req.query.amount
    let ban_word 

    try {
        if ( amount === "all" && word === undefined ){
            ban_word  = await Words.find().sort({ word: 1 })
        }else if ( amount === "one" && word !== undefined ){
            ban_word = await Words.findOne({ word: word })
        }else{
            res.status(400).send({ message: "invalid query parameters" })
        }

        res.send(ban_word)
    } catch (error) {
        res.status(400).send({ message: error })
    }
})


//change specific ban word
router.put("/:ban_word", async (req, res) => {

    //check if new word is exist 
    const exist_word = await Words.findOne({ word: req.body.word })
    if( exist_word ) return res.status(400).send({ message: "word already exist" })

    //check if old word is invalid
    const old_word = await Words.findOne({ word: req.params.ban_word })
    if( !old_word ) return res.status(400).send({ message: "word not found" })

    try {
        await Words.updateOne(
            { word: old_word.word },
            {
                word: req.body.word,
                date: Date.now()
            }
        )
        res.send({ message: `updated ${old_word.word}` })
    } catch (error) {
        res.status(400).send({ message: error })   
    }
})


//delete specific ban word
router.delete("/:ban_word", async (req,res) => {
    const word = req.params.ban_word
    
    try {
        await Words.deleteOne({ word: word })
        res.send({ message: `deleted ${word}` })
    } catch (error) {
        res.status(400).send({ message: error }) 
    }
})


module.exports = router