import React from 'react'
import { Col, Container, Row } from 'react-bootstrap'
import Cards from '../components/Cards'


const Homescreen = () => {
    return (
        <div>
           <Container>
               <Row >
               {["Project1","Project2","Project 3","Project11","Project21","Project 31","Project12","Project22","Project 32","Project12","Project22","Project 32"].map((value,index) => 
                <Col lg={3}>
                        <Cards project={value} key={index}/>
                  </Col>
               )}
                 
                  
               </Row>
           </Container>
        </div>
    )
}

export default Homescreen
