import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Database, MessageSquare, History } from 'lucide-react';
import UploadPage from './pages/UploadPage';
import ChatPage from './pages/ChatPage';
import HistoryPage from './pages/HistoryPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-neutral-900 text-neutral-100 font-sans">
        <nav className="border-b border-neutral-800 bg-neutral-950 p-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-2 text-blue-400">
              <Database className="w-6 h-6" />
              <span className="text-xl font-bold tracking-tight">Codebase AI</span>
            </div>
            
            <div className="flex space-x-6">
              <Link to="/" className="flex items-center space-x-1 hover:text-blue-400 transition-colors">
                <Database className="w-4 h-4" />
                <span>Ingest</span>
              </Link>
              <Link to="/chat" className="flex items-center space-x-1 hover:text-blue-400 transition-colors">
                <MessageSquare className="w-4 h-4" />
                <span>Chat</span>
              </Link>
              <Link to="/history" className="flex items-center space-x-1 hover:text-blue-400 transition-colors">
                <History className="w-4 h-4" />
                <span>History</span>
              </Link>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto p-6">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
