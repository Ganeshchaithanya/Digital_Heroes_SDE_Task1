import React from 'react';

interface ScoreGaugeProps {
  score: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score }) => {
  const getBadge = (val: number) => {
    if (val >= 80) return { label: 'Good Health', class: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
    if (val >= 50) return { label: 'Needs Improvement', class: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
    return { label: 'Action Required', class: 'bg-rose-500/10 text-rose-400 border-rose-500/30' };
  };

  const badge = getBadge(score);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
      <span className="text-xs text-slate-400 font-medium uppercase tracking-wider mb-1">Overall Score</span>
      <div className="text-5xl font-extrabold text-white my-2">{score}<span className="text-lg text-slate-500 font-normal">/100</span></div>
      <span className={`text-xs font-semibold px-3 py-1 rounded-full border mt-1 ${badge.class}`}>
        {badge.label}
      </span>
    </div>
  );
};
