import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:5000/login";
    setTimeout(() => {
      navigate("/display");
    }, 3000); // Adjust the timeout duration as needed
  };

  return (
    <div className="bg-black h-screen flex justify-center items-center">
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="bg-gradient-to-r from-green-400 to-green-100  transition ease-in-out delay-150  hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
        onClick={handleLogin}
      >
        Login with Spotify
      </motion.button>
    </div>
  );
}
