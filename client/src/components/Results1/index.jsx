import im13 from "../../images/im13.png";
import "./results1.css";
import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import  { useRef, useEffect } from 'react';







const Results1 = () => {

    
  const [profileData, setProfileData] = useState(null)

  // const handleChange = ({ currentTarget: p}) => {
	// 	setProfileData({ ...profileData, [input.name]: input.value });
	// };

//   const isInitialMount = useRef(true);

// useEffect(() => {
//   if (isInitialMount.current) {
//      isInitialMount.current = false;
//   } else {
//       // Your useEffect code here to be run on update
//   }
// });


  function getData() {
  
    axios({
      method: "GET",
      url:"http://127.0.0.1:5000/results"
    })
    .then((response) => {
      const res =response.data
      console.log(res)
      setProfileData(({
        covid_status: res.covid_status,
        probability : res.probability 
      }))
      console.log(profileData)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}



    //end of new line 




    function sendData () {
   
   
    const user = JSON.parse(localStorage.getItem('token'));
    console.log(user)
    // const profileData={profileData && profileData.covid_status}
    const reactData = {profileData,user};
    console.log(reactData)

    const url ="http://localhost:8080/api/results"
    // localStorage.setItem("token", res.data);
    // const user = JSON.parse(localStorage.getItem('token'));
    // console.log(user)
    axios. post(url, reactData)
    . then(res => console. log('Data send'))
    . catch(err => console. log(err. data))
    }

    
      //end of new line 

      const handleLogout = () => {
        localStorage.removeItem("token");
      };
    const [show,setShow]=useState(true)

  return (
    
    <div class = "re1background">
       	<meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
      <img src={im13} alt="image" class="re1img"></img>
      <div class="results">
      <h1 class="text">To get your results double click the button: </h1><br/>
      <button onClick={() => { getData();sendData();setShow(false);}}>Click me</button>
        {profileData && <div>
              <p  class="re1line1">You have tested : {profileData.covid_status}</p>
              <Link to="/Dashboard"><button class="re1btn"><h5 class="re1text">Check your progress</h5></button></Link>
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
    <Link  onClick={handleLogout} to="/Home"><a><li>Log out</li></a></Link> <br></br> 
    <Link to="/Dashboard"><a><li>Report</li></a></Link>
      
    </ul>
  </div>
</nav>
    </div>
  );
}

export default Results1;
