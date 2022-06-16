// import { useState } from "react";
import axios from "axios";
import React from "react";
import im2 from "../../images/im2.png";
import  styles from "./heavycough.css";
import rec from "recorderjs";
import { useReactMediaRecorder } from "react-media-recorder";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { ReactMic } from 'react-mic'; 
import AudioAnalyser from "react-audio-analyser";



// import { Link, useNavigate } from "react-router-dom";

export default class Recordaudio extends  React.Component {
  constructor(props) {
    super(props);
    this.state = {
      
      count : 0
      
    };
    this.startTimer = this.startTimer.bind(this)
    this.stopTimer = this.stopTimer.bind(this)
    this.resetTimer = this.resetTimer.bind(this)
  }
  startTimer(){
    this.timer = setInterval(()=>
    this.setState({
        count: this.state.count + 1
    }),1000)
}
stopTimer(){
    clearInterval(this.timer)
}
resetTimer(){
    this.setState({count:0})
}

  controlAudio(status) {
    this.setState({
      status
    });
  }

  changeScheme(e) {
    this.setState({
      audioType: e.target.value
    });
  }

  componentDidMount() {
    this.setState({
      audioType: "audio/wav"
    });
  }


  render() {
    const { status, audioSrc, audioType } = this.state;
    const {error, setError} = this.state;
   
    const audioProps = {
      audioType,
      status,
      audioSrc,
     
      timeslice: 1000,
      startCallback: e => {
        console.log("succ start", e);
      },
      pauseCallback: e => {
        console.log("succ pause", e);
      },
      stopCallback: e => {
        this.setState({
           audioSrc: window.URL.createObjectURL(e),
          

        });
        console.log("succ stop", e);
      },
      onRecordCallback: e => {
        console.log("recording", e);
      },
      errorCallback: err => {
        console.log("error", err);
      }
    };

    
    const handleRedirect =async (e) =>{
      console.log("ok")
       window.location.href = '/VowelE';
    }



    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
             
              console.log("deed",Audio)

              const blob = await fetch(audioSrc)
              .then(response => response.blob());
              
              console.log(blob)
              let data = new FormData()
             
              data.append('file', blob, 'demo.wav');
              fetch('http://127.0.0.1:5000/heavy_cough', {
                method: 'POST',
                body: data
      

        }).then(response => response.json()
        ).then(json => {
            console.log(json)
            handleRedirect()
        });

		} catch (error) {
			if (
				
				error.response &&
				error.response.status >= 400 &&
				error.response.status <= 500
			) {
				console.log(error);
				setError(error.response.data.message);
				
			}
		}
	};



    return (
      <div class="chbackground">
        <div class="timer">
        
        <h3>Time: {this.state.count}</h3>
                
         
        </div>
           
        <img src={im2} alt="image" class="chimg2"></img>
        <img src={im2} alt="image" class="chimg3"></img>
        <h1 class="ch1line1">Record your HEAVY COUGH</h1>
        <div class="animationbox"><AudioAnalyser {...audioProps}
        strokeColor="#000000"
        backgroundColor="#FFFFFF"></AudioAnalyser></div>
          
            <button className="rebtn1" onClick={()=>{ this.controlAudio("recording"); this.startTimer() }}><b/>Start</button>
            <button className="rebtn2" onClick={() => {this.controlAudio("paused");this.stopTimer()}}><b/>Pause</button>
            <button className="rebtn3" onClick={() => {this.controlAudio("inactive");this.stopTimer()}}><b/>Stop</button>
            <Link to="/VowelE"><button className="rebtn4" onClick={handleSubmit}><b/>Upload</button></Link>
            {/* <Navigate to="/Shallowcough" replace={true} /> */}
          </div>
        
      
    );
  }
}



// export default Recordaudio;

