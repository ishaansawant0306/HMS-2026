const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();

//middlewares
app.use(cors());
app.use(express.json());

//test route
app.get("/", (req, res) => {
    res.send("HMS Backend running");
});

// test API route
app.get("/test", (req,res) => {
    res.json({ message: "API working perfectly"});
});

// database connection 
//mongoose.connect(process.env.MONGO_URI)
//.then(() => console.log("Database connected"))
//.catch((err) => console.log(err));

//start server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
