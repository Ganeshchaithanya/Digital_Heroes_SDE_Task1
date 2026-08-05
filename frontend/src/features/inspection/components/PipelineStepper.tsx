import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2 } from 'lucide-react';

interface PipelineStepperProps {
  isLoading: boolean;
}

export const PipelineStepper: React.FC<PipelineStepperProps> = ({ isLoading }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { title: '1. Validating URL Syntax & Scheme', detail: 'Validation Layer' },
    { title: '2. Connecting & Network Inspection', detail: 'Inspection Engine (httpx)' },
    { title: '3. Parsing HTML Structure', detail: 'HTML Parser (BS4 / lxml)' },
    { title: '4. Extracting Feature Metrics', detail: 'Feature Extraction Subsystem' },
    { title: '5. Evaluating Policy Rules', detail: 'Policy Engine (v1)' },
    { title: '6. Generating AI Insights', detail: 'Groq LLM & Verifier' },
  ];

  useEffect(() => {
    if (!isLoading) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) return prev + 1;
        return prev;
      });
    }, 700);

    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading) return null;

  return (
    <div className="my-8 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl max-w-2xl mx-auto animate-fade-in">
      <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm mb-4 border-b border-slate-800 pb-3">
        <Loader2 className="w-4 h-4 animate-spin" />
        <span>Executing Inspection Pipeline...</span>
      </div>

      <div className="space-y-3">
        {steps.map((step, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div
              key={idx}
              className={`flex items-center justify-between p-2.5 rounded-lg border text-xs transition duration-300 ${
                isDone
                  ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-300'
                  : isCurrent
                  ? 'bg-cyan-950/60 border-cyan-700/80 text-cyan-200 font-semibold'
                  : 'bg-slate-950/40 border-slate-900 text-slate-600'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 text-cyan-400 animate-spin flex-shrink-0" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-slate-700 flex-shrink-0"></div>
                )}
                <span>{step.title}</span>
              </div>

              <span className="text-[10px] opacity-75 font-mono">{step.detail}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
