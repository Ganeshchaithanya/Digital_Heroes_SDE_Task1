import React, { useState } from 'react';
import { Search, Loader2, Globe, Sparkles } from 'lucide-react';

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

  const sampleUrls = [
    'https://python.org',
    'https://example.com',
    'https://wikipedia.org'
  ];

  return (
    <div className="w-full max-w-4xl mx-auto my-8 px-4">
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-cyan-950/60 border border-cyan-800/40 text-cyan-400 text-xs font-semibold mb-4">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Deterministic Audit & AI Insights Engine</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
          Inspect Any Website. <br />
          <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500 bg-clip-text text-transparent">
            Instant Metrics & AI Audits.
          </span>
        </h1>
        <p className="mt-3 text-slate-400 text-sm sm:text-base max-w-2xl mx-auto">
          Enter any webpage URL below. PAGEPULSE downloads the HTML, measures performance, evaluates policy rules, and provides actionable recommendations.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur-lg opacity-25 group-hover:opacity-40 transition duration-300"></div>
        
        <div className="relative flex items-center bg-slate-900/90 border border-slate-700/60 rounded-2xl p-2 shadow-2xl backdrop-blur-xl">
          <div className="pl-4 text-slate-400">
            <Globe className="w-6 h-6 text-cyan-400" />
          </div>
          <input
            type="text"
            placeholder="Enter website URL (e.g. https://python.org)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={isLoading}
            className="w-full px-4 py-3 bg-transparent text-white placeholder-slate-500 font-medium focus:outline-none text-sm sm:text-base"
          />
          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="flex items-center space-x-2 px-6 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Inspecting...</span>
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                <span>Inspect</span>
              </>
            )}
          </button>
        </div>
      </form>

      <div className="flex items-center justify-center space-x-3 mt-4 text-xs text-slate-400">
        <span className="text-slate-500">Try sample URLs:</span>
        {sampleUrls.map((sample) => (
          <button
            key={sample}
            onClick={() => {
              setUrl(sample);
              onInspect(sample);
            }}
            disabled={isLoading}
            className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-cyan-500/50 hover:text-cyan-300 transition duration-150"
          >
            {sample.replace('https://', '')}
          </button>
        ))}
      </div>
    </div>
  );
};
