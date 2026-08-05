import React from 'react';
import { CategoryScores } from '../../../types/inspection';
import { Search, Zap, Eye, FileText } from 'lucide-react';

interface CategoryBreakdownProps {
  scores: CategoryScores;
}

export const CategoryBreakdown: React.FC<CategoryBreakdownProps> = ({ scores }) => {
  const categories = [
    { key: 'seo', name: 'SEO Structure', score: scores.seo, icon: Search, color: 'text-cyan-400', bg: 'bg-cyan-500/10' },
    { key: 'performance', name: 'Performance', score: scores.performance, icon: Zap, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { key: 'accessibility', name: 'Accessibility', score: scores.accessibility, icon: Eye, color: 'text-purple-400', bg: 'bg-purple-500/10' },
    { key: 'content', name: 'Content Quality', score: scores.content, icon: FileText, color: 'text-amber-400', bg: 'bg-amber-500/10' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full">
      {categories.map((cat) => {
        const Icon = cat.icon;
        return (
          <div key={cat.key} className="glass-card rounded-xl p-5 flex flex-col justify-between hover:border-slate-700 transition duration-200">
            <div className="flex items-center justify-between">
              <div className={`p-2.5 rounded-lg ${cat.bg}`}>
                <Icon className={`w-5 h-5 ${cat.color}`} />
              </div>
              <span className="text-2xl font-bold text-white">{cat.score}%</span>
            </div>
            
            <div className="mt-4">
              <div className="text-sm font-semibold text-slate-200">{cat.name}</div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    cat.score >= 80 ? 'bg-emerald-500' : cat.score >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                  }`}
                  style={{ width: `${cat.score}%` }}
                ></div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
