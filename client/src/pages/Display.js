import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
function Display() {
  // const navigate = useNavigate();

  // const handleLogout = async () => {
  //   await fetch("http://127.0.0.1:5000/logout", {
  //     method: "GET",
  //     credentials: "include",
  //   });
  //   navigate("/login");
  // };
  return (
    <div className="bg-black h-screen flex justify-center items-center">
      <div className="flex flex-col justify-center gap-4">
        <div className="flex items-center justify-center">
          <h1 className="text-white font-roboto text-2xl">
            The suggested Tracks are successfully added to your new playlist
          </h1>
        </div>
        <div className="flex items-center justify-center">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="bg-gradient-to-r from-green-400 to-green-100  transition ease-in-out delay-150  hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
            // onClick={handleLogout}
          >
            End Session
          </motion.button>
        </div>
      </div>
    </div>
  );
}
export default Display;
