import React from 'react'
import { Button, Col, Container, Form, Row } from 'react-bootstrap'
import Cards from '../components/Cards'
import Signin from "./GoogleAuth";

const Homescreen = () => {
    return (
        <div>
            <Container>
                <Row>
                    <Col>
                        <h1>Welcome to the Home Screen</h1>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Signin />
                    </Col>
                </Row>
                <Row>
                    <Col>
                    <Form>
  <Form.Group className="mb-3" controlId="formBasicEmail">
    <Form.Label>Email address</Form.Label>
    <Form.Control type="email" placeholder="Enter email" />
    <Form.Text className="text-muted">
      We'll never share your email with anyone else.
    </Form.Text>
  </Form.Group>

  <Form.Group className="mb-3" controlId="formBasicPassword">
    <Form.Label>Password</Form.Label>
    <Form.Control type="password" placeholder="Password" />
  </Form.Group>
  <Form.Group className="mb-3" controlId="formBasicCheckbox">
    <Form.Check type="checkbox" label="Check me out" />
  </Form.Group>
  <Button variant="primary" type="submit">
    Submit
  </Button>
</Form>
                    </Col>
                </Row>
            </Container>

           

         
        </div>
    )
}

export default Homescreen
