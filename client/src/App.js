import { Route, Routes, Navigate } from "react-router-dom";
import Signup from "./components/Singup";
import Login from "./components/Login";
import Home from "./components/Home";
import Readandagree from "./components/Readandagree";
import Shallowbreath from "./components/Shallowbreath";
import Shallowcough from "./components/Shallowcough";
import Heavycough from "./components/Heavycough";
import VowelE from "./components/VowelE";
import VowelO from "./components/VowelO";
import Fastcounting from "./components/Fastcounting";
import Results1 from "./components/Results1";
import Dashboard from "./components/Charts/Dashboard";
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';


function App() {
	const user = localStorage.getItem("token");

	return (
		<Routes>
			{user && <Route path="/" exact element={<Home />} />}
			<Route path="/Home" exact element={<Home />} />
			<Route path="/signup" exact element={<Signup />} />
			<Route path="/login" exact element={<Login />} />	
			<Route path="/Readandagree" exact element={<Readandagree />} />
			<Route path="/Shallowbreath" exact element={<Shallowbreath />} />
			<Route path="/Shallowcough" exact element={<Shallowcough />} />
			<Route path="/Heavycough" exact element={<Heavycough />} />
			<Route path="/VowelE" exact element={<VowelE />} />
			<Route path="/VowelO" exact element={<VowelO />} />
			<Route path="/Fastcounting" exact element={<Fastcounting />} />
			<Route path="/Results1" exact element={<Results1 />} />	
			<Route path="/Dashboard" exact element={<Dashboard />} />
			<Route path="/" element={<Navigate replace to="/Home" />} />
			
		</Routes>
	);
}

export default App;
