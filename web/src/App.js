import * as React from "react";

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NoMatch from "./pages/NoMatch"
import Signup from "./pages/Signup"
import Home from "./pages/Home"
import Login from "./pages/Login";

function App() {
  return(
    <Router>
        <div className="flex-column justify-flex-start min-100-vh">
          
          <div className="container p-5">
            <Routes>
                  <Route
                    path="/"
                    element={<Home />}
                  />
                  <Route
                    path="/login"
                    element={<Login />}
                  />
                  <Route
                    path="/signup"
                    element={<Signup />}
                  />
                  <Route
                        path="*"
                        element={<NoMatch />}
                  />
              </Routes>
            </div>
        </div>
      </Router>
  )
}

export default App;
