import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 


const DecisionPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/pairings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            password: password
        }), // Send username and password in the body
      });
        const data = await response.json();

        // Example: Check a boolean condition in the API response
        if (data.condition === true) { 
          navigate('/waiting'); 
        } else {
          navigate('/successfulPair');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle API request errors (e.g., show an error message)
        navigate('/error'); // Redirect to an error page
      }
    };
    const email = Cookies.get("username");
    const password = Cookies.get("userpass");

    if (!email || !password) {
        console.error("User is not logged in. Missing cookies.");
        return;}

    fetchData(); 
  }, []); 

  return (
    <div> 
      {/* Optional: Loading spinner or placeholder while fetching data */}
    </div>
  );
};

export default DecisionPage;