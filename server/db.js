// const mongoose = require("mongoose");

// module.exports = () => {
// 	const connectionParams = {
// 		useNewUrlParser: true,
// 		useUnifiedTopology: true,
// 	};
// 	try {
// 		mongoose.connect(process.env.DB, connectionParams);
// 		console.log("Connected to database successfully");
// 	} catch (error) {
// 		console.log(error);
// 		console.log("Could not connect database!");
// 	}
// };

const mongoose =require('mongoose');

const connectDB = async () => {
    try {
        const conn = await mongoose.connect(process.env.DB_CONNECT, {
            useUnifiedTopology: true,
            useNewUrlParser: true,
            // useCreateIndex: true
        });

        console.log(`MongoDB connected: ${conn.connection.host}`);
    } catch (error) {
        console.log(`Error: ${error.message}`);
        // Exist when error occurs
        process.exit(1);
    }
}


module.exports= connectDB;
