import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function Display() {
  const [playlistUrl, setPlaylistUrl] = useState(null);
  const navigate = useNavigate();

  const handleEndSession = async () => {
    window.open("http://127.0.0.1:5000/playlist", "_blank");
    navigate("/");
  };

  return (
    <div className="bg-black h-screen flex justify-center items-center">
      <div className="flex flex-col items-center gap-4">
        <h1 className="text-white font-roboto text-2xl mb-4">
          The suggested tracks are successfully added to your new playlist!
        </h1>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
          onClick={handleEndSession}
        >
          End Session
        </motion.button>
      </div>
    </div>
  );
}

export default Display;
