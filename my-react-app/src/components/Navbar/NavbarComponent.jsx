import React from 'react';
import './Navbar.css'; // Import the CSS styles

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span>UCSBites</span>
      </div>
      
      <div className="nav-links">
        <a href="/" className="nav-link">Home</a>
        <a href="/about" className="nav-link">About</a>
        <a href="/projects" className="nav-link">Projects</a>
      </div>

      <div className="nav-auth">
        <a href="/login" className="auth-btn login">Login</a>
        <a href="/signup" className="auth-btn signup">Sign Up</a>
      </div>
    </nav>
  );
};

export default Navbar;
