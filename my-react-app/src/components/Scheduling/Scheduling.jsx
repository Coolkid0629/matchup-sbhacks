import React, { useEffect } from "react";
import Cookies from "js-cookie";

function Matches() {
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

  return (
    <div className="matches-container">
      <h2>User is active on this page</h2>
    </div>
  );
}

export default Matches;
