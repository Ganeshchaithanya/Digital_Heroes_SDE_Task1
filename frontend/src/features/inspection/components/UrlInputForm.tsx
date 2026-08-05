import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface UrlInputFormProps {
  onInspect: (url: string) => void;
  isLoading: boolean;
}

export const UrlInputForm: React.FC<UrlInputFormProps> = ({ onInspect, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onInspect(url.trim());
    }
  };

  const samples = ['https://python.org', 'https://example.com', 'https://wikipedia.org'];

  return (
    <div className="w-full max-w-2xl mx-auto my-12 text-center">
      <h1 className="text-3xl font-bold text-white mb-2">Inspect Any Website</h1>
      <p className="text-slate-400 text-sm mb-6">Enter a URL to get instant technical metrics and AI health analysis.</p>

      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <input
          type="text"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isLoading}
          className="flex-1 px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 text-sm"
        />
        <button
          type="submit"
          disabled={isLoading || !url.trim()}
          className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold rounded-xl disabled:opacity-50 flex items-center space-x-2 transition"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Inspecting...</span>
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              <span>Inspect</span>
            </>
          )}
        </button>
      </form>

      <div className="flex items-center justify-center space-x-3 mt-4 text-xs text-slate-500">
        <span>Try sample:</span>
        {samples.map((s) => (
          <button
            key={s}
            onClick={() => { setUrl(s); onInspect(s); }}
            disabled={isLoading}
            className="hover:text-cyan-400 underline transition"
          >
            {s.replace('https://', '')}
          </button>
        ))}
      </div>
    </div>
  );
};
