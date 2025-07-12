import { Link } from 'react-router-dom';

export const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Fantasy Football Analysis
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Advanced analytics and insights for your fantasy football league
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
        {/* Setup League Card */}
        <div className="card">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 ml-4">Setup League</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Connect your ESPN or Sleeper league to start analyzing your fantasy football data.
          </p>
          <Link to="/setup" className="btn-primary inline-block">
            Get Started
          </Link>
        </div>

        {/* Analysis Card */}
        <div className="card">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 ml-4">Analysis</h3>
          </div>
          <p className="text-gray-600 mb-4">
            View detailed analytics including expected wins, luck analysis, and draft insights.
          </p>
          <Link to="/analysis" className="btn-primary inline-block">
            View Analysis
          </Link>
        </div>

        {/* Features Card */}
        <div className="card">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 ml-4">Features</h3>
          </div>
          <p className="text-gray-600 mb-4">
            Advanced analytics including expected wins, consistency analysis, and draft insights.
          </p>
          <div className="text-sm text-gray-500">
            <ul className="space-y-1">
              <li>• Expected Wins Analysis</li>
              <li>• Luck & Consistency Metrics</li>
              <li>• Draft Performance Insights</li>
              <li>• Real-time Progress Tracking</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Supported Platforms</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">ESPN</h3>
            <p className="text-gray-600">
              Full support for ESPN fantasy football leagues with authentication.
            </p>
          </div>
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Sleeper</h3>
            <p className="text-gray-600">
              Complete integration with Sleeper fantasy football platform.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}; 