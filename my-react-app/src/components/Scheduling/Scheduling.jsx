import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './Scheduling.css';


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
  const navigate = useNavigate();

  if (!email || !password) {
      console.error("User is not logged in. Missing cookies.");
      navigate("/login");
      return;
  }

  const navigate = useNavigate();

  const handleClick = (time) => {
    setSelectedTime(time);

    fetch('http://127.0.0.1:5000/api/update-lunch-time', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, time }),
    })
    .then(() => {
      navigate('/waiting');
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