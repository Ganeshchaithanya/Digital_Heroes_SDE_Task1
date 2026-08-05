import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-900 bg-slate-950 py-8 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-slate-500">
        <p>PAGEPULSE &copy; {new Date().getFullYear()} — Production Website Inspection Platform</p>
        <p className="mt-1 text-slate-600">Built with Python 3.12, FastAPI, BeautifulSoup4, Pydantic, React, TypeScript & Tailwind CSS</p>
      </div>
    </footer>
  );
};
