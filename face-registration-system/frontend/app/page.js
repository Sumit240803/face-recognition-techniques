'use client'
import { useState } from "react";
import FaceAuth from "./components/FaceAuth";

export default function Home() {
  const[login , setLogin ] = useState(false);
  return (
    <div className="flex flex-col items-center gap-2 bg-gray-100 h-screen">
      <div className="text-center text-xl font-bold my-5">
        FACE RECOGNITION AUTHENTICATION
      </div>
      <div className="flex gap-2">

      <div className="bg-green-300 rounded-xl p-2"><button onClick={()=>setLogin(false)}>Register</button> </div>
      <div className="bg-blue-200 rounded-xl p-2"><button onClick={()=>setLogin(true)}>Login</button> </div>
      </div>
      <FaceAuth isLogin={login}/>
    </div>
  );
}

