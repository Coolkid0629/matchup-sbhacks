import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import '../Login/Login.css';
import './About.css';

function About() {
  return (
    <div className="login-container">
      <Container className="login-form" style={{ maxWidth: '800px' }}>
        <h2 className="login-title">About UCSBites</h2>
        <p className="login-subtitle">Connecting UCSB Students Through Food</p>
        
        <Row className="mt-4">
          <Col>
            <div className="interests-section">
              <h3 className="interests-title">Our Mission</h3>
              <p>
                UCsBites is a platform designed to bring UCSB students together through their shared love of food. 
                We believe that some of the best friendships and connections are formed over a good meal.
              </p>
            </div>

            <div className="interests-section">
              <h3 className="interests-title">How It Works</h3>
              <div className="category-title">1. Create Your Profile</div>
              <p>Sign up and tell us about your food preferences, favorite cuisines, and dining habits.</p>
              
              <div className="category-title">2. Find Food Buddies</div>
              <p>Match with other UCSB students who share your interests!</p>
              
              <div className="category-title">3. Plan Meetups</div>
              <p>Connect with others and plan meals at your favorite campus eateries or local restaurants.</p>
            </div>

            <div className="interests-section">
              <h3 className="interests-title">Why Choose UCsBites?</h3>
              <div className="interests-container">
                <div className="interest-item">
                  <strong>🤝 Make Friends</strong>
                  <p>Connect with fellow Gauchos who share your food interests</p>
                </div>
                <div className="interest-item">
                  <strong>🍽️ Discover Places</strong>
                  <p>Explore new dining spots around campus and IV</p>
                </div>
                <div className="interest-item">
                  <strong>🌟 Safe Community</strong>
                  <p>Verified UCSB students only</p>
                </div>
                <div className="interest-item">
                  <strong>💫 Shared Experiences</strong>
                  <p>Create memories over delicious meals</p>
                </div>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default About;
