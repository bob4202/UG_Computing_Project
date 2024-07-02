import React from "react";
import Home from "../pages/Home";
import Capture from "../pages/Capture";
import Login from "../pages/Login";
import Display from "../pages/Display";
import { Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence } from "framer-motion";

function AnimatedRoute() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/capture" element={<Capture />} />
        <Route path="/login" element={<Login />} />
        <Route path="/display" element={<Display />} />
      </Routes>
    </AnimatePresence>
  );
}

export default AnimatedRoute;
