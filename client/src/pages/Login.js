import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();
  const [imageUrl, setImageUrl] = useState(null);
  const [emotion, setEmotion] = useState(null);

  useEffect(() => {
    // Retrieve the image URL and emotion from local storage when the component mounts
    const storedImageUrl = localStorage.getItem("uploadedImageUrl");
    let storedEmotion = localStorage.getItem("userEmotion");
    if (storedImageUrl) {
      setImageUrl(storedImageUrl);
    }
    if (storedEmotion) {
      // Convert emotion to uppercase
      storedEmotion = storedEmotion.toUpperCase();
      setEmotion(storedEmotion);
    }
  }, []);

  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:5000/login";
    setTimeout(() => {
      navigate("/display");
    }, 3000); // Adjust the timeout duration as needed
  };

  return (
    <div className="bg-black h-screen flex flex-col justify-center items-center p-4">
      <div className="flex flex-col items-center sm:flex-row sm:items-center sm:justify-center mb-4">
        {imageUrl && (
          <div className="sm:mr-4 mb-4 sm:mb-0">
            <img
              src={imageUrl}
              alt="Uploaded"
              className="w-20  h-24 rounded-lg"
            />
          </div>
        )}
        {emotion && (
          <div className="text-white text-center sm:text-left">
            <p className="text-lg font-semibold">
              Your current emotional status according to our system is
            </p>
            <p className="text-2xl font-bold">{emotion}</p>
          </div>
        )}
      </div>
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
        onClick={handleLogin}
      >
        Login with Spotify
      </motion.button>
    </div>
  );
}
