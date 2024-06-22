import React from "react";
import { motion } from "framer-motion";
import { AnimatePresence } from "framer-motion";

export default function Login() {
  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:5000/login";
  };

  return (
    <div className="bg-black h-screen flex justify-center items-center">
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        onClick={handleLogin}
      >
        Login with Spotify
      </motion.button>
    </div>
  );
}
