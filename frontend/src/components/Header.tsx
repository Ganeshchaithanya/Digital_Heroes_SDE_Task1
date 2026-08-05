import React from 'react';
import { Activity, ShieldCheck, Cpu } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
              PAGEPULSE
            </span>
            <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-800/50 text-cyan-400">
              v1.0 Engine
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-6 text-xs text-slate-400 font-medium">
          <div className="hidden sm:flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Deterministic Policy Audit</span>
          </div>
          <div className="hidden sm:flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Groq LLM Insights</span>
          </div>
        </div>
      </div>
    </header>
  );
};
