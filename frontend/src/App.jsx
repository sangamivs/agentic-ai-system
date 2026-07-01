import { useState, useRef, useEffect } from 'react';
import { useAgentChat } from './hooks/useAgentChat';
import { ChatMessage } from './components/ChatMessage';
import { Send } from 'lucide-react';

export default function App() {
  const sessionId = 'session-' + Math.random().toString(36).slice(2, 9);
  const { messages, sendMessage, isStreaming } = useAgentChat(sessionId);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || isStreaming) return;
    sendMessage(input);
    setInput('');
  };

  return (
    <div className='flex flex-col h-screen bg-white max-w-2xl mx-auto'>
      <div className='p-4 border-b font-semibold text-gray-800'>
        Support Agent
      </div>

      <div className='flex-1 overflow-y-auto p-4'>
        {messages.map((m) => (
          <ChatMessage key={m.id} message={m} />
        ))}
        <div ref={bottomRef} />
      </div>

      <div className='p-4 border-t flex gap-2'>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className='flex-1 border rounded-xl px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500'
          placeholder='Type your message...'
        />

        <button
          onClick={handleSend}
          disabled={isStreaming}
          className='bg-blue-600 text-white rounded-xl px-4 py-2 disabled:opacity-50'
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}