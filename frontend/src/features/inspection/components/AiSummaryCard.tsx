import React from 'react';
import { AiSummary } from '../../../types/inspection';
import { Sparkles } from 'lucide-react';

interface AiSummaryCardProps {
  aiSummary: AiSummary | null;
}

export const AiSummaryCard: React.FC<AiSummaryCardProps> = ({ aiSummary }) => {
  if (!aiSummary) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center space-x-2 text-cyan-400 text-sm font-bold mb-3">
        <Sparkles className="w-4 h-4" />
        <span>AI Health Summary</span>
      </div>

      <p className="text-slate-200 text-sm leading-relaxed mb-6">
        "{aiSummary.executive_summary}"
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <h4 className="font-bold text-emerald-400 mb-2">Key Strengths</h4>
          <ul className="space-y-1.5 text-slate-300">
            {aiSummary.key_strengths.map((s, i) => (
              <li key={i}>• {s}</li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <h4 className="font-bold text-rose-400 mb-2">Main Issues</h4>
          <ul className="space-y-1.5 text-slate-300">
            {aiSummary.prioritized_issues.map((iss, i) => (
              <li key={i}>• {iss}</li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
          <h4 className="font-bold text-cyan-400 mb-2">Action Plan</h4>
          <ol className="space-y-1.5 text-slate-300 list-decimal list-inside">
            {aiSummary.action_plan.map((act, i) => (
              <li key={i}>{act}</li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
};
