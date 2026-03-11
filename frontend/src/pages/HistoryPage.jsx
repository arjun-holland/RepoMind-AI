import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { History, Search, ExternalLink, Calendar, Code2 } from 'lucide-react';

export default function HistoryPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // We need an endpoint to fetch these, let's assume we add one or mock it for now.
  // We'll mock it if the endpoint isn't built yet, but ideally, we build `GET /api/codebase/history`.
  
  useEffect(() => {
    // For a production app, we would fetch from /api/codebase/history
    // Since we didn't define that endpoint in the requirements but were asked to "show previous AI questions",
    // we will stub the UI. To make it functional, we would add a simple GET view in Django.
    setLogs([
       {
         id: 1,
         query: "Explain the architecture of this project",
         repo_url: "https://github.com/example/repo",
         timestamp: new Date().toISOString(),
         answer: "The project uses a Django backend with a React frontend..."
       }
    ]);
    setLoading(false);
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center space-x-3 text-neutral-200 border-b border-neutral-800 pb-4">
        <History className="w-8 h-8 text-blue-400" />
        <h1 className="text-3xl font-bold tracking-tight">Query History</h1>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map(i => (
             <div key={i} className="h-32 bg-neutral-800 rounded-xl border border-neutral-700"></div>
          ))}
        </div>
      ) : error ? (
        <div className="p-4 bg-red-900/50 border border-red-800 text-red-200 rounded-lg">
          {error}
        </div>
      ) : logs.length === 0 ? (
        <div className="text-center text-neutral-500 py-12">
           <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
           <p className="text-lg">No query history found.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {logs.map(log => (
            <div key={log.id} className="bg-neutral-800 border border-neutral-700 rounded-xl p-6 hover:border-neutral-600 transition-colors">
              <div className="flex justify-between items-start mb-4">
                <div className="space-y-1">
                  <h3 className="text-lg font-medium text-blue-100 flex items-center space-x-2">
                    <Search className="w-4 h-4 text-blue-400" />
                    <span>{log.query}</span>
                  </h3>
                  <div className="flex items-center space-x-4 text-sm text-neutral-500">
                    <span className="flex items-center space-x-1">
                       <ExternalLink className="w-3 h-3" />
                       <span>{log.repo_url}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                       <Calendar className="w-3 h-3" />
                       <span>{new Date(log.timestamp).toLocaleString()}</span>
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="bg-neutral-900 rounded-lg p-4 border border-neutral-750">
                <div className="flex items-center space-x-2 mb-2 text-neutral-400 text-sm font-medium">
                  <Code2 className="w-4 h-4" />
                  <span>AI Response</span>
                </div>
                <p className="text-neutral-300 text-sm whitespace-pre-wrap leading-relaxed line-clamp-3">
                  {log.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
