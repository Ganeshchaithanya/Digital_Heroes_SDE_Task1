import React from 'react';
import { CategoryScores } from '../../../types/inspection';

interface CategoryBreakdownProps {
  scores: CategoryScores;
}

export const CategoryBreakdown: React.FC<CategoryBreakdownProps> = ({ scores }) => {
  const items = [
    { label: 'SEO', score: scores.seo },
    { label: 'Performance', score: scores.performance },
    { label: 'Accessibility', score: scores.accessibility },
    { label: 'Content', score: scores.content },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 w-full">
      {items.map((i) => (
        <div key={i.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 font-medium">
            <span>{i.label}</span>
            <span className="text-white font-bold text-base">{i.score}%</span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className={`h-full rounded-full ${i.score >= 80 ? 'bg-emerald-500' : i.score >= 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
              style={{ width: `${i.score}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};
