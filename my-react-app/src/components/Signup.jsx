import { Link } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import './Login/Login.css';

function Signup() {
  return (
    <div className="login-container">
      <Form className="login-form">
        <h2 className="login-title">SIGNUP</h2>
        
        <Form.Group className="mb-4" controlId="formBasicEmail">
          <Form.Control 
            type="email" 
            placeholder="Enter email"
            className="form-input"
          />
        </Form.Group>

        <Form.Group className="mb-4" controlId="formBasicPassword">
          <Form.Control 
            type="password" 
            placeholder="Password"
            className="form-input"
          />
        </Form.Group>

        <Form.Group className="mb-4" controlId="formBasicConfirmPassword">
          <Form.Control 
            type="password" 
            placeholder="Confirm Password"
            className="form-input"
          />
        </Form.Group>

        <Button 
          variant="primary" 
          type="submit" 
          className="submit-button w-100">
          Sign Up
        </Button>

        <div className="text-center mt-3">
          <p>
            Already have an account?{" "}
            <a href="#login" className="sign-up">
              Login
            </a>
          </p>
        </div>
      </Form>
    </div>
  );
}

export default Signup;