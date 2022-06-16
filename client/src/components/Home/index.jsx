import React from 'react';
import im2 from "../../images/im2.png"; // gives image path
import im9 from "../../images/im9.png";
import im16 from "../../images/im16.png";
import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import "./Home.css";



const Home = () => {
  return(
    <div className='body'>
    
    <div class="background">
    {/* <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta> */}
   <div>
     <p class="Hline1"><b>DefCov</b></p>
     <h1 class="Hline2"><b>The best way to cure covid-19 is to Prevent.</b></h1>
     <Link to="/login"><button class="hbtn1"><h3 class="label">Log In</h3></button></Link>
        <Link to="/signup"><button class="hbtn2"><h3 class="label">Sign Up</h3></button></Link> 
        </div>
  </div>
  </div>
  )
}

export default Home;