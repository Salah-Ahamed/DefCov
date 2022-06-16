const router = require("express").Router();
const { Result} = require("../models/result");
const bcrypt = require("bcrypt");
const { User } = require("../models/user");


router.post("/", async (req, res) => {
	try {
	       console.log("works")
           console.log(req.body)
           const result_user=await new Result({probability: req.body.profileData.probability})
           const user= await User.findOne({email: req.body.user.email})
           result_user.user = user._id;
           result_user.save();
           console.log(result_user)
           res.status(201).send({ message: "Results saved  successfully" });

	} catch (error) {
		res.status(500).send({ message: error });
	}
});





module.exports = router;