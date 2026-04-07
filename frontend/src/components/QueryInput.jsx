import React, { useState } from 'react';
import PropTypes from 'prop-types';

function QueryInput({ onAnalyze, isLoading }) {
  const [symptoms, setSymptoms] = useState('');
  const [patientContext, setPatientContext] = useState('');

  const handleAnalyze = () => {
    if (symptoms.trim() === '') return;
    onAnalyze({ symptoms, patient_context: patientContext });
  };

  const handleExampleClick = (text) => {
    setSymptoms(text);
  };

  const examples = [
    "Muscle weakness + elevated CK + cardiac involvement",
    "Recurrent infections + low immunoglobulin levels",
    "Progressive vision loss + hearing impairment + ataxia"
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-navy-900 mb-4 flex items-center">
        <svg className="w-5 h-5 mr-2 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
        Patient Presentation
      </h2>
      
      <div className="space-y-5">
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">Patient Symptoms & History *</label>
          <textarea 
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all placeholder:text-slate-400"
            rows="4"
            placeholder="e.g. Patient presents with progressive muscle weakness..."
          ></textarea>
        </div>

        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">Additional Context (Lab Values, Age, etc.)</label>
          <textarea 
            value={patientContext}
            onChange={(e) => setPatientContext(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all placeholder:text-slate-400"
            rows="3"
            placeholder="e.g. 34yo male, CK elevated to 1200 U/L..."
          ></textarea>
        </div>

        <button 
          onClick={handleAnalyze}
          disabled={isLoading || symptoms.trim() === ''}
          className="w-full bg-navy-900 text-white font-semibold py-3 px-4 rounded-lg hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              <span>Analyze Presentation</span>
            </>
          )}
        </button>

        <div className="pt-4 border-t border-slate-100">
          <p className="text-xs text-slate-500 mb-3 font-medium">Try an example query:</p>
          <div className="flex flex-wrap gap-2">
            {examples.map((ex, i) => (
              <button 
                key={i}
                onClick={() => handleExampleClick(ex)}
                className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 py-1.5 px-3 rounded-full transition-colors border border-slate-200 text-left"
              >
                {ex}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

QueryInput.propTypes = {
  onAnalyze: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
};

export default QueryInput;
