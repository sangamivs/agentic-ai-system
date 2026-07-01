import { useState, useCallback } from "react";

export function useAgentChat(sessionId) {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = useCallback(
    async (text) => {
      const userMsg = {
        id: Date.now(),
        role: "user",
        content: text,
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsStreaming(true);

      try {
        const response = await fetch("http://localhost:8000/api/v1/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: text,
            session_id: sessionId,
          }),
        });

        const data = await response.json();

        const botMsg = {
          id: Date.now() + 1,
          role: "assistant",
          content: data.answer || data.detail || "No response",
        };

        setMessages((prev) => [...prev, botMsg]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: "assistant",
            content: "Error connecting to backend.",
          },
        ]);
      }

      setIsStreaming(false);
    },
    [sessionId]
  );

  return {
    messages,
    sendMessage,
    isStreaming,
  };
}