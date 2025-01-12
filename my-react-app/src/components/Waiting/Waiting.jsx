import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import './Waiting.css';

const ApiRequestComponent = () => {
  const [bestMatch, setBestMatch] = useState(null);

  useEffect(() => {
    // Retrieve email and password from cookies
    const email = Cookies.get('username');
    const password = Cookies.get('userpass');

    if (email && password) {
      // Make the API request using the cookies data
      fetch('http://127.0.0.1:5000/api/matches', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          // Find the match with the highest similarity
          const highestMatch = data.reduce((max, match) =>
            match.similarity > max.similarity ? match : max
          );
          setBestMatch(highestMatch); // Set the best match to state
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    } else {
      console.log('No email or password found in cookies.');
    }
  }, []); // Empty dependency array to only run on component mount

  return (
    <div className="sponsors-container">
      <div className="sponsors-content">
        <h1>Best Match</h1>
        {bestMatch ? (
          <div>
            <h3>{bestMatch.match_name}</h3>
            <p><strong>Similarity:</strong> {bestMatch.similarity}</p>
            <p><strong>Lunch Time:</strong> {bestMatch.lunch_time}</p>
            <p><strong>Common Interests:</strong> {bestMatch.common_interests.join(', ')}</p>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
};

export default ApiRequestComponent;
