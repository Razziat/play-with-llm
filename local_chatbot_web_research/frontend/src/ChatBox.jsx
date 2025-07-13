// frontend/ChatBox.jsx
import React, { useState, useRef, useEffect } from "react";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [useSearch, setUseSearch] = useState(true);
  const chatRef = useRef(null);

  /* ----- Scroll bas automatique ----- */
  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function send() {
    if (!input.trim()) return;
    setMessages((m) => [...m, { role: "user", text: input }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, use_search: useSearch }),
      });
      const data = await res.json();
      setMessages((m) => [
        ...m,
        { role: "bot", text: data.reply, sources: data.sources ?? [] },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "bot", text: "Erreur serveur : " + err.message, sources: [] },
      ]);
    }
    setInput("");
  }

  return (
    <div style={styles.container}>
      {/* -------- Fenêtre de dialogue -------- */}
      <div ref={chatRef} style={styles.chatWindow}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.bubble,
              ...(m.role === "user" ? styles.user : styles.bot),
            }}
          >
            {m.text}
            {m.role === "bot" && m.sources?.length > 0 && (
              <ul style={styles.sources}>
                {m.sources.map((s, k) => (
                  <li key={k}>
                    <a href={s.url} target="_blank" rel="noreferrer">
                      {s.title || s.url}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      {/* -------- Zone d'input -------- */}
      <div style={styles.inputRow}>
        <input
          style={styles.input}
          value={input}
          placeholder="Votre message…"
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button style={styles.button} onClick={send}>
          Envoyer
        </button>
      </div>

      <label style={styles.checkbox}>
        <input
          type="checkbox"
          checked={useSearch}
          onChange={(e) => setUseSearch(e.target.checked)}
        />
        Activer la recherche Web
      </label>
    </div>
  );
}

/* -------- Styles -------- */
const styles = {
  container: {
    /* largeur fluide jusqu’à 700 px, puis centrée */
    width: "100%",
    maxWidth: 700,
    margin: "0 auto",
    /* occupe toute la hauteur écran moins un petit padding */
    height: "calc(100vh - 32px)",
    display: "flex",
    flexDirection: "column",
  },
  chatWindow: {
    flex: 1,
    overflowY: "auto",
    border: "1px solid #ddd",
    borderRadius: 8,
    padding: "0.75rem",
    background: "#fafafa",
  },
  bubble: {
    maxWidth: "85%",
    margin: "0.4rem 0",
    padding: "0.6rem 0.8rem",
    borderRadius: 14,
    whiteSpace: "pre-wrap",
    lineHeight: 1.35,
    fontSize: 14,
  },
  user: { alignSelf: "flex-end", background: "#d1e8ff", marginLeft: "auto" },
  bot: { alignSelf: "flex-start", background: "#e8e8e8" },
  sources: { marginTop: 6, paddingLeft: 18, fontSize: 13 },
  inputRow: { display: "flex", gap: 8, marginTop: 8 },
  input: { flex: 1, padding: "0.5rem" },
  button: { padding: "0 1rem" },
  checkbox: { display: "inline-flex", gap: 6, marginTop: 6, fontSize: 14 },
};
