import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";

function Matches() {
  const [matches, setMatches] = useState([]);
  
  useEffect(() => {
    // Get email and password from cookies
    const email = Cookies.get("username");
    const password = Cookies.get("userpass");

    if (!email || !password) {
      console.error("User is not logged in. Missing cookies.");
      return;
    }

    // Set the user status to active when the component is mounted
    updateUserStatus("active", email, password);

    // Fetch matches for the logged-in user
    fetchMatches(email, password);

    // Cleanup function to set the status to inactive when the user leaves the page (optional)
    return () => {
      updateUserStatus("inactive", email, password);
    };
  }, []);

  const updateUserStatus = async (status, email, password) => {
    const statusData = { email, password, status };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/update-status", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(statusData),
      });

      if (!response.ok) {
        console.error("Failed to update status:", await response.json());
      }
    } catch (error) {
      console.error("Error updating user status:", error);
    }
  };

  const fetchMatches = async (email, password) => {
    const userData = { email, password };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/matches", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        const data = await response.json();
        setMatches(data);
      } else {
        console.error("Failed to fetch matches:", await response.json());
      }
    } catch (error) {
      console.error("Error fetching matches:", error);
    }
  };

  return (
    <div className="matches-container">
      <h2>Your Matches</h2>
      {matches.length > 0 ? (
        <div className="match-list">
          {matches.map((match, index) => (
            <div key={index} className="match-card">
              <h3>{match.match_name}</h3>
              <p><strong>Common Interests:</strong> {match.common_interests.join(", ")}</p>
              <p><strong>Similarity Score:</strong> {match.similarity}</p>
              <p><strong>Lunch Time:</strong> {match.lunch_time}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No matches found. Please check back later!</p>
      )}
    </div>
  );
}

export default Matches;
