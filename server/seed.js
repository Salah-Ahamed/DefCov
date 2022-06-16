const {Result} =require('./models/result')
const dotenv = require('dotenv');
const connectDB =require( './db.js');
const { User } = require('./models/user');
const { users } = require('./data/users');
const { results } = require('./data/results');


dotenv.config();

connectDB();


const importData=async()=>{
    try{
        await User.deleteMany();
        await Result.deleteMany();
    
        
    const createdUsers=await User.insertMany(users)
    const user1=createdUsers[0]._id;
    const user2=createdUsers[1]._id;
    const user3=createdUsers[2]._id;
    const user4=createdUsers[3]._id;
    // createdUsers()

    // const createdUsers=await connectDB.User.insertOne(users)

     const sampleProbabilities = results.map(probability => {
            return { ...probability,user:user1};
        });

        await Result.insertMany(sampleProbabilities);
        console.log("Data Imported!".green);
        process.exit();
    } catch (error) {
        console.log(`Error: ${error}`.red);
        console.log(error.stack)
        process.exit(1);
    }
}

const destroyData = async () => {
    try {
        await User.deleteMany();
        await Result.deleteMany();

        console.log("Data Destroyed!".red);
        process.exit();
    } catch (error) {
        console.log(`Error: ${error}`.red);
        process.exit(1);
    }
}

if (process.argv[2] == '-d') {
    destroyData();
} else {
    importData();
}


