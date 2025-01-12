import React from 'react';
import './Spinner.css';

const Spinner = () => {
  return (
    <div className="spinner-overlay">
      <div className="spinner-container">
        <div className="spinner-border" style={{ color: '#8f00ff', width: '3rem', height: '3rem' }} role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <div className="spinner-text">Loading...</div>
      </div>
    </div>
  );
};

export default Spinner;
