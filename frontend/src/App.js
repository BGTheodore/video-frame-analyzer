import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);       // Vidéo uploadée
  const [frames, setFrames] = useState([]);     // Frames analysées
  const [rawJson, setRawJson] = useState(null); // JSON complet pour affichage
  const containerRef = useRef(null);            // Scroll automatique

  // Scroll automatique vers le bas quand frames changent
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [frames]);

  // --- Upload + Analyse ---
  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      setFrames(data.results);  // Sauvegarde frames dans state
      setRawJson(data);         // Sauvegarde JSON complet
    } catch (error) {
      console.error("Erreur API:", error);
    }
  };

  return (
    <div className="App" style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Video Frame Analyzer</h1>

      {/* Upload vidéo */}
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} style={{ marginLeft: 10 }}>
        Analyze
      </button>

      {/* Container scrollable */}
      <div
        ref={containerRef}
        className="frames-container"
      >
        {/* Grille des frames */}
        <div className="frames-grid">
          {frames.map((frame) => (
            <div key={frame.second} className="frame-card">
              <div>
                <strong>Second: {frame.second}</strong>
              </div>
              <div>Brightness: {frame.brightness}</div>
              <img
                src={`http://127.0.0.1:8000${frame.frame_url}`}
                alt={`Frame ${frame.second}`}
              />
            </div>
          ))}
        </div>
      </div>

      {/* JSON complet */}
      {rawJson && (
        <div style={{ marginTop: 20 }}>
          <h2>JSON Response</h2>
          <pre
            style={{
              background: "#f0f0f0",
              padding: 10,
              borderRadius: 6,
              overflowX: "auto",
              maxHeight: "300px"
            }}
          >
            {JSON.stringify(rawJson, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
