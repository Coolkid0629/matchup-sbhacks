import React, { useState } from "react";
import { Link } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import '../components/Login/Login.css';
import { Navigate, useNavigate } from "react-router-dom";

function Signup() {
  // State to store form data
  const [email, setEmail] = useState("");
  const [name, setName] = useState("")
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [bio, setBio] = useState("");
  const [interests, setInterests] = useState({
    movies: false,
    books: false,
    food: false,
    music: false,
    sports: false,
    travel: false
  });
  const navigate = useNavigate();

  // Handle checkbox change for interests
  const handleInterestChange = (event) => {
    const { id, checked } = event.target;
    setInterests((prevInterests) => ({
      ...prevInterests,
      [id]: checked
    }));
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the form from refreshing the page
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const signupData = {
      name: name,
      email: email,
      password: password,
      bio: bio,
      interests: Object.keys(interests).filter((interest) => interests[interest]).join(", "),
      profile_picture: "test"
    };
    console.log(signupData)

    try {
      const response = await fetch("http://127.0.0.1:5000/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signupData), // Send the signup data
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Sign-up successful:", data);
        navigate("/login");
        // Handle successful sign-up (e.g., redirect to login page)
      } else {
        console.error("Sign-up failed:", response.status);
        // Handle failed sign-up attempt (e.g., show an error message)
      }
    } catch (error) {
      console.error("Error during sign-up request:", error);
      // Handle error (e.g., show an error message)
    }
  };

  return (
    <div className="login-container">
      <Form className="login-form" onSubmit={handleSubmit}>
        <h2 className="login-title">Sign Up</h2>
        <p className="login-subtitle">Find friends today!</p>
        {/* Name input */}
        <Form.Group className="mb-3" controlId="formGroupName">
          <Form.Label className="form-label">Name: </Form.Label>
          <Form.Control
            type="name"
            placeholder="Enter your name"
            className="form-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </Form.Group>

        {/* Email input */}
        <Form.Group className="mb-3" controlId="formGroupEmail">
          <Form.Label className="form-label">Email: </Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter your email"
            className="form-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>

        {/* Password input */}
        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label className="form-label">Password: </Form.Label>
          <Form.Control
            type="password"
            placeholder="Create a password"
            className="form-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>

        {/* Confirm Password input */}
        <Form.Group className="mb-3" controlId="formGroupConfirmPassword">
          <Form.Label className="form-label">Confirm Password: </Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm your password"
            className="form-input"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </Form.Group>

        {/* Interests checkboxes */}
        <div className="interests-section">
          <h3 className="interests-title">Your Interests</h3>
          <div className="interests-container">
            {["movies", "books", "food", "music", "sports", "travel"].map((interest) => (
              <div className="interest-item" key={interest}>
                <Form.Check
                  type="checkbox"
                  id={interest}
                  label={interest.charAt(0).toUpperCase() + interest.slice(1)}
                  className="interest-checkbox"
                  checked={interests[interest]}
                  onChange={handleInterestChange}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Bio input */}
        <Form.Group className="mb-4">
          <label className="bio-label">Tell us about yourself</label>
          <textarea
            className="bio-textarea"
            placeholder="Share your interests, hobbies, or anything else you'd like others to know..."
            rows="3"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          />
        </Form.Group>

        {/* Submit button */}
        <Button variant="primary" /*type="submit" className="submit-button"*/ onClick={handleSubmit}> 
          Sign Up
        </Button>

        {/* Footer with login link */}
        <div className="login-footer">
          <p>
            Already have an account?{" "}
            <Link to="/login" className="sign-up">
              Login
            </Link>
          </p>
        </div>
      </Form>
    </div>
  );
}

export default Signup;
