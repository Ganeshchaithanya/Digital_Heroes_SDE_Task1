import React, { useState } from 'react';
import { CategoryScores, IssueItem } from '../../../types/inspection';
import { ChevronDown, ChevronUp, CheckCircle, AlertTriangle, Info } from 'lucide-react';

interface CategoryBreakdownProps {
  scores: CategoryScores;
  issues?: IssueItem[];
}

export const CategoryBreakdown: React.FC<CategoryBreakdownProps> = ({ scores, issues = [] }) => {
  const [expandedCat, setExpandedCat] = useState<string | null>(null);

  const categories = [
    { key: 'seo', name: 'SEO Structure', score: scores.seo, weight: '35%' },
    { key: 'performance', name: 'Performance', score: scores.performance, weight: '25%' },
    { key: 'accessibility', name: 'Accessibility', score: scores.accessibility, weight: '25%' },
    { key: 'content', name: 'Content Quality', score: scores.content, weight: '15%' },
  ];

  const getCategoryRules = (catKey: string) => {
    switch (catKey) {
      case 'seo':
        return [
          { name: 'H1 Primary Headline Count', detail: 'Target: Exactly 1 H1 tag' },
          { name: 'Page Title Length', detail: 'Target: 30 to 60 characters' },
          { name: 'Meta Description Length', detail: 'Target: 70 to 160 characters' },
        ];
      case 'performance':
        return [
          { name: 'Server Response Latency', detail: 'Target: Initial GET under 2000 ms' },
        ];
      case 'accessibility':
        return [
          { name: 'Content Image ALT Attributes', detail: 'Excludes decorative & SVG icons' },
        ];
      case 'content':
        return [
          { name: 'Visible Word Count Depth', detail: 'Target: Minimum 300 words' },
        ];
      default:
        return [];
    }
  };

  const toggleExpand = (key: string) => {
    setExpandedCat(expandedCat === key ? null : key);
  };

  return (
    <div className="space-y-3 w-full">
      <div className="grid grid-cols-2 gap-3 w-full">
        {categories.map((cat) => {
          const isExpanded = expandedCat === cat.key;
          const catIssues = issues.filter(i => i.category.toLowerCase() === cat.key);
          const hasIssues = catIssues.length > 0;

          return (
            <div
              key={cat.key}
              onClick={() => toggleExpand(cat.key)}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-4 cursor-pointer transition flex flex-col justify-between"
            >
              <div className="flex items-center justify-between text-xs text-slate-400 font-medium">
                <span className="flex items-center space-x-1">
                  <span>{cat.name}</span>
                  <span className="text-[10px] text-slate-500">({cat.weight})</span>
                </span>
                <div className="flex items-center space-x-1.5">
                  <span className="text-white font-bold text-base">{cat.score}%</span>
                  {isExpanded ? <ChevronUp className="w-3.5 h-3.5 text-cyan-400" /> : <ChevronDown className="w-3.5 h-3.5 text-slate-500" />}
                </div>
              </div>

              <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    cat.score >= 80 ? 'bg-emerald-500' : cat.score >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                  }`}
                  style={{ width: `${cat.score}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Expanded Category Rule Inspection Drawer */}
      {expandedCat && (
        <div className="bg-slate-900/90 border border-cyan-500/30 rounded-xl p-4 text-xs animate-fade-in">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
            <span className="font-bold text-white uppercase tracking-wider">
              {categories.find(c => c.key === expandedCat)?.name} Rules Inspection
            </span>
            <span className="text-slate-400 text-[11px]">Click card again to collapse</span>
          </div>

          <div className="space-y-2">
            {getCategoryRules(expandedCat).map((rule, idx) => {
              const matchingIssue = issues.find(
                i => i.category.toLowerCase() === expandedCat && i.issue.replace('_', ' ').toLowerCase().includes(rule.name.toLowerCase().split(' ')[0])
              );

              return (
                <div key={idx} className="flex items-start justify-between bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                  <div className="flex items-start space-x-2">
                    {matchingIssue ? (
                      matchingIssue.severity === 'critical' ? (
                        <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                      ) : (
                        <Info className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                      )
                    ) : (
                      <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    )}
                    <div>
                      <div className="font-semibold text-white">{rule.name}</div>
                      <div className="text-[11px] text-slate-400">{rule.detail}</div>
                    </div>
                  </div>

                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    matchingIssue ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
                  }`}>
                    {matchingIssue ? 'VARIANCE' : 'PASSED'}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
