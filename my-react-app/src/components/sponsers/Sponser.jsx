import React, { useState } from 'react';
import './Sponser.css';

const Sponsors = () => {
  const [sponsors, setSponsors] = useState([
    { name: '.Tech Domains', logo: './tech.png', description: 'A great way to get your own .tech domain!', link: 'https://www.get.tech' },
    { name: 'SingleStore DB', logo: './ss.png', description: 'SingleStore DB', link: 'https://www.singlestore.com' },
    { name: 'Midnight', logo: './midnight.png', description: 'Midnight Blockchain', link: 'https://midnight.network/' },
  ]);

  return (
    <div className="sponsors-container">
      <div className="sponsors-content">
        <h1>Our Sponsors</h1>
        <p>We are proud to be supported by these amazing brands!</p>
      </div>
      <div className="sponsors-gallery">
        {sponsors.map((sponsor, index) => (
          <div key={index} className="sponsor-card">
            <a href={sponsor.link} target="_blank" rel="noopener noreferrer">
              <img src={sponsor.logo} alt={`${sponsor.name} logo`} className="sponsor-logo" />
            </a>
            <h3>{sponsor.name}</h3>
            <p>{sponsor.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sponsors;
