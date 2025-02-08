"use client"; // Required for Next.js App Router (app directory)

import React, { useRef, useState, useEffect } from "react";
import axios from "axios";

const FaceAuth = ({ isLogin }) => {
  const videoRef = useRef(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing webcam:", error);
      }
    };

    startVideo();
  }, []);

  const captureImage = async () => {
    const video = videoRef.current;
    if (!video) return;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    const imageBase64 = canvas.toDataURL("image/jpeg").split(",")[1];

    const endpoint = isLogin ? "/login" : "/register";
    const payload = isLogin
      ? { image: imageBase64 }
      : { username: "test_user", image: imageBase64 };

    try {
      const res = await axios.post(`http://localhost:5000${endpoint}`, payload, {
        headers: { "Content-Type": "application/json" },
      });
      setMessage(res.data.message);
    } catch (error) {
      console.error("Request failed:", error);
      setMessage(error.response?.data?.error || "Something went wrong");
    }
  };

  return (
    <div className="m-auto flex flex-col gap-2 w-full">
      <video className="m-auto border-2 border-black rounded-lg" ref={videoRef} autoPlay width="300" height="200"></video>
      <button className=" w-fit m-auto p-4 rounded-xl bg-green-200" onClick={captureImage}>{isLogin ? "Login" : "Register"}</button>
      <p>{message}</p>
    </div>
  );
};

export default FaceAuth;
