import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();
  const [imageUrl, setImageUrl] = useState(null);
  const [emotion, setEmotion] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch the emotion from the server
    const fetchEmotion = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get_emotion");
        const data = await response.json();
        if (data.emotion) {
          // Convert emotion to uppercase
          setEmotion(data.emotion.toUpperCase());
        }
      } catch (error) {
        console.error("Error fetching emotion:", error);
      }
    };

    fetchEmotion();

    // Retrieve the image URL from local storage
    const storedImageUrl = localStorage.getItem("uploadedImageUrl");
    if (storedImageUrl) {
      setImageUrl(storedImageUrl);
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
      {loading ? ( // Show spinner while loading
        <l-quantum size="55" speed="1.8" color="blue"></l-quantum>
      ) : (
        <>
          <div className="flex flex-col items-center sm:flex-row sm:items-center sm:justify-center mb-4">
            {imageUrl && (
              <div className="sm:mr-4 mb-4 sm:mb-0">
                <img
                  src={imageUrl}
                  alt="Uploaded"
                  className="w-20 h-24 rounded-lg"
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
        </>
      )}
    </div>
  );
}
