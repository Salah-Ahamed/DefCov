import "./Readandagree.css";
import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
const Readandagree = () => {


  const handleLogout = () => {
		localStorage.removeItem("token");
	};

  return (
    <div class="rbackground">
      <div class="rvector">
      <h3 class="rline1"><b>Please Read the terms and conditions before continuing.</b></h3><br/>
        <p ><h5 class="rp">The purpose of the DefCov is to help you make decisions about seeking appropriate medical care.
        This system does not ask about the symptoms you are having, But to record six types of sounds and to upload.
        <br/><br/>
        To continue using this system, Please agree that you have read and understood the contents of this disclaimer.</h5></p><br/>
          
            <h3 class="rline1"><b>I have read and agree the terms and conditions.</b></h3>
          
  <Link to="/Shallowbreath"><button class="rbtn1"><h3 class="rtext"><b>I agree</b></h3></button></Link>
  <Link to="/Home"><button class="rbtn2"><h3 class="rtext"><b>I don't agree</b></h3></button></Link>
      
      </div>
      <nav role="navigation">
  <div id="menuToggle">
     
    <input type="checkbox" />
     
    
    <span></span>
    <span></span>
    <span></span>
     
    
    <ul id="menu">
    
    <Link to="/Login"><a><li>Log In</li></a></Link><br></br>
    <Link to="/Signup"><a><li>Sign up</li></a></Link><br></br>
    <Link to="/Shallowbreath"><a><li>Record</li></a></Link><br></br>
    <Link   onClick={handleLogout} to="/Home"><a><li>Log out</li></a></Link> <br></br> 
    <Link to="/Dashboard"><a><li>Report</li></a></Link>
      
    </ul>
  </div>
</nav>
  </div>
  );
}

export default Readandagree;
