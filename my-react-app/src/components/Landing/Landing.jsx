import React, { useEffect, useState } from 'react';
import './Landing.css';

const Landing = () => {
  const [activeUsers, setActiveUsers] = useState(null);
  const [totalUsers, setTotalUsers] = useState(null);

  useEffect(() => {
    // Fetch the number of active users and total users from the Flask backend
    const fetchUserCount = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/user-count");
        const data = await response.json();
        
        // Handle data format properly
        if (data.total_users !== undefined && data.active_users !== undefined) {
          setActiveUsers(data.active_users);
          setTotalUsers(data.total_users);
        } else {
          console.error('Data format error:', data);
        }
      } catch (error) {
        console.error("Error fetching user count:", error);
      }
    };

    fetchUserCount();
  }, []);

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
          <h3>{activeUsers !== null ? activeUsers : 'Loading...'}</h3>
          <p>People looking to connect</p>
        </div>
        <div className="feature-card">
          <h3>{totalUsers !== null ? totalUsers : 'Loading...'}</h3>
          <p>Total Registered Users</p>
        </div>
        <div className="feature-card">
          <h3>{activeUsers !== null && totalUsers !== null ? (activeUsers / totalUsers * 100).toFixed(2) : 'Loading...'}</h3>
          <p>Active Users (%)</p>
        </div>
      </div>
    </div>
  );
};

export default Landing;
