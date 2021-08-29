import React from "react";
import { Container } from "react-bootstrap";
import Header from "./components/Header";
import Homescreen from "./Screens/Homescreen";
import { Route } from "react-router-dom";


const App = () => {
  return (
    <>
      <Header />
      <main className="py-3">
        <Container>
          <Route path="/" exact>
            <Homescreen />
          </Route>
        </Container>
      </main>
    </>
  );
};

export default App;

