"use client";
import { useState, useRef, useEffect } from "react";

type Message = {
  role: "user" | "ai";
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.response ?? "No response." },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "Could not reach the server. Is your backend running?" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <main className="rain-bg">
      <Rain />
      <div className="overlay" />

      <div className="chat-shell">
        <header className="chat-header">
          <span className="dot" />
          <h1>Study Assistant</h1>
        </header>

        <div className="messages">
          {messages.length === 0 && (
            <p className="empty">Ask me anything about your studies.</p>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`bubble-wrap ${m.role}`}>
              <div className={`bubble ${m.role}`}>{m.text}</div>
            </div>
          ))}
          {loading && (
            <div className="bubble-wrap ai">
              <div className="bubble ai typing">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="input-row">
          <textarea
            rows={1}
            placeholder="Ask your study assistant…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>
            Send
          </button>
        </div>
      </div>
    </main>
  );
}

function Rain() {
  const drops = Array.from({ length: 60 }, (_, i) => ({
    left: `${Math.random() * 100}%`,
    delay: `${Math.random() * 3}s`,
    duration: `${0.6 + Math.random() * 0.8}s`,
    opacity: 0.15 + Math.random() * 0.3,
    key: i,
  }));

  return (
    <div className="rain" aria-hidden="true">
      {drops.map((d) => (
        <div
          key={d.key}
          className="drop"
          style={{
            left: d.left,
            animationDelay: d.delay,
            animationDuration: d.duration,
            opacity: d.opacity,
          }}
        />
      ))}
    </div>
  );
}
