import React, { useState } from "react";
import axios from "axios";

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
    <div style={{ padding: "20px" }}>
      <h2>Upload Resume (PDF/DOCX)</h2>
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Extract Text</button>
      <h3>Extracted Text:</h3>
      <textarea rows="15" cols="80" value={extractedText} readOnly />
    </div>
  );
}

export default FileUpload;
