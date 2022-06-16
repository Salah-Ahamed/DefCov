import './Dashboard.css';
import Chart from "./Chart";
import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import  { useRef, useEffect } from 'react';



const Dashboard = () => {

  // const [filteruser, SetUser] = useState(null);
  let profileData = useState(null)
 
   useEffect(function effectFunction() {
    async function fetchUser() {
      const user_data = JSON.parse(localStorage.getItem('token'));
      const response = await axios.post('http://localhost:8080/api/charts',user_data);
          //  const json = await response;
          console.log(response.data)
          //  SetUser(response.data);
          //  console.log(filteruser)
          // setProfileData(({
          //        user:response.data}))
          profileData=response.data

          console.log(profileData)
       }
       fetchUser();
   }, [profileData]);

   const handleLogout = () => {
		localStorage.removeItem("token");
	};





  return <div className="App">
    
      
       <div className="charts">
       <h2 className="title">Your Progress</h2>
       
      {profileData && <div>
         <Chart height={'600px'} width={'800px'} filter={profileData} chartId={'6230cd2f-edfd-41a5-850d-38f4775fbc7f'}/> 
       <Chart height={'600px'} width={'800px'} filter={profileData}  chartId={'6230d4ae-73ca-453e-8dc5-3424988ff809'}/> 
      <Chart height={'600px'} width={'800px'} filter={'62507eae30d79fa7eb3af1f7'} chartId={'6230e0f3-73ca-41e6-8a4a-34249899dc7c'}/> 
   
       </div>
}
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
    <Link onClick={handleLogout} to="/Home"><a><li>Log out</li></a></Link> <br></br> 
    <Link to="/Dashboard"><a><li>Report</li></a></Link>
      
    </ul>
  </div>
</nav>
  
     
  </div>
};

export default Dashboard;