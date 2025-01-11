import { Link } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import './Login/Login.css';
import Login from './Login/Login.jsx';

function Signup() {
  return (
    <div className="login-container">
      <Form className="login-form">
      <h2 className="login-title">Sign Up</h2>
      <p className="login-subtitle">Find friends today!</p>
        <Form.Group className="mb-3" controlId="formGroupEmail">
          <Form.Label className="form-label">Email: </Form.Label>
          <Form.Control 
            type="email" 
            placeholder="Enter your email"
            className="form-input"
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label className="form-label">Password: </Form.Label>
          <Form.Control 
            type="password" 
            placeholder="Create a password"
            className="form-input"
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGroupConfirmPassword">
          <Form.Label className="form-label">Confirm Password: </Form.Label>
          <Form.Control 
            type="password" 
            placeholder="Confirm your password"
            className="form-input"
          />
        </Form.Group>

        <div className="interests-section">
          <h3 className="interests-title">Your Interests</h3>
          <div className="interests-container">
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="movies"
                label="Movies"
                className="interest-checkbox"
              />
            </div>
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="books"
                label="Books"
                className="interest-checkbox"
              />
            </div>
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="food"
                label="Food"
                className="interest-checkbox"
              />
            </div>
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="music"
                label="Music"
                className="interest-checkbox"
              />
            </div>
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="sports"
                label="Sports"
                className="interest-checkbox"
              />
            </div>
            <div className="interest-item">
              <Form.Check 
                type="checkbox"
                id="travel"
                label="Travel"
                className="interest-checkbox"
              />
            </div>
          </div>
        </div>

        <Form.Group className="mb-4">
          <label className="bio-label">Tell us about yourself</label>
          <textarea
            className="bio-textarea"
            placeholder="Share your interests, hobbies, or anything else you'd like others to know..."
            rows="3"
          />
        </Form.Group>

        <Button 
          variant="primary" 
          type="submit" 
          className="submit-button">
          Sign Up
        </Button>

        <div className="login-footer">
          <p>
            Already have an account?{" "}
            <a href="login" className="sign-up">
              Login
            </a>
          </p>
        </div>
      </Form>
    </div>
  );
}

export default Signup;
