import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import NavbarComponent from './components/Navbar/NavbarComponent.jsx';
import Landing from './components/Landing/Landing.jsx';

function App() {
  return (
    <Router>
      <NavbarComponent/>
      <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  )
}

export default App
