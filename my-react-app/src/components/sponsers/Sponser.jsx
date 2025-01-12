import React from 'react';
import './Sponser.css';

const Sponser = () => {
  return (
    <div className="sponser-container">
      <div className="sponser-content">
        <h1>SingleStoreDB</h1>
        <p>Tech that powers UCSBites with speed and scalability</p>
        <div className="cta-buttons">
          <a className="primary-btn auth-btn" href="https://www.singlestore.com">Visit SingleStoreDB</a>
        </div>
      </div>
      <div className="sponser-info">
        <div className="info-card">
          <h3>Tech Powerhouse</h3>
          <p>SingleStoreDB offers a fast, scalable, and reliable database solution for modern applications.</p>
        </div>
        <div className="info-card">
          <h3>Innovative Solutions</h3>
          <p>Trusted by companies for handling massive amounts of data in real-time, delivering unparalleled performance.</p>
        </div>
        <div className="info-card">
          <h3>Why Choose Them?</h3>
          <p>SingleStoreDB integrates seamlessly with various tech stacks, ensuring smooth operations and maximum efficiency.</p>
        </div>
      </div>
      <div className="sponser-content">
        <h1>Tech Domains: .tech</h1>
        <p>Tech that provide UCSBites with domain name</p>
        <div className="cta-buttons">
          <a className="primary-btn auth-btn" href="https://get.tech/">Visit Tech Domains</a>
        </div>
      </div>
      <div className="sponser-info">
        <div className="info-card">
          <h3>Innovation-Focused</h3>
          <p>The .Tech domain highlights a brand's focus on innovation in the tech industry.</p>
        </div>
        <div className="info-card">
          <h3>Global Recognition</h3>
          <p>Tech is gaining worldwide recognition, providing a unique online presence.</p>
        </div>
        <div className="info-card">
          <h3>Versatility</h3>
          <p>Ideal for startups, companies, and enthusiasts, the .Tech domain suits any tech-driven venture.</p>
        </div>
      </div>
      <h2>Tech we Tried Using</h2>
      <div className="sponser-content">
        <h1>Midnight</h1>
        <p>Tech that provides UCSBites users' data protection blockchain</p>
        <div className="cta-buttons">
          <a className="primary-btn auth-btn" href="https://midnight.network/">Visit Midnight</a>
        </div>
      </div>
      <div className="sponser-info">
        <div className="info-card">
          <h3>Enhanced Security</h3>
          <p>Midnight uses blockchain technology to provide robust, tamper-proof data protection, ensuring your sensitive information is safe.</p>
        </div>
        <div className="info-card">
          <h3>Decentralized Control</h3>
          <p>With a decentralized approach, Midnight allows users to maintain full control over their data without relying on central authorities.</p>
        </div>
        <div className="info-card">
          <h3>Privacy-Focused</h3>
          <p>Midnight prioritizes user privacy by leveraging encryption and blockchain to ensure that personal data is never exposed to unauthorized parties.</p>
        </div>
      </div>
      <div className="tech-stack">
        <h2>Tech We Use</h2>
        <ul>
          <li>SingleStoreDB - Scalable, real-time data</li>
          <li>React - Fast, interactive UI</li>
          <li>Node.js - Backend services</li>
          <li>CSS Grid & Flexbox - Responsive design</li>
          <li>Flask - Backend Compability with SingleStoreDB</li>
        <li>.Tech Domains - Easy to start domain name</li>
            <li>Midnight - Fast Data protection</li>
        </ul>
      </div>
      
    </div>
  );
};

export default Sponser;
