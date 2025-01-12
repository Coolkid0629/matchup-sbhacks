import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import './Waiting.css';

const ApiRequestComponent = () => {
  const [bestMatch, setBestMatch] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const email = Cookies.get('username');
    const password = Cookies.get('userpass');

    if (email && password) {
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
          if (data && data.length > 0) {
            // Find the match with the highest similarity score
            const highestMatch = data.reduce((best, current) =>
              current.similarity > best.similarity ? current : best
            );
            setBestMatch(highestMatch);
          } else {
            setBestMatch(null); // No matches found
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          setBestMatch(null); // Handle errors gracefully
        })
        .finally(() => setLoading(false));
    } else {
      console.log('No email or password found in cookies.');
      setLoading(false);
    }
  }, []);

  return (
    <div className="sponsors-container">
      <div className="sponsors-content">
        <h1>Best Match</h1>
        {loading ? (
          <p>Loading...</p>
        ) : bestMatch ? (
          <div>
            <h3>{bestMatch.match_name}</h3>
            <p>
              Probability of having a great meal together: <strong>{bestMatch.similarity*100}%</strong>
            </p>
            <p>
              Common Interests: <strong>{bestMatch.common_interests.join(', ')}</strong>
            </p>
            <p>
              Lunch Time: <strong>{bestMatch.lunch_time}</strong>
            </p>
          </div>
        ) : (
          <p>No match found.</p>
        )}
      </div>
    </div>
  );
};

export default ApiRequestComponent;
