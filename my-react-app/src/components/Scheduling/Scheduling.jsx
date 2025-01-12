import React, { useState, useEffect } from 'react';

const Scheduling = () => {
  const [match, setMatch] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatchData = async () => {
        try {
          // Fetch user1 data
          const user1Response = await fetch("http://127.0.0.1:5000/api/login", {
            method: "POST",
            mode: "no-cors",
            /* headers: {
              "Content-Type": "application/json",
            }, */
            body: JSON.stringify({
              email: "user1@gmail.com",
              password: "1",
            }),
          });
      
          if (!user1Response.ok) {
            throw new Error("Failed to fetch user1 data");
          }
      
          const user1 = await user1Response.json();
      
          // Fetch user2 data
          const user2Response = await fetch("http://127.0.0.1:5000/api/login", {
            method: "POST",
            mode: "no-cors",
            /* headers: {
              "Content-Type": "application/json",
            }, */
            body: JSON.stringify({
              email: "user2@gmail.com",
              password: "1",
            }),
          });
      
          if (!user2Response.ok) {
            throw new Error("Failed to fetch user2 data");
          }
      
          const user2 = await user2Response.json();
      
          // Process match information locally
          const user1Interests = new Set(user1.interests.split(", ").map((interest) => interest.toLowerCase()));
          const user2Interests = new Set(user2.interests.split(", ").map((interest) => interest.toLowerCase()));
      
          const commonInterests = Array.from(user1Interests).filter((interest) =>
            user2Interests.has(interest)
          );
      
          // Dummy similarity calculation (if vector info isn't directly provided by the backend)
          const similarity = Math.random().toFixed(2); // Replace with actual similarity if needed
      
          // Save match data
          setMatch({
            user1: user1.name,
            user2: user2.name,
            commonInterests: commonInterests,
            similarity: similarity,
          });
        } catch (err) {
          setError(err.message || "Error fetching match data.");
        }
      };
      
    fetchMatchData();
  }, []);

  return (
    <div>
      <h1>Scheduling</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {match ? (
        <div>
          <h2>Match Found</h2>
          <p>
            <strong>User 1:</strong> {match.user1}
          </p>
          <p>
            <strong>User 2:</strong> {match.user2}
          </p>
          <p>
            <strong>Common Interests:</strong> {match.commonInterests.join(", ")}
          </p>
          <p>
            <strong>Similarity:</strong> {match.similarity}
          </p>
        </div>
      ) : (
        <p>Loading match data...</p>
      )}
    </div>
  );
};

export default Scheduling;
