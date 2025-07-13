import { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAnalysisData } from '../hooks/useAnalysisData';
import { leagueApi } from '../services/api';
import { ExpectedWinsChart } from '../components/Charts/ExpectedWinsChart';
import { EWDifferenceChart } from '../components/Charts/EWDifferenceChart';
import { LuckChart } from '../components/Charts/LuckChart';
import { BonageChart } from '../components/Charts/BonageChart';
import { ConsistencyChart } from '../components/Charts/ConsistencyChart';
import { SleepersTable } from '../components/Charts/SleepersTable';
import { PositionalRanksChart } from '../components/Charts/PositionalRanksChart';
import { DraftInjuryTable } from '../components/Charts/DraftInjuryTable';
import toast from 'react-hot-toast';

// Extend Window interface to include Plotly
declare global {
  interface Window {
    Plotly?: any;
  }
}

export const Analysis = () => {
  const [searchParams] = useSearchParams();
  const [leagueId, setLeagueId] = useState<string>('');
  const [isProcessingDraft, setIsProcessingDraft] = useState(false);
  const analysisData = useAnalysisData(leagueId);
  const chartRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  // Read league ID from URL parameters
  useEffect(() => {
    const urlLeagueId = searchParams.get('leagueId');
    if (urlLeagueId) {
      setLeagueId(urlLeagueId);
    }
  }, [searchParams]);

  // Trigger Plotly resize after charts are rendered
  useEffect(() => {
    const timer = setTimeout(() => {
      // Try to trigger Plotly resize for all charts
      if (window.Plotly) {
        Object.values(chartRefs.current).forEach(ref => {
          if (ref) {
            const plotlyDiv = ref.querySelector('.plotly-graph-div');
            if (plotlyDiv) {
              try {
                window.Plotly.relayout(plotlyDiv, {});
              } catch (e) {
                console.log('Plotly resize failed:', e);
              }
            }
          }
        });
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [analysisData]);

  const handleProcessDraft = async () => {
    if (!leagueId) {
      toast.error('Please enter a league ID first');
      return;
    }

    setIsProcessingDraft(true);
    try {
      await leagueApi.processDraft(leagueId);
      toast.success('Draft processing completed!');
      
      // Refetch draft analysis data
      analysisData.sleepers.refetch();
      analysisData.positionalRanks.refetch();
      analysisData.draftInjury.refetch();
    } catch (error) {
      toast.error('Failed to process draft data');
      console.error('Draft processing error:', error);
    } finally {
      setIsProcessingDraft(false);
    }
  };

  const renderChart = (chartHtml: string, title: string) => {
    // Debug: Log the chart HTML content
    console.log(`DEBUG: Rendering chart for ${title}:`, chartHtml);
    console.log(`DEBUG: Chart HTML length: ${chartHtml?.length || 0}`);
    
    if (!chartHtml || chartHtml.length === 0) {
      console.error(`DEBUG: Empty chart HTML for ${title}`);
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
    
    const chartId = `chart-${title.replace(/\s+/g, '-').toLowerCase()}`;
    
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <div 
          ref={(el) => {
            chartRefs.current[chartId] = el;
          }}
          className="w-full h-100 overflow-hidden"
          style={{ minHeight: '400px' }}
          dangerouslySetInnerHTML={{ __html: chartHtml }}
        />
      </div>
    );
  };

  const renderExpectedWinsChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <ExpectedWinsChart data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderEWDifferenceChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <EWDifferenceChart 
            data={data.chart_data} 
            title={title} 
            summary={data.metadata?.summary}
          />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderLuckChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <LuckChart 
            data={data.chart_data} 
            title={title} 
            summary={data.metadata?.summary}
          />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderBonageChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <BonageChart data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderConsistencyChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <ConsistencyChart data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderSleepersChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <SleepersTable data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderPositionalRanksChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <PositionalRanksChart data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderDraftInjuryChart = (data: any, title: string) => {
    if (data.chart_data) {
      return (
        <div className="card">
          <DraftInjuryTable data={data.chart_data} title={title} />
        </div>
      );
    } else if (data.chart_html) {
      return renderChart(data.chart_html, title);
    } else {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800">No chart data available</p>
          </div>
        </div>
      );
    }
  };

  const renderLoadingState = (title: string) => (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <span className="ml-3 text-gray-600">Loading...</span>
      </div>
    </div>
  );

  const renderErrorState = (title: string, error: any) => {
    // Check if this is a draft analysis error that requires processing
    const isDraftAnalysis = title.includes('Sleepers') || title.includes('Positional Ranks') || title.includes('Draft Injury');
    const isProcessingError = error?.response?.status === 400 && 
                             (error?.response?.data?.solution || 
                              error?.response?.data?.error?.includes('Draft data not available'));
    
    if (isDraftAnalysis && isProcessingError) {
      return (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-blue-800 mb-2">
              <strong>Draft data not available.</strong> This analysis requires draft data to be processed first.
            </p>
            <p className="text-blue-700 text-sm">
              Click the "Process Draft Data" button above to analyze your league's draft.
            </p>
          </div>
        </div>
      );
    }
    
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Failed to load chart: {error?.message || 'Unknown error'}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">League Analysis</h1>
        <p className="text-lg text-gray-600">
          View detailed analytics and insights for your fantasy football league
        </p>
      </div>

      {/* League ID Input */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">League ID</h2>
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={leagueId}
            onChange={(e) => setLeagueId(e.target.value)}
            placeholder="Enter your league ID (e.g., 1103905062545362944)"
            className="input-field flex-1"
          />
          <button
            onClick={handleProcessDraft}
            disabled={!leagueId || isProcessingDraft}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {isProcessingDraft ? 'Processing Draft...' : 'Process Draft Data'}
          </button>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Enter the league ID from your processed league to view analysis charts
        </p>
      </div>

      {!leagueId ? (
        <div className="text-center py-12">
          <div className="text-gray-500">
            <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p className="text-lg font-medium">Enter a League ID to View Analysis</p>
            <p className="text-sm">Use the league ID from your processed league to see charts and analytics</p>
          </div>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Scoring Analysis Section */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Scoring Analysis</h2>
            <div className="space-y-6">
              {/* Expected Wins */}
              {analysisData.expectedWins.isLoading && renderLoadingState('Expected Wins Analysis')}
              {analysisData.expectedWins.isError && renderErrorState('Expected Wins Analysis', analysisData.expectedWins.error)}
              {analysisData.expectedWins.data && renderExpectedWinsChart(
                analysisData.expectedWins.data,
                'Expected Wins Analysis'
              )}

              {/* EW Difference */}
              {analysisData.ewDifference.isLoading && renderLoadingState('EW Difference Analysis')}
              {analysisData.ewDifference.isError && renderErrorState('EW Difference Analysis', analysisData.ewDifference.error)}
              {analysisData.ewDifference.data && renderEWDifferenceChart(
                analysisData.ewDifference.data,
                'EW Difference Analysis'
              )}

              {/* Luck Analysis */}
              {analysisData.luck.isLoading && renderLoadingState('Luck Analysis')}
              {analysisData.luck.isError && renderErrorState('Luck Analysis', analysisData.luck.error)}
              {analysisData.luck.data && renderLuckChart(
                analysisData.luck.data,
                'Luck Analysis'
              )}

              {/* Bonage Analysis */}
              {analysisData.bonage.isLoading && renderLoadingState('Bonage Analysis')}
              {analysisData.bonage.isError && renderErrorState('Bonage Analysis', analysisData.bonage.error)}
              {analysisData.bonage.data && renderBonageChart(
                analysisData.bonage.data,
                'Bonage Analysis'
              )}

              {/* Consistency Analysis */}
              {analysisData.consistency.isLoading && renderLoadingState('Consistency Analysis')}
              {analysisData.consistency.isError && renderErrorState('Consistency Analysis', analysisData.consistency.error)}
              {analysisData.consistency.data && renderConsistencyChart(
                analysisData.consistency.data,
                'Consistency Analysis'
              )}
            </div>
          </div>

          {/* Draft Analysis Section */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Draft Analysis</h2>
            <div className="space-y-6">
              {/* Sleepers */}
              {analysisData.sleepers.isLoading && renderLoadingState('Sleepers Analysis')}
              {analysisData.sleepers.isError && renderErrorState('Sleepers Analysis', analysisData.sleepers.error)}
              {analysisData.sleepers.data && renderSleepersChart(
                analysisData.sleepers.data,
                'Sleepers Analysis'
              )}

              {/* Positional Ranks */}
              {analysisData.positionalRanks.isLoading && renderLoadingState('Positional Ranks')}
              {analysisData.positionalRanks.isError && renderErrorState('Positional Ranks', analysisData.positionalRanks.error)}
              {analysisData.positionalRanks.data && renderPositionalRanksChart(
                analysisData.positionalRanks.data,
                'Positional Ranks Through Draft'
              )}

              {/* Draft Injury */}
              {analysisData.draftInjury.isLoading && renderLoadingState('Draft Injury Analysis')}
              {analysisData.draftInjury.isError && renderErrorState('Draft Injury Analysis', analysisData.draftInjury.error)}
              {analysisData.draftInjury.data && renderDraftInjuryChart(
                analysisData.draftInjury.data,
                'Draft Injury Analysis'
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}; 