import React, { useState } from "react";
import axios from "axios";
import { API_BASE } from "../config";

function SemanticSearch() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loadingIngest, setLoadingIngest] = useState(false);
  const [loadingSearch, setLoadingSearch] = useState(false);

  const ingest = async () => {
    if (!text.trim()) {
      alert("Provide text to ingest");
      return;
    }
    setLoadingIngest(true);
    try {
      const res = await axios.post(`${API_BASE}/api/ingest/`, { title, text });
      alert(`Ingested with id ${res.data.id}`);
      setTitle("");
      setText("");
    } catch (e) {
      console.error(e);
      alert("Ingest failed");
    } finally {
      setLoadingIngest(false);
    }
  };

  const search = async () => {
    if (!query.trim()) {
      alert("Provide a query");
      return;
    }
    setLoadingSearch(true);
    try {
      const res = await axios.post(`${API_BASE}/api/search-match/`, { query, top_k: 5 });
      setResults(res.data.results || []);
    } catch (e) {
      console.error(e);
      alert("Search failed");
    } finally {
      setLoadingSearch(false);
    }
  };

  return (
    <div>
      <h2>Semantic Ingest & Search</h2>
      <div className="row" style={{ marginBottom: 12 }}>
        <div>
          <h4>Ingest Document</h4>
          <input
            type="text"
            placeholder="Title (optional)"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input"
            style={{ display: "block", marginBottom: 8 }}
          />
          <textarea
            rows={8}
            placeholder="Paste resume or JD text here"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="textarea"
          />
          <br />
          <button className="btn" onClick={ingest} disabled={loadingIngest}>
            {loadingIngest ? "Ingesting..." : "Ingest"}
          </button>
        </div>
        <div>
          <h4>Search</h4>
          <textarea
            rows={8}
            placeholder="Query text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="textarea"
          />
          <br />
          <button className="btn" onClick={search} disabled={loadingSearch}>
            {loadingSearch ? "Searching..." : "Search"}
          </button>
        </div>
      </div>
      {!!results.length && (
        <div>
          <strong>Top Results</strong>
          <ol>
            {results.map((r) => (
              <li key={r.id}>
                <span style={{ marginRight: 8 }}>{r.title || `Doc ${r.id}`}</span>
                <span>score: {r.score.toFixed(4)}</span>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default SemanticSearch;
