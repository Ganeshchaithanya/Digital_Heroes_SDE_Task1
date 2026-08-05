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
import { AlertCircle, CheckCircle2, XCircle, ExternalLink } from 'lucide-react';

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

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8">
        <UrlInputForm onInspect={handleInspect} isLoading={isLoading} />

        {/* Error / Invalid URL Banner */}
        {error && (
          <div className="my-6 p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-300 text-sm flex items-center space-x-3">
            <XCircle className="w-6 h-6 flex-shrink-0 text-rose-400" />
            <div>
              <p className="font-bold text-base">URL Validity Status: ❌ INVALID URL / UNREACHABLE</p>
              <p className="text-xs text-rose-400 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Inspection Results Dashboard */}
        {data && (
          <div className="space-y-6 mt-8">
            {/* Validity Status Banner */}
            <div className={`p-4 rounded-xl border flex items-center justify-between ${
              data.technical_metrics.status_code === 200
                ? 'bg-emerald-950/50 border-emerald-800/80 text-emerald-300'
                : 'bg-amber-950/50 border-amber-800/80 text-amber-300'
            }`}>
              <div className="flex items-center space-x-3">
                {data.technical_metrics.status_code === 200 ? (
                  <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-amber-400 flex-shrink-0" />
                )}
                <div>
                  <div className="font-bold text-base flex items-center space-x-2">
                    <span>Website Validity Status:</span>
                    <span className={data.technical_metrics.status_code === 200 ? 'text-emerald-400' : 'text-amber-400'}>
                      {data.technical_metrics.status_code === 200 ? '✅ VALID & ACCESSIBLE (HTTP 200 OK)' : `⚠️ ACCESSIBLE WITH HTTP STATUS ${data.technical_metrics.status_code}`}
                    </span>
                  </div>
                  <div className="text-xs opacity-90 mt-0.5 flex items-center space-x-2">
                    <span className="font-mono">{data.url}</span>
                    <a href={data.url} target="_blank" rel="noreferrer" className="underline hover:text-white inline-flex items-center">
                      <ExternalLink className="w-3 h-3 ml-1" />
                    </a>
                  </div>
                </div>
              </div>

              <div className="text-right text-xs font-mono">
                <div>Latency: {data.technical_metrics.response_time_ms} ms</div>
              </div>
            </div>

            {/* Score & Breakdown Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <ScoreGauge score={data.scores.overall} />
              <div className="md:col-span-2">
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
