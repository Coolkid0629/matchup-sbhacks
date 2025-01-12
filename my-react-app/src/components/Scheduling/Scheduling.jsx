import React, { useState } from 'react';

const TimeSelector = () => {
  // Generate the times from 8 AM to 10 PM, spaced 15 minutes apart
  const generateTimes = () => {
    const times = [];
    let currentTime = new Date();
    currentTime.setHours(8, 0, 0, 0); // Start at 8 AM
    while (currentTime.getHours() < 22 || (currentTime.getHours() === 22 && currentTime.getMinutes() === 0)) {
      times.push(currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
      currentTime.setMinutes(currentTime.getMinutes() + 15); // Increment by 15 minutes
    }
    return times;
  };

  const times = generateTimes();
  const [selectedTime, setSelectedTime] = useState('');

  // Function to handle time button click and send API request
  const handleClick = (time) => {
    setSelectedTime(time);

    // Send API request with the selected time
    fetch('http://yourserver.com/api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ time }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('API Response:', data);
      })
      .catch((error) => {
        console.error('Error sending API request:', error);
      });
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100" style={{ margin: '0' }}> 
      <div className="scrollable-container">
        <div className="scrollable-widget" style={{ overflowY: 'scroll', backgroundColor: '#fff' }}>
          {times.map((time, index) => (
            <button
              key={index}
              className={`btn btn-purple text-white w-100 mb-2 ${selectedTime === time ? 'active' : ''}`}
              onClick={() => handleClick(time)}
              style={{ backgroundColor: '#9C54A6' }}
            >
              {time}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TimeSelector;
