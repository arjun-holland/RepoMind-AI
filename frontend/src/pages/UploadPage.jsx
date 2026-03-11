import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Github, Loader2, CheckCircle, Database } from 'lucide-react';

export default function UploadPage() {
  const [url, setUrl] = useState('');
  const [status, setStatus] = useState('idle'); // idle, checking, polling, success, error
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleIngest = async (e) => {
    e.preventDefault();
    setStatus('checking');
    setError('');

    try {
      const res = await axios.post('http://localhost:8000/api/repository/ingest', { repo_url: url });
      
      if (res.data.message === 'Repository already indexed') {
        setStatus('success');
        return;
      }

      // Start polling
      setStatus('polling');
      pollStatus(res.data.record_id);

    } catch (err) {
      setStatus('error');
      setError(err.response?.data?.error || 'Failed to communicate with server');
    }
  };

  const pollStatus = async (recordId) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/repository/status?record_id=${recordId}`);
        const repoStatus = res.data.status;
        
        if (repoStatus === 'ready') {
          clearInterval(interval);
          setStatus('success');
        } else if (repoStatus === 'failed') {
          clearInterval(interval);
          setStatus('error');
          setError(res.data.error || 'Repository ingestion failed during processing');
        }
        
      } catch (err) {
        clearInterval(interval);
        setStatus('error');
        setError('Lost connection while polling status');
      }
    }, 2000);
  };

  return (
    <div className="max-w-2xl mx-auto mt-20">
      <div className="bg-neutral-800 p-8 rounded-2xl border border-neutral-700 shadow-xl">
        <h1 className="text-3xl font-bold mb-2 flex items-center space-x-3">
          <Database className="w-8 h-8 text-blue-400" />
          <span>Ingest Repository</span>
        </h1>
        <p className="text-neutral-400 mb-8">
          Provide a public GitHub repository. The assistant will clone, scan the abstract syntax trees, generate embeddings in ChromaDB, and construct a knowledge base.
        </p>

        <form onSubmit={handleIngest} className="space-y-4">
          <div>
            <div className="relative">
              <Github className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-500" />
              <input 
                type="url" 
                required
                placeholder="https://github.com/example/repo"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full bg-neutral-900 border border-neutral-700 rounded-lg py-3 pl-11 pr-4 focus:outline-none focus:border-blue-500 transition-colors"
                disabled={status === 'checking' || status === 'polling'}
              />
            </div>
          </div>
          
          <button 
            type="submit"
            disabled={!url || status === 'checking' || status === 'polling'}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors flex justify-center items-center space-x-2"
          >
            {(status === 'checking' || status === 'polling') ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>{status === 'checking' ? 'Initializing...' : 'Indexing Codebase...'}</span>
              </>
            ) : status === 'success' ? (
               <>
                <CheckCircle className="w-5 h-5" />
                <span>Indexed Successfully</span>
              </>
            ) : (
               <span>Analyze Repository</span>
            )}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-900/50 border border-red-800 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {status === 'success' && (
          <div className="mt-8 flex justify-center">
            <button 
              onClick={() => navigate('/chat', { state: { repo_url: url } })}
              className="bg-neutral-700 hover:bg-neutral-600 px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Continue to Chat →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
