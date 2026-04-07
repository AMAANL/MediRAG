import React from 'react';
import PropTypes from 'prop-types';
import CitationCard from './CitationCard';

function ResponseDisplay({ response, isLoading, error }) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 h-full min-h-[500px]">
        <div className="animate-pulse space-y-6">
          <div className="h-6 bg-slate-200 rounded w-1/3"></div>
          <div className="space-y-3">
            <div className="h-4 bg-slate-200 rounded w-full"></div>
            <div className="h-4 bg-slate-100 rounded w-5/6"></div>
            <div className="h-4 bg-slate-100 rounded w-4/6"></div>
          </div>
          <div className="h-6 bg-slate-200 rounded w-1/4 mt-8"></div>
          <div className="space-y-3">
            <div className="h-4 bg-slate-200 rounded w-full"></div>
            <div className="h-4 bg-slate-100 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6 h-full min-h-[500px] flex items-center justify-center flex-col text-center">
        <svg className="w-12 h-12 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <h3 className="text-lg font-bold text-slate-800 mb-2">Analysis Failed</h3>
        <p className="text-slate-600">{error}</p>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="bg-slate-50 rounded-xl border border-dashed border-slate-300 p-6 h-full min-h-[500px] flex items-center justify-center text-center">
        <div className="max-w-sm">
          <svg className="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          <h3 className="text-lg font-medium text-slate-600 mb-2">Awaiting Case Submission</h3>
          <p className="text-sm text-slate-500">Enter patient symptoms and click Analyze to generate a source-backed diagnostic assessment.</p>
        </div>
      </div>
    );
  }

  // Parse diagnosis sections
  const formatText = (text) => {
    return text.split('\n').map((line, i) => {
      if (line.match(/^#+\s/)) {
        return <h3 key={i} className="text-lg font-bold mt-4 mb-2 text-navy-900">{line.replace(/^#+\s/, '')}</h3>;
      } else if (line.match(/^[0-9]+\)/) || line.match(/^[0-9]+\./)) {
        return <h4 key={i} className="text-md font-bold mt-3 mb-1 text-teal-700">{line}</h4>;
      }
      return <p key={i} className="mb-2 text-slate-700 text-sm leading-relaxed">{line}</p>;
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-full min-h-[500px]">
      <div className="p-6 border-b border-slate-100 flex-grow">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-navy-900 flex items-center">
            <svg className="w-5 h-5 mr-2 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
            Clinical Assessment
          </h2>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Confidence: {response.confidence}
          </span>
        </div>
        
        <div className="prose prose-sm max-w-none text-slate-800">
          {formatText(response.diagnosis)}
        </div>
      </div>

      <div className="p-6 bg-slate-50 rounded-b-xl border-t border-slate-200">
        <h3 className="text-sm font-bold text-slate-800 mb-4 uppercase tracking-wider">Citations & References</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {response.sources.map((source, index) => (
            <CitationCard key={index} source={source} index={index + 1} />
          ))}
        </div>
        <div className="mt-6 text-xs text-center text-slate-400">
          Powered by RAG — all responses are source-backed by PubMed and openFDA.
        </div>
      </div>
    </div>
  );
}

ResponseDisplay.propTypes = {
  response: PropTypes.object,
  isLoading: PropTypes.bool.isRequired,
  error: PropTypes.string
};

export default ResponseDisplay;
