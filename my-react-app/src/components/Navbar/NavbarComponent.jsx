import React from 'react';
import './Navbar.css'; // Import the CSS styles

const Navbar = () => {
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
      </div>

      <div className="nav-auth">
        <a href="/login" className="auth-btn login">Login</a>
        <a href="/signup" className="auth-btn signup">Sign Up</a>
      </div>
    </nav>
  );
};

export default Navbar;
