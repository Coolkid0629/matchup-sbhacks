import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";
import { Navigate, useNavigate } from "react-router-dom";
import Cookies from "js-cookie"; 

import "./Login.css";

function Login() {
  // State to store username and password
  const [email, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginFailed, setLoginFailed] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Handle the form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the form from refreshing the page

    const loginData = {
      email: email,
      password: password,
    };
    console.log(loginData);

    try {
      // Make the POST request to the server
      const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginData), // Send username and password in the body
      });

      // Handle the response from the server
      if (response.ok) {
        const data = await response.json();
        Cookies.set("username", data.email);
        Cookies.set("userpass", data.password);
        navigate("/");
        // You can redirect or update the UI based on the response here
      } else {
        const errorData = await response.json();
        console.log(errorData);
        setError(errorData.message || "Login failed. Please try again.");
        setLoginFailed(true);
      }
    } catch (error) {
      console.error("Error during login request:", error);
      setError("Network error. Please try again later.");
      setLoginFailed(true);
    }
  };

  return (
    <div className="login-container">
      {loginFailed && (
        <Alert variant="danger" className="mb-3" onClose={() => setLoginFailed(false)} dismissible>
          {error}
        </Alert>
      )}
      <Form className="login-form" onSubmit={handleSubmit}>
        <h2 className="login-title">Welcome Back</h2>
        <p className="login-subtitle">Please login to your account</p>
        <Form.Group className="mb-3" controlId="formGroupUsername">
          <Form.Label className="form-label">Username: </Form.Label>
          <Form.Control
            className="form-input"
            type="text"
            placeholder="Enter your username"
            value={email}
            onChange={(e) => setUsername(e.target.value)} // Update state on change
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label className="form-label">Password: </Form.Label>
          <Form.Control
            className="form-input"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Update state on change
          />
        </Form.Group>
        <Button className="submit-button" type="submit">
          Login
        </Button>
        <div className="login-footer">
          <a href="#forgot-password" className="forgot-password">
            Forgot Password?
          </a>
          <p>
            Don’t have an account?{" "}
            <a href="/signup" className="sign-up">
              Sign Up
            </a>
          </p>
        </div>
      </Form>
    </div>
  );
}

export default Login;
