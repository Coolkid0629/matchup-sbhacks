import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import About from './components/About/About.jsx'
import NavbarComponent from './components/Navbar/NavbarComponent.jsx';
import FooterComponent from './components/Footer/FooterComponent.jsx';
import Landing from './components/Landing/Landing.jsx';
//import ProfilePage from './components/Profile/Profile.jsx';
import PersonalProfile from './components/Profile/ProfileCard.jsx';
import Spinner from './components/Spinner/Spinner.jsx';
import TimeSelector from './components/Scheduling/Scheduling.jsx';
import Sponsors from './components/sponsers/Sponser.jsx';

// Wrapper component to handle route change loading states
function AppContent() {
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();

  useEffect(() => {
    let timeoutId;
    
    // Start loading
    setIsLoading(true);
    
    // Set a minimum delay before showing content to prevent flash
    timeoutId = setTimeout(() => {
      setIsLoading(false);
    }, 500);

    // Cleanup timeout if component unmounts
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [location]); // Trigger effect on route change

  return (
    <div className="app-container">
      <NavbarComponent/>
      {isLoading && <Spinner />}
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/about" element={<About />} />
          <Route path="/profile" element={<PersonalProfile/>} />
          <Route path="/sponser" element={<Sponsors/>} />
          { <Route path="/scheduling" element={<TimeSelector/>} /> }
      </Routes>
        </main>
        <FooterComponent/>
      </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App
