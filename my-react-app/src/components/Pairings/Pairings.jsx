import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 

const DecisionPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('YOUR_API_ENDPOINT'); 
        const data = await response.json();

        // Example: Check a boolean condition in the API response
        if (data.condition === true) { 
          navigate('/waiting'); // Navigate to Page 1
        } else {
          navigate('/successfulPair'); // Navigate to Page 2
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle API request errors (e.g., show an error message)
        navigate('/error'); // Redirect to an error page
      }
    };

    fetchData(); 
  }, []); 

  return (
    <div> 
      {/* Optional: Loading spinner or placeholder while fetching data */}
    </div>
  );
};

export default DecisionPage;