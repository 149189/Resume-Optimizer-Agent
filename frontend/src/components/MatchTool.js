import React, { useState } from "react";
import axios from "axios";
import { API_BASE } from "../config";

function MatchTool() {
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onMatch = async () => {
    if (!resumeText.trim() || !jobText.trim()) {
      alert("Please provide both resume and job description text.");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/match/`, {
        resume_text: resumeText,
        job_text: jobText,
      });
      setResult(res.data);
    } catch (e) {
      console.error(e);
      alert("Match request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Job & Resume Semantic Match</h2>
      <div className="row">
        <div>
          <h4>Resume Text</h4>
          <textarea className="textarea" rows={8} value={resumeText} onChange={(e) => setResumeText(e.target.value)} />
        </div>
        <div>
          <h4>Job Description</h4>
          <textarea className="textarea" rows={8} value={jobText} onChange={(e) => setJobText(e.target.value)} />
        </div>
      </div>
      <button className="btn" onClick={onMatch} disabled={loading} style={{ marginTop: 12 }}>
        {loading ? "Matching..." : "Compute Match"}
      </button>
      {result && (
        <div style={{ marginTop: 16 }}>
          <div><strong>Score:</strong> {result.score}</div>
          <div style={{ display: "flex", gap: 20, marginTop: 10 }}>
            <div>
              <strong>Top Resume Terms</strong>
              <ul>
                {result.top_resume_terms?.map((t, i) => (
                  <li key={`rt-${i}`}>{t}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Top Job Terms</strong>
              <ul>
                {result.top_job_terms?.map((t, i) => (
                  <li key={`jt-${i}`}>{t}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MatchTool;
