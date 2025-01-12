import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import './Navbar.css'; // Import the CSS styles

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const username = Cookies.get('username');
    const userpass = Cookies.get('userpass');
    setUsername(username);
    setIsLoggedIn(!!username && !!userpass);
  }, []);
  function handleLogout() {
    Cookies.remove('username');
    Cookies.remove('userpass');
    setIsLoggedIn(false);
    setUsername('');
  }
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <a href="/" className="navbar-a">
          <img src="/Santa_BarBit-A2.png" alt="UCSBites Logo" style={{ height: '100px', width: 'auto' }} />
          &nbsp;
          &nbsp;
          <span>UCSBites</span>
        </a>
      </div>
      
      <div className="nav-links">
        <a href="/" className="nav-link">Home</a>
        <a href="/about" className="nav-link">About</a>
        <a href="/scheduling" className="nav-link">Scheduling</a>
        <a href="/sponser" className="nav-link">Sponsers</a>
      </div>

      <div className="nav-auth">
        {!isLoggedIn ? (
          <>
            <a href="/login" className="auth-btn login">Login</a>
            <a href="/signup" className="auth-btn signup">Sign Up</a>
          </>
        ) : (
          <>
            {username}
            <a href="/profile" className="auth-btn login">Profile</a>
            <button href="/" className='auth-btn signup' onClick={handleLogout}>Logout</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
