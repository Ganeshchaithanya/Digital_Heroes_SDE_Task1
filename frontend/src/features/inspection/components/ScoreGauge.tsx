import React from 'react';

interface ScoreGaugeProps {
  score: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score }) => {
  const getScoreColor = (val: number) => {
    if (val >= 80) return 'from-emerald-400 to-teal-500 text-emerald-400 border-emerald-500/30';
    if (val >= 50) return 'from-amber-400 to-orange-500 text-amber-400 border-amber-500/30';
    return 'from-rose-500 to-red-600 text-rose-500 border-rose-500/30';
  };

  const getScoreLabel = (val: number) => {
    if (val >= 80) return 'Good Health';
    if (val >= 50) return 'Needs Improvement';
    return 'Critical Issues';
  };

  const colorClass = getScoreColor(score);
  const strokeDashoffset = 283 - (283 * score) / 100;

  return (
    <div className="glass-card rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden">
      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Overall Health Score</div>
      
      <div className="relative w-40 h-40 flex items-center justify-center my-2">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            className="text-slate-800"
            strokeWidth="8"
            stroke="currentColor"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            className={`transition-all duration-1000 ease-out stroke-current ${colorClass.split(' ')[2]}`}
            strokeWidth="8"
            strokeDasharray="283"
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-extrabold text-white tracking-tight">{score}</span>
          <span className="text-xs text-slate-500 font-medium">/ 100</span>
        </div>
      </div>

      <div className={`mt-2 px-3 py-1 rounded-full border text-xs font-bold ${colorClass.split(' ')[2]} bg-slate-900/60`}>
        {getScoreLabel(score)}
      </div>
    </div>
  );
};
