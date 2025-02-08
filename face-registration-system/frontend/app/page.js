import Image from "next/image";
import FaceAuth from "./components/FaceAuth";

export default function Home() {
  return (
    <div>
      <FaceAuth isLogin={true}/>
    </div>
  );
}
