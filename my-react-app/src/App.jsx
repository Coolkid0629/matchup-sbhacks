import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import About from './components/About/About.jsx'
import NavbarComponent from './components/Navbar/NavbarComponent.jsx';
import FooterComponent from './components/Footer/FooterComponent.jsx';
import Landing from './components/Landing/landing.jsx';
import ProfilePage from './components/Profile/Profile.jsx';

function App() {
  return (
    <Router>
      <div className="app-container">
        <NavbarComponent/>
        <main className="main-content">
          <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/login" element={<Login />} />
          <Route path="/about" element={<About />} />
              <Route path="/profile" element={<ProfilePage/>} />
      </Routes>
        </main>
        <FooterComponent/>
      </div>
    </Router>
  )
}

export default App
