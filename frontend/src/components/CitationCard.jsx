import React from 'react';
import PropTypes from 'prop-types';

function CitationCard({ source, index }) {
  const isFDA = source.source === 'openFDA';
  const badgeColor = isFDA ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800';

  return (
    <a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 bg-white border border-slate-200 rounded-lg hover:border-teal-500 hover:shadow-md transition-all cursor-pointer group"
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-2 mb-2">
          <span className="shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-slate-100 text-slate-500 text-xs font-bold font-mono">
            {index}
          </span>
          <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${badgeColor}`}>
            {source.source}
          </span>
        </div>
        <svg className="w-4 h-4 text-slate-300 group-hover:text-teal-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
        </svg>
      </div>
      <h4 className="text-sm font-semibold text-slate-800 line-clamp-2 leading-tight group-hover:text-teal-700 transition-colors">
        {source.title}
      </h4>
    </a>
  );
}

CitationCard.propTypes = {
  source: PropTypes.shape({
    title: PropTypes.string.isRequired,
    source: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired
  }).isRequired,
  index: PropTypes.number.isRequired
};

export default CitationCard;
