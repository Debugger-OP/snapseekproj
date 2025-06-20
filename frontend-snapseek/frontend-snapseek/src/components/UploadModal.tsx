"use client";

import React, { useState } from "react";
import api from "@/lib/api";

const UploadModal = ({ onClose }: { onClose: () => void }) => {
  const [image, setImage] = useState<File | null>(null);
  const [description, setDescription] = useState("");

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
      // Optional: auto-fill description from filename
      setDescription(e.target.files[0].name);
    }
  };

  const handleUpload = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image);
    formData.append("description", description);

    try {
      const res = await api.post("/upload/", formData);
      console.log("✅ Uploaded:", res.data);
      onClose(); // close modal
    } catch (err) {
      console.error("❌ Upload failed:", err);
    }
  };

  return (
    <div style={{ background: "white", padding: "1rem", zIndex: 50 }}>
      <input type="file" onChange={handleImageChange} />
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
      />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default UploadModal;
