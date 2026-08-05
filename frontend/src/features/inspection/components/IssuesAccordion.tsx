import React from 'react';
import { IssueItem } from '../../../types/inspection';

interface IssuesAccordionProps {
  issues: IssueItem[];
  recommendations: string[];
}

export const IssuesAccordion: React.FC<IssuesAccordionProps> = ({ issues, recommendations }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Detected Issues */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Detected Issues ({issues.length})</h3>
        {issues.length === 0 ? (
          <p className="text-xs text-slate-500">No issues found! Webpage meets all standards.</p>
        ) : (
          <div className="space-y-3 text-xs">
            {issues.map((item, idx) => (
              <div key={idx} className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-white uppercase">{item.issue.replace('_', ' ')}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                    item.severity === 'critical' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {item.severity}
                  </span>
                </div>
                <p className="text-slate-400 text-xs mt-1">{item.recommendation}</p>
                <div className="mt-2 text-[11px] text-slate-500">
                  Observed: <span className="text-rose-400 font-mono">{String(item.observed_value)}</span> | Expected: <span className="text-emerald-400 font-mono">{item.expected_value}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recommendations Checklist */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Fix Recommendations</h3>
        {recommendations.length === 0 ? (
          <p className="text-xs text-slate-500">No recommendations needed.</p>
        ) : (
          <ul className="space-y-2.5 text-xs text-slate-300">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start space-x-2 bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-cyan-400 font-bold">{idx + 1}.</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
