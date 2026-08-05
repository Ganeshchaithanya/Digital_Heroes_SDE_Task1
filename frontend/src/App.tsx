import React, { useState } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { UrlInputForm } from './features/inspection/components/UrlInputForm';
import { ScoreGauge } from './features/inspection/components/ScoreGauge';
import { CategoryBreakdown } from './features/inspection/components/CategoryBreakdown';
import { TechnicalMetricsGrid } from './features/inspection/components/TechnicalMetricsGrid';
import { IssuesAccordion } from './features/inspection/components/IssuesAccordion';
import { AiSummaryCard } from './features/inspection/components/AiSummaryCard';
import { inspectUrl } from './services/api';
import { InspectionResponse } from './types/inspection';
import { AlertCircle, ExternalLink } from 'lucide-react';

export const App: React.FC = () => {
  const [data, setData] = useState<InspectionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleInspect = async (url: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await inspectUrl(url);
      setData(result);
    } catch (err: any) {
      console.error('Inspection failed:', err);
      const msg = err.response?.data?.detail?.message || err.message || 'Failed to inspect website.';
      setError(msg);
      setData(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <UrlInputForm onInspect={handleInspect} isLoading={isLoading} />

        {error && (
          <div className="max-w-3xl mx-auto my-6 p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-300 text-sm flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-400" />
            <div>
              <p className="font-bold">Inspection Request Failed</p>
              <p className="text-xs text-rose-400 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {data && (
          <div className="space-y-8 mt-10 animate-fade-in">
            {/* Header URL Details */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800">
              <div>
                <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Inspected URL</div>
                <div className="flex items-center space-x-2 text-xl font-bold text-white mt-1">
                  <span className="truncate max-w-xl">{data.url}</span>
                  <a
                    href={data.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-slate-400 hover:text-cyan-400 transition"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>

              <div className="mt-4 sm:mt-0 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-400">
                HTTP {data.technical_metrics.status_code} • {data.technical_metrics.response_time_ms}ms
              </div>
            </div>

            {/* Score & Breakdown Row */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
              <div className="lg:col-span-1">
                <ScoreGauge score={data.scores.overall} />
              </div>
              <div className="lg:col-span-4 flex items-center">
                <CategoryBreakdown scores={data.scores} />
              </div>
            </div>

            {/* Technical Metrics Grid */}
            <TechnicalMetricsGrid metrics={data.technical_metrics} />

            {/* AI Summary Section */}
            <AiSummaryCard aiSummary={data.ai_summary} />

            {/* Issues & Recommendations */}
            <IssuesAccordion issues={data.issues} recommendations={data.recommendations} />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default App;
