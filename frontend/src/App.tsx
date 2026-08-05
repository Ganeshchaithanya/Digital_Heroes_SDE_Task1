import React, { useState } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { UrlInputForm } from './features/inspection/components/UrlInputForm';
import { PipelineStepper } from './features/inspection/components/PipelineStepper';
import { ScoreGauge } from './features/inspection/components/ScoreGauge';
import { CategoryBreakdown } from './features/inspection/components/CategoryBreakdown';
import { TechnicalMetricsGrid } from './features/inspection/components/TechnicalMetricsGrid';
import { IssuesAccordion } from './features/inspection/components/IssuesAccordion';
import { AiSummaryCard } from './features/inspection/components/AiSummaryCard';
import { inspectUrl } from './services/api';
import { InspectionResponse } from './types/inspection';
import { AlertCircle, CheckCircle2, XCircle, ExternalLink } from 'lucide-react';

interface ErrorDetail {
  error_code: string;
  status_name: string;
  url_valid: boolean;
  message: string;
}

export const App: React.FC = () => {
  const [data, setData] = useState<InspectionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorObj, setErrorObj] = useState<ErrorDetail | null>(null);

  const handleInspect = async (url: string) => {
    setIsLoading(true);
    setErrorObj(null);
    try {
      const result = await inspectUrl(url);
      setData(result);
    } catch (err: any) {
      console.error('Inspection failed:', err);
      const detail = err.response?.data?.detail;

      if (detail && typeof detail === 'object' && detail.status_name) {
        setErrorObj({
          error_code: detail.error_code || 'INSPECTION_ERROR',
          status_name: detail.status_name,
          url_valid: detail.url_valid !== undefined ? detail.url_valid : true,
          message: detail.message || 'Inspection could not be completed.'
        });
      } else {
        const msg = typeof detail === 'string' ? detail : err.message || 'Failed to inspect website.';
        setErrorObj({
          error_code: 'INSPECTION_ERROR',
          status_name: '❌ Inspection Failed',
          url_valid: true,
          message: msg
        });
      }
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

        {/* Live Inspection Pipeline Stepper */}
        <PipelineStepper isLoading={isLoading} />

        {/* Error Taxonomy & Network Unreachable Banner */}
        {errorObj && (
          <div className="my-6 p-5 rounded-xl bg-slate-900 border border-rose-800/80 shadow-xl animate-fade-in space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 text-xs font-semibold">
              <span className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>{errorObj.url_valid ? '✔ URL Valid' : '❌ URL Format Invalid'}</span>
              </span>
              <span className="text-rose-400 font-bold">{errorObj.status_name}</span>
            </div>

            <div className="flex items-start space-x-3 text-sm">
              <XCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
              <div>
                <div className="font-bold text-white text-base">Inspection Status: {errorObj.status_name}</div>
                <div className="text-xs text-slate-300 mt-1">
                  <span className="font-semibold text-slate-400">Reason: </span>
                  {errorObj.message}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Inspection Results Dashboard */}
        {data && (
          <div className="space-y-6 mt-8">
            {/* Separate Validation & Reachability Status Banner */}
            <div className={`p-4 rounded-xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
              data.technical_metrics.status_code === 200
                ? 'bg-emerald-950/40 border-emerald-800/80 text-emerald-300'
                : 'bg-amber-950/40 border-amber-800/80 text-amber-300'
            }`}>
              <div className="flex items-start sm:items-center space-x-3">
                {data.technical_metrics.status_code === 200 ? (
                  <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0 mt-0.5 sm:mt-0" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5 sm:mt-0" />
                )}
                <div>
                  <div className="flex flex-wrap items-center gap-2 text-xs font-bold mb-0.5">
                    <span className="px-2 py-0.5 rounded bg-emerald-900/60 border border-emerald-700 text-emerald-300">
                      ✔ URL Valid
                    </span>
                    <span className={`px-2 py-0.5 rounded border ${
                      data.technical_metrics.status_code === 200
                        ? 'bg-emerald-900/60 border-emerald-700 text-emerald-300'
                        : 'bg-amber-900/60 border-amber-700 text-amber-300'
                    }`}>
                      {data.technical_metrics.status_code === 200 ? '✔ Website Reachable' : `⚠ HTTP ${data.technical_metrics.status_code}`}
                    </span>
                  </div>
                  <div className="font-bold text-base text-white flex items-center space-x-2">
                    <span>{data.url}</span>
                    <a href={data.url} target="_blank" rel="noreferrer" className="text-slate-400 hover:text-white inline-flex items-center">
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              </div>

              <div className="text-right text-xs font-mono text-slate-300 sm:self-center">
                <div>Status: <strong className="text-white">HTTP {data.technical_metrics.status_code}</strong></div>
                <div>Latency: <strong className="text-cyan-400">{data.technical_metrics.response_time_ms} ms</strong></div>
              </div>
            </div>

            {/* Score & Breakdown Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <ScoreGauge score={data.scores.overall} />
              <div className="md:col-span-2">
                <CategoryBreakdown scores={data.scores} issues={data.issues} />
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
