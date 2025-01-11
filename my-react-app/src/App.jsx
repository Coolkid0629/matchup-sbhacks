import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import NavbarComponent from './components/NavBarComponent.jsx';

function App() {
  const [count, setCount] = useState(0)
  return (
    <Router>
      <NavbarComponent/>
      <div> 
      <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login"  element={<Login />} />
      </Routes>
      </div>
    </Router>
  )
}

export default App
