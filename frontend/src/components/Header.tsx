import React from 'react';
import { Activity } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-800/60 bg-slate-950 py-4">
      <div className="max-w-4xl mx-auto px-4 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <Activity className="w-5 h-5 text-cyan-400" />
          <span className="text-lg font-bold tracking-tight text-white">PAGEPULSE</span>
        </div>
        <span className="text-xs text-slate-400 font-medium">Website Inspection Platform</span>
      </div>
    </header>
  );
};
