import React from 'react';
import { TechnicalMetrics } from '../../../types/inspection';
import { Clock, CheckCircle2, Type, Image, FileText, Link, Heading1, Heading2 } from 'lucide-react';

interface TechnicalMetricsGridProps {
  metrics: TechnicalMetrics;
}

export const TechnicalMetricsGrid: React.FC<TechnicalMetricsGridProps> = ({ metrics }) => {
  const metricCards = [
    { label: 'Response Time', value: `${metrics.response_time_ms} ms`, icon: Clock, detail: 'Network GET Latency' },
    { label: 'HTTP Status', value: `${metrics.status_code}`, icon: CheckCircle2, detail: metrics.status_code === 200 ? '200 OK' : 'Non-200 Status' },
    { label: 'Title Length', value: `${metrics.title_length} chars`, icon: Type, detail: 'Target: 30 - 60 chars' },
    { label: 'Meta Description', value: `${metrics.meta_description_length} chars`, icon: FileText, detail: 'Target: 70 - 160 chars' },
    { label: 'H1 Headings', value: `${metrics.h1_count}`, icon: Heading1, detail: 'Target: Exactly 1' },
    { label: 'H2 Headings', value: `${metrics.h2_count}`, icon: Heading2, detail: 'Subheading Count' },
    { label: 'Images Total', value: `${metrics.total_images_count}`, icon: Image, detail: `${metrics.missing_alt_images_count} missing ALT` },
    { label: 'Word Count', value: `${metrics.word_count}`, icon: FileText, detail: 'Target: >= 300 words' },
    { label: 'Internal Links', value: `${metrics.internal_links_count}`, icon: Link, detail: 'Same-domain links' },
    { label: 'External Links', value: `${metrics.external_links_count}`, icon: Link, detail: 'Outbound links' },
  ];

  return (
    <div className="glass-card rounded-2xl p-6">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
        <FileText className="w-5 h-5 text-cyan-400" />
        <span>Technical Metrics</span>
      </h3>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {metricCards.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div key={idx} className="bg-slate-900/80 border border-slate-800/80 rounded-xl p-3.5 flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs font-medium text-slate-400 truncate">{m.label}</span>
                <Icon className="w-4 h-4 text-cyan-400/80" />
              </div>
              <div className="mt-2">
                <div className="text-lg font-bold text-white tracking-tight">{m.value}</div>
                <div className="text-[11px] text-slate-500 font-medium truncate mt-0.5">{m.detail}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
