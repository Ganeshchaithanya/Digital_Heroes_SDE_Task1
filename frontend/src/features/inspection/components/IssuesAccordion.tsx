import React from 'react';
import { IssueItem } from '../../../types/inspection';
import { AlertTriangle, AlertCircle, Info, CheckCircle, ArrowRight } from 'lucide-react';

interface IssuesAccordionProps {
  issues: IssueItem[];
  recommendations: string[];
}

export const IssuesAccordion: React.FC<IssuesAccordionProps> = ({ issues, recommendations }) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return {
          bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
          icon: AlertOctagonIcon,
          label: 'CRITICAL'
        };
      case 'warning':
        return {
          bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
          icon: AlertTriangle,
          label: 'WARNING'
        };
      default:
        return {
          bg: 'bg-sky-500/10 border-sky-500/30 text-sky-400',
          icon: Info,
          label: 'INFO'
        };
    }
  };

  function AlertOctagonIcon(props: any) {
    return <AlertCircle {...props} />;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Issues Column */}
      <div className="lg:col-span-2 glass-card rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-white flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span>Detected Policy Issues ({issues.length})</span>
          </h3>
          {issues.length === 0 && (
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center space-x-1">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>All Checks Passed</span>
            </span>
          )}
        </div>

        {issues.length === 0 ? (
          <div className="text-center py-10 border border-dashed border-slate-800 rounded-xl">
            <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
            <p className="text-slate-300 font-semibold">Zero Issues Found!</p>
            <p className="text-slate-500 text-xs mt-1">This webpage satisfies all active deterministic evaluation policies.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {issues.map((item, idx) => {
              const badge = getSeverityBadge(item.severity);
              const BadgeIcon = badge.icon;
              return (
                <div key={idx} className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 transition hover:border-slate-700">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${badge.bg} flex items-center space-x-1`}>
                          <BadgeIcon className="w-3 h-3" />
                          <span>{badge.label}</span>
                        </span>
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{item.category}</span>
                      </div>
                      <h4 className="text-base font-semibold text-white mt-1.5 capitalize">
                        {item.issue.replace('_', ' ')}
                      </h4>
                    </div>

                    <div className="text-right text-xs">
                      <span className="text-slate-400 block">Observed: <strong className="text-rose-400 font-mono">{String(item.observed_value)}</strong></span>
                      <span className="text-slate-500 block">Target: <strong className="text-emerald-400 font-mono">{item.expected_value}</strong></span>
                    </div>
                  </div>

                  <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-start space-x-2 text-xs text-slate-300">
                    <ArrowRight className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                    <p>{item.recommendation}</p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Recommendations Column */}
      <div className="glass-card rounded-2xl p-6">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
          <CheckCircle className="w-5 h-5 text-emerald-400" />
          <span>Actionable Fixes</span>
        </h3>

        {recommendations.length === 0 ? (
          <p className="text-slate-500 text-xs">No fixes required. Website adheres to standards.</p>
        ) : (
          <ul className="space-y-3 text-xs">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start space-x-2.5 p-3 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <span className="w-5 h-5 rounded-full bg-cyan-950 text-cyan-400 font-bold text-[11px] flex items-center justify-center flex-shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <span className="text-slate-300 leading-relaxed">{rec}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
