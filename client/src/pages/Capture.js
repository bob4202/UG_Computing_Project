import React, { useState } from "react";
import { motion } from "framer-motion";
import { AnimatePresence } from "framer-motion";
import { IoCameraSharp } from "react-icons/io5";

function Capture() {
  const [isExiting, setIsExiting] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const goToHome = () => {
    setIsExiting(true);
    setTimeout(() => {
      window.location.href = "/";
    }, 500); // Delay to allow the exit animation to complete
  };

  const goToLogin = () => {
    setIsExiting(true);
    setTimeout(() => {
      window.location.href = "/login";
    }, 500);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (
      file &&
      ["image/png", "image/jpg", "image/jpeg", "image/svg+xml"].includes(
        file.type
      )
    ) {
      setSelectedFile(file);
    } else {
      alert("Please select a valid file type: png, jpg, jpeg, svg.");
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Upload Response:", data); // Log the response
        alert("File uploaded successfully!");
        localStorage.setItem("uploadedImageUrl", data.file_url); // Store the uploaded image URL in local storage
        goToLogin();
      } else {
        const errorData = await response.json();
        alert(`Failed to upload file: ${errorData.error}`);
      }
    } catch (error) {
      alert(`Error uploading file: ${error.message}`);
    }
  };

  return (
    <div className="bg-black h-dvh flex justify-center items-center">
      <AnimatePresence>
        {!isExiting && (
          <div className="flex flex-col justify-center gap-4">
            <motion.div
              variants={{
                hidden: {
                  opacity: 0,
                  y: -1300,
                },
                visible: {
                  opacity: 1,
                  y: 0,
                },
                exit: {
                  opacity: 0,
                  y: 1300, // Reverse the animation
                },
              }}
              initial="hidden"
              animate="visible"
              exit="exit"
              transition={{ duration: 1.5 }}
            >
              <div className="flex items-center justify-center">
                <button className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto">
                  <IoCameraSharp size={30} />
                </button>
              </div>
            </motion.div>
            <motion.div
              variants={{
                hidden: {
                  opacity: 0,
                  x: 1300,
                },
                visible: {
                  opacity: 1,
                  x: 0,
                },
                exit: {
                  opacity: 0,
                  x: -1300, // Reverse the animation
                },
              }}
              initial="hidden"
              animate="visible"
              exit="exit"
              transition={{ duration: 1.5 }}
            >
              <div className="flex items-center justify-center">
                <input
                  type="file"
                  accept=".png,.jpg,.jpeg,.svg"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                  id="upload-input"
                />
                <label htmlFor="upload-input">
                  <button
                    className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
                    onClick={() =>
                      document.getElementById("upload-input").click()
                    }
                  >
                    Upload
                  </button>
                </label>
                {selectedFile && (
                  <button
                    className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto ml-2"
                    onClick={handleUpload}
                  >
                    Submit
                  </button>
                )}
              </div>
            </motion.div>
            <motion.div
              variants={{
                hidden: {
                  opacity: 0,
                  x: -1300,
                },
                visible: {
                  opacity: 1,
                  x: 0,
                },
                exit: {
                  opacity: 0,
                  x: 1300, // Reverse the animation
                },
              }}
              initial="hidden"
              animate="visible"
              exit="exit"
              transition={{ duration: 1.5 }}
            >
              <div className="flex items-center justify-center">
                <button
                  className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
                  onClick={goToHome}
                >
                  Cancel
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default Capture;
