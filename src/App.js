import React from "react";
import { Container } from "react-bootstrap";
import Header from "./components/Header";
import Homescreen from "./Screens/Homescreen";
import AirbnbDashboard from "./Screens/AirbnbDashboard";
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
          <Route path="/airbnb-analysis">
            <AirbnbDashboard />
          </Route>
        </Container>
      </main>
    </>
  );
};

export default App;

