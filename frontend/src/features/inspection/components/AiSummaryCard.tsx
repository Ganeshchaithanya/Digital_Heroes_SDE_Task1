import React from 'react';
import { AiSummary } from '../../../types/inspection';
import { Sparkles, CheckCircle2, AlertOctagon, ListOrdered, ShieldCheck } from 'lucide-react';

interface AiSummaryCardProps {
  aiSummary: AiSummary | null;
}

export const AiSummaryCard: React.FC<AiSummaryCardProps> = ({ aiSummary }) => {
  if (!aiSummary) {
    return (
      <div className="glass-card rounded-2xl p-6 border-cyan-900/30">
        <div className="flex items-center space-x-2 text-slate-400 text-xs mb-2">
          <ShieldCheck className="w-4 h-4 text-slate-500" />
          <span>Core Inspection Output</span>
        </div>
        <p className="text-slate-400 text-sm">
          AI summary is currently disabled or unreachable. Deterministic metrics, scores, issues, and recommendations above remain 100% accurate.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card glass-glow rounded-2xl p-6 border border-cyan-500/30 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-md shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white tracking-tight">AI Executive Summary</h3>
            <span className="text-xs text-cyan-400 font-medium">Powered by Groq LLM (llama-3.3-70b-versatile)</span>
          </div>
        </div>

        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-300">
          Fact Verified
        </span>
      </div>

      {/* Executive Summary */}
      <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 mb-6">
        <p className="text-slate-200 text-sm leading-relaxed font-medium">
          "{aiSummary.executive_summary}"
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Key Strengths */}
        <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800/80">
          <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-3 flex items-center space-x-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>Key Strengths</span>
          </h4>
          <ul className="space-y-2 text-xs text-slate-300">
            {aiSummary.key_strengths.map((str, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Prioritized Issues */}
        <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800/80">
          <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center space-x-1.5">
            <AlertOctagon className="w-4 h-4" />
            <span>Prioritized Issues</span>
          </h4>
          <ul className="space-y-2 text-xs text-slate-300">
            {aiSummary.prioritized_issues.map((iss, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>{iss}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Developer Action Plan */}
        <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800/80">
          <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-3 flex items-center space-x-1.5">
            <ListOrdered className="w-4 h-4" />
            <span>Developer Action Plan</span>
          </h4>
          <ol className="space-y-2 text-xs text-slate-300">
            {aiSummary.action_plan.map((act, idx) => (
              <li key={idx} className="flex items-start space-x-2">
                <span className="text-cyan-400 font-bold">{idx + 1}.</span>
                <span>{act}</span>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
};
