import React from 'react';
import './Footer.css';

const FooterComponent = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-brand">
        <p>© 2024 UCSBites</p>

        </div>
        <div className="footer-links">
          <a href="/about" className="footer-link">About</a>
          <a href="/about" className="footer-link">Contact</a>
          <a href="#" className="footer-link">Privacy</a>
          <a href="#" className="footer-link">Terms</a>
        </div>
        <div className="footer-social">
          <a href="https://github.com/Coolkid0629/matchup-sbhacks/tree/main" className="social-link">GitHub</a>
        </div>
      </div>
    </footer>
  );
};

export default FooterComponent;
