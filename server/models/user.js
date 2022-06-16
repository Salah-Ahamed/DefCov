const mongoose = require("mongoose");
const jwt = require("jsonwebtoken");
const Joi = require("joi");
const dotenv = require('dotenv');
const passwordComplexity = require("joi-password-complexity");

const userSchema = new mongoose.Schema({
	// firstname: { type: String, required: true },
	// lastName: { type: String, required: true },
	email: { type: String, required: true },
	password: { type: String, required: true },
});

userSchema.methods.generateAuthToken = function () {
	const token = jwt.sign({ _id: this._id }, process.env.JWTPRIVATEKEY, {
		expiresIn: "7d",
	});
	return token;
};


const validate = (data) => {
	const schema = Joi.object({
		// firstname: Joi.string().required().label("firstName"),
		// lastName: Joi.string().required().label("lastName"),
		email: Joi.string().email().required().label("email"),
		password: passwordComplexity().required().label("password")
	});
	return schema.validate(data);
};

const User = mongoose.model("user", userSchema);
module.exports = { User, validate };
