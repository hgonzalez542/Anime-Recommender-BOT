import { useState, useEffect, useRef } from "react";
import "./styles.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);

  const [recommendations, setRecommendations] = useState({
    new_gen: [],
    old_gen: []
  });

  const chatRef = useRef(null);

  // AUTO SCROLL
  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, recommendations]);

  const handleSubmit = async () => {
    if (!prompt) return;

    const newMessages = [...messages, { type: "user", text: prompt }];
    setMessages(newMessages);

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await res.json();

    setMessages([
      ...newMessages,
      { type: "ai", text: data.assistant_message }
    ]);

    setRecommendations({
      new_gen: data.new_gen,
      old_gen: data.old_gen
    });

    setPrompt("");
  };

  return (
    <div className="app-container">

      {/* HERO */}
      <div className="hero">
        <h1>Anime AI Assitant</h1>
        <p>Find your next anime instantly</p>

        <div className="top-bar">
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="Try: 'dark anime' or 'like attack on titan'"
          />
          <button onClick={handleSubmit}>Search</button>
        </div>
      </div>

      <div className="content">

        {/* LEFT SIDE — CHAT */}
        <div className="chat-section">

          {messages.length === 0 && (
            <div className="chat-bubble ai">
              Ask for anime recommendations...
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.type}`}>
              {msg.text}
            </div>
          ))}

          
          {recommendations.new_gen.length > 0 && (
            <div className="chat-bubble ai recommendation-bubble">
              <h2>🔥New Gen Anime</h2>

              {recommendations.new_gen.map((anime, i) => (
                <AnimeCard key={i} anime={anime} />
              ))}
            </div>
          )}

          
          {recommendations.old_gen.length > 0 && (
            <div className="chat-bubble ai recommendation-bubble">
              <h2>📺 Classic Anime</h2>

              {recommendations.old_gen.map((anime, i) => (
                <AnimeCard key={i} anime={anime} />
              ))}
            </div>
          )}

          <div ref={chatRef}></div>
        </div>

      </div>
    </div>
  );
}

/* ANIME CARD COMPONENT */
function AnimeCard({ anime }) {
  return (
    <div className="anime-card">

      {anime.image && (
        <img src={anime.image} alt={anime.title} />
      )}

      <div className="anime-info">
        <h3>{anime.title}</h3>

        {/* GENRES */}
        <div className="tags">
          {anime.genres?.map((g, i) => (
            <span key={i}>{g}</span>
          ))}
        </div>

        <p>{anime.description}</p>

        <div className="meta">
          ⭐ {anime.rating} • {anime.year}
        </div>

        <small>{anime.reason}</small>
      </div>
    </div>
  );
}

export default App;