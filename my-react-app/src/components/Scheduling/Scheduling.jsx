import React, { useState } from 'react';
import { Button, Container, Row, Col } from 'react-bootstrap';
import './Scheduling.css'; 
import Cookies from "js-cookie";

const TimeSelector = () => {
  const generateTimes = () => {
    const times = [];
    let currentTime = new Date();
    currentTime.setHours(8, 0, 0, 0); 
    while (currentTime.getHours() < 22 || (currentTime.getHours() === 22 && currentTime.getMinutes() === 0)) {
      times.push(currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
      currentTime.setMinutes(currentTime.getMinutes() + 15); 
    }
    return times;
  };
  

  const times = generateTimes();
  const [selectedTime, setSelectedTime] = useState('');

  const email = Cookies.get("username");
  const password = Cookies.get("userpass");

  if (!email || !password) {
      console.error("User is not logged in. Missing cookies.");
      return;
  }

  const handleClick = (time) => {
    setSelectedTime(time);

    fetch('http://127.0.0.1:5000/api/update-lunch-time', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        email: email,
        password: password,
        lunch_time: time
      }),
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
    <Container className="d-flex justify-content-center align-items-center vh-100"> 
      <Row>
        <Col xs={12} md={6}>
          <div className="p-3 scrollable-container"> 
            {times.map((time, index) => (
              <Button 
                key={index} 
                variant="purple" 
                className={`mb-3 w-100 ${selectedTime === time ? 'active' : ''}`} 
                onClick={() => handleClick(time)}
              >
                {time}
              </Button>
            ))}
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default TimeSelector;
