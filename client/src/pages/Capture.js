import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { AnimatePresence } from "framer-motion";
import { IoCameraSharp } from "react-icons/io5";

function Capture() {
  const [isExiting, setIsExiting] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (isCameraOn) {
      const startVideo = async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
          });
          videoRef.current.srcObject = stream;
        } catch (err) {
          console.error("Error accessing webcam: ", err);
        }
      };
      startVideo();
      return () => {
        if (videoRef.current && videoRef.current.srcObject) {
          const tracks = videoRef.current.srcObject.getTracks();
          tracks.forEach((track) => track.stop());
        }
      };
    }
  }, [isCameraOn]);

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

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      setCapturedImage(blob);
      setIsCameraOn(false); // Turn off the camera preview after capturing the image
    }, "image/png");
  };

  const handleUpload = async () => {
    const fileToUpload = capturedImage || selectedFile;
    if (!fileToUpload) {
      alert("Please select or capture a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileToUpload);

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
                {/* Show the camera button only if the camera is off and no image is captured */}
                {!capturedImage && !isCameraOn && (
                  <button
                    className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
                    onClick={() => setIsCameraOn(true)}
                  >
                    <IoCameraSharp size={30} />
                  </button>
                )}
                {isCameraOn && (
                  <video
                    ref={videoRef}
                    style={{
                      display: "block",
                      marginTop: "20px",
                      width: "100%",
                      maxWidth: "500px",
                    }}
                    autoPlay
                  />
                )}
                <canvas ref={canvasRef} style={{ display: "none" }} />
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
                {(selectedFile || capturedImage) && (
                  <button
                    className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto ml-2"
                    onClick={handleUpload}
                  >
                    Submit
                  </button>
                )}
                {isCameraOn && !capturedImage && (
                  <button
                    className="bg-gradient-to-r from-green-400 to-green-100 transition ease-in-out delay-150 hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto ml-2"
                    onClick={captureImage}
                  >
                    Capture
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
