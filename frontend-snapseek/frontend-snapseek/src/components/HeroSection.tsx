"use client";

import React, { useState } from "react";
import UploadModal from "./UploadModal";

const HeroSection = () => {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div>
      <h1>Snapseek</h1>
      <button onClick={() => setShowUpload(true)}>Upload Image</button>
      {showUpload && <UploadModal onClose={() => setShowUpload(false)} />}
    </div>
  );
};

export default HeroSection;
