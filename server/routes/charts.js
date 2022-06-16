const router = require("express").Router();
const { Result} = require("../models/result");
const { User } = require("../models/user");
var ObjectId = require('mongoose').Types.ObjectId;

router.post("/", async (req, res) => {
	// try {
	       console.log("charts connect")
           console.log(req.body)
        //    const result_user=await new Result({probability: req.body.profileData.probability})
           let user= await User.findOne({email: req.body.email})
        //    user=JSON.stringify(user._id)
        //    console.log(user)
        //    user = user._id.toString();
          let  u=ObjectId(user._id)
          console.log(u)
           res.status(201).send(u);
        //    res.status(201).send({ message: "Results saved  successfully" });

	// } catch (error) {
	// 	res.status(500).send({ message: error });
	// }
});





module.exports = router;