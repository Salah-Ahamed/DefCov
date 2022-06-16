const bcrypt =require("bcryptjs");
const Joi = require("joi");
const passwordComplexity = require("joi-password-complexity");


const users = [
    {
        name: "Elda Palumbo",
        email: "Elda@gmail.com",
        password:bcrypt.hashSync("notapassword", 10)
 

    },
    {
        name: "Ashley",
        email: "Ashley@gmail.com",
        password: bcrypt.hashSync("allpassword", 10)

    },
    {
        name: "greens",
        email: "greens@gmail.com",
        password:bcrypt.hashSync("passworduser", 10)

    },
    {
        name: "collins",
        email: "collins@gmail.com",
        password:bcrypt.hashSync("goodpassword", 10)

    }
];
module.exports ={users} ;