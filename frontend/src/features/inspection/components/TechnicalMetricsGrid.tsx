import React from 'react';
import { TechnicalMetrics } from '../../../types/inspection';

interface TechnicalMetricsGridProps {
  metrics: TechnicalMetrics;
}

export const TechnicalMetricsGrid: React.FC<TechnicalMetricsGridProps> = ({ metrics }) => {
  const items = [
    { label: 'Response Time', val: `${metrics.response_time_ms} ms` },
    { label: 'HTTP Status', val: `${metrics.status_code}` },
    { label: 'Title Length', val: `${metrics.title_length} chars` },
    { label: 'Meta Description', val: `${metrics.meta_description_length} chars` },
    { label: 'H1 Headings', val: `${metrics.h1_count}` },
    { label: 'H2 Headings', val: `${metrics.h2_count}` },
    { label: 'Images (Missing ALT)', val: `${metrics.total_images_count} (${metrics.missing_alt_images_count} missing)` },
    { label: 'Word Count', val: `${metrics.word_count} words` },
    { label: 'Internal Links', val: `${metrics.internal_links_count}` },
    { label: 'External Links', val: `${metrics.external_links_count}` },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">Technical Metrics</h3>
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
        {items.map((m, idx) => (
          <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800/60">
            <span className="text-slate-400 block text-[11px] font-medium">{m.label}</span>
            <span className="text-white font-bold text-sm mt-1 block truncate">{m.val}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
