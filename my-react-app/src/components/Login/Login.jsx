import React from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import "./Login.css";

function Login() {
  return (
    <div className="login-container">
      <Form className="login-form">
        <h2 className="login-title">Welcome Back</h2>
        <p className="login-subtitle">Please login to your account</p>
        <Form.Group className="mb-3" controlId="formGroupUsername">
          <Form.Label className="form-label">Username: </Form.Label>
          <Form.Control
            className="form-input"
            type="text"
            placeholder="Enter your username"
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label className="form-label">Password: </Form.Label>
          <Form.Control
            className="form-input"
            type="password"
            placeholder="Enter your password"
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
