import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import ResponseDisplay from './components/ResponseDisplay';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async (queryData) => {
    setLoading(true);
    setError(null);
    setResponse(null);
    
    try {
      // Changed to relative URL so it works seamlessly in production
      const res = await fetch('/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(queryData)
      });
      
      if (!res.ok) {
        throw new Error('Failed to fetch response');
      }
      
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      {/* Header */}
      <header className="bg-navy-900 text-white py-4 shadow-md px-6 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-teal-600 p-2 rounded-full shadow-inner">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.5 12h3l2.5-6 4 13 2.5-7h3" />
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">MediRAG</h1>
            <p className="text-xs text-teal-100 font-medium">Clinical Decision Support AI</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-5">
            <QueryInput onAnalyze={handleQuery} isLoading={loading} />
          </div>
          <div className="lg:col-span-7">
            <ResponseDisplay response={response} isLoading={loading} error={error} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
