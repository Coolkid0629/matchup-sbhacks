import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import './Signup.css';

function BasicExample() {
  return (
    <Container className="mt-5 d-flex flex-column align-items-center signup-container">
      <h1 className="mb-5 signup-title">
        SIGNUP
      </h1>
      <Form className="signup-form">
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

        <Button 
          variant="primary" 
          type="submit" 
          className="w-100 submit-button mt-4">
          Sign Up
        </Button>
      </Form>
    </Container>
  );
}

export default BasicExample;