import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950/90 py-6 mt-16 text-center text-xs text-slate-400">
      <div className="max-w-4xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <p className="text-slate-400">
          Built for{' '}
          <a
            href="https://digitalheroesco.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-cyan-400 font-semibold hover:text-cyan-300 underline transition decoration-cyan-500/50 underline-offset-4"
          >
            Digital Heroes Training Task
          </a>
        </p>
        <p className="text-slate-500 text-[11px]">
          PAGEPULSE &copy; {new Date().getFullYear()} — Production Website Inspection Platform
        </p>
      </div>
    </footer>
  );
};
