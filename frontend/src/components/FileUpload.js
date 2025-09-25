import React, { useState } from "react";
import axios from "axios";
import { API_BASE } from "../config";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload-resume/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setExtractedText(res.data.text);
    } catch (error) {
      console.error(error);
      alert("Upload failed!");
    }
  };

  return (
    <div>
      <h2>Upload Resume (PDF/DOCX)</h2>
      <div className="row">
        <input className="input" type="file" accept=".pdf,.docx" onChange={handleFileChange} />
        <button className="btn" onClick={handleUpload}>Upload & Extract Text</button>
      </div>
      <h3>Extracted Text:</h3>
      <textarea className="textarea" rows="10" value={extractedText} readOnly />
    </div>
  );
}

export default FileUpload;
