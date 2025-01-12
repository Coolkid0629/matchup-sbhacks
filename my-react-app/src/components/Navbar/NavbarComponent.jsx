import React from 'react';
import './Navbar.css'; // Import the CSS styles

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <a href="/">
          <img src="/Santa_BarBit-A.png" alt="UCSBites Logo" style={{ height: '100px', width: 'auto' }} />
        </a>
      </div>
      
      <div className="nav-links">
        <a href="/" className="nav-link">Home</a>
        <a href="/about" className="nav-link">About</a>
        <a href="/projects" className="nav-link">Scheduling</a>
      </div>

      <div className="nav-auth">
        <a href="/login" className="auth-btn login">Login</a>
        <a href="/signup" className="auth-btn signup">Sign Up</a>
      </div>
    </nav>
  );
};

export default Navbar;
