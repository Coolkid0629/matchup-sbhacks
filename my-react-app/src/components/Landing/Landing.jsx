import React from 'react';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1>Welcome to UCSBites</h1>
        <p>Connect, Eat, and Collaborate at UCSB's Premier Campus</p>
        <div className="cta-buttons">
          <a className="primary-btn auth-btn" href="/signup">Join Now</a>
          <a className="secondary-btn" href="/about"> Learn More</a>
        </div>
      </div>
      <div className="landing-features">
        <div className="feature-card">
          <h3>GET NUM FROM FLASK</h3>
          <p>of people looking to connect</p>
        </div>
        <div className="feature-card">
          <h3>4</h3>
          <p>Dining Hall Locations</p>
        </div>
        <div className="feature-card">
          <h3>NUM PAIRINGS</h3>
          <p>in </p>
        </div>
      </div>
    </div>
  );
};

export default Landing;
