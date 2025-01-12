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
          <h3>1000's</h3>
          <p>of people looking to connect</p>
        </div>
        <div className="feature-card">
          <h3>$10,000+</h3>
          <p>in crypto</p>
        </div>
        <div className="feature-card">
          <h3>50+</h3>
          <p>eating locations</p>
        </div>
      </div>
    </div>
  );
};

export default Landing;
