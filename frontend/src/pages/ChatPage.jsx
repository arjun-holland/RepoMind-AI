import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Send, Bot, User, FileCode2, Loader2 } from 'lucide-react';

export default function ChatPage() {
  const location = useLocation();
  const initialRepo = location.state?.repo_url || '';
  
  const [repoUrl, setRepoUrl] = useState(initialRepo);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim() || !repoUrl.trim()) return;

    const userMessage = { role: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const res = await axios.post(`${API_URL}/api/codebase/query`, {
        repo_url: repoUrl,
        query: userMessage.content
      });

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.answer,
        references: res.data.references
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'system',
        content: err.response?.data?.error || 'Failed to get an answer. Ensure the repository is fully indexed.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-100px)] max-w-4xl mx-auto">
      <div className="bg-neutral-800 p-4 rounded-t-xl border border-neutral-700 border-b-0 flex items-center space-x-4">
        <label className="text-sm font-medium text-neutral-400 whitespace-nowrap">Target Repository:</label>
        <input 
          type="url"
          value={repoUrl}
          onChange={e => setRepoUrl(e.target.value)}
          placeholder="https://github.com/..."
          className="bg-neutral-900 border border-neutral-700 rounded-md px-3 py-1 text-sm w-full focus:outline-none focus:border-blue-500"
        />
      </div>

      <div className="flex-1 overflow-y-auto bg-neutral-900 border-x border-neutral-700 p-6 space-y-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-neutral-500 space-y-4">
            <Bot className="w-16 h-16 opacity-50" />
            <p className="text-lg">Ask anything about the codebase!</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex space-x-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role !== 'user' && (
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'system' ? 'bg-red-900' : 'bg-blue-900'}`}>
                <Bot className="w-5 h-5 text-blue-200" />
              </div>
            )}
            
            <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-blue-600 text-white' : msg.role === 'system' ? 'bg-red-900/50 text-red-200 border border-red-800' : 'bg-neutral-800 border border-neutral-700'}`}>
              <div className="whitespace-pre-wrap">{msg.content}</div>
              
              {msg.references && msg.references.length > 0 && (
                <div className="mt-4 pt-4 border-t border-neutral-700">
                  <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider mb-2 block">Referenced Files:</span>
                  <div className="flex flex-wrap gap-2">
                    {msg.references.map((ref, i) => (
                      <div key={i} className="flex items-center space-x-1 bg-neutral-900 border border-neutral-700 text-xs px-2 py-1 rounded">
                        <FileCode2 className="w-3 h-3 text-blue-400" />
                        <span className="text-neutral-300 font-mono">{ref}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center shrink-0">
                <User className="w-5 h-5 text-neutral-300" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex space-x-4 justify-start">
             <div className="w-8 h-8 rounded-full bg-blue-900 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 text-blue-200" />
              </div>
              <div className="bg-neutral-800 border border-neutral-700 rounded-2xl p-4 flex items-center space-x-2">
                <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
                <span className="text-neutral-400 animate-pulse">Analyzing vector references...</span>
              </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="bg-neutral-800 p-4 border border-neutral-700 rounded-b-xl flex space-x-2">
        <input 
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="e.g. Where is the database connection initialized?"
          className="flex-1 bg-neutral-900 border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
          disabled={loading}
        />
        <button 
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white p-3 rounded-lg transition-colors flex items-center justify-center"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  )
}
