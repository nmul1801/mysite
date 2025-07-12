import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useLeagueAssembly } from '../hooks/useLeagueAssembly';
import { ProgressBar } from '../components/ProgressBar/ProgressBar';
import type { LeagueAssemblyRequest } from '../services/types';
import toast from 'react-hot-toast';

export const SetupLeague = () => {
  const [selectedPlatform, setSelectedPlatform] = useState<'espn' | 'sleeper'>('sleeper');
  const { streamingAssembly, progress, isLoading } = useLeagueAssembly();
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors }, setValue } = useForm<LeagueAssemblyRequest>();

  // Set the platform when it changes
  const handlePlatformChange = (platform: 'espn' | 'sleeper') => {
    setSelectedPlatform(platform);
    setValue('platform', platform);
  };

  const onSubmit = async (data: LeagueAssemblyRequest) => {
    try {
      await streamingAssembly(data);
      toast.success('League assembly completed successfully!');
      
      // Redirect to analysis page with the league ID
      navigate(`/analysis?leagueId=${data.league_id}`);
    } catch (error) {
      toast.error('Failed to assemble league. Please try again.');
      console.error('Assembly error:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Setup Your League</h1>
        <p className="text-lg text-gray-600">
          Connect your fantasy football league to start analyzing performance, luck, and draft strategies.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Setup Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">League Information</h2>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Platform Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Platform
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => handlePlatformChange('sleeper')}
                  className={`p-4 border-2 rounded-lg text-center transition-colors ${
                    selectedPlatform === 'sleeper'
                      ? 'border-primary-600 bg-primary-50 text-primary-700'
                      : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                  }`}
                >
                  <div className="font-semibold">Sleeper</div>
                  <div className="text-sm text-gray-500">No authentication required</div>
                </button>
                <button
                  type="button"
                  onClick={() => handlePlatformChange('espn')}
                  className={`p-4 border-2 rounded-lg text-center transition-colors ${
                    selectedPlatform === 'espn'
                      ? 'border-primary-600 bg-primary-50 text-primary-700'
                      : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                  }`}
                >
                  <div className="font-semibold">ESPN</div>
                  <div className="text-sm text-gray-500">Requires authentication</div>
                </button>
              </div>
            </div>

            {/* Hidden platform field */}
            <input type="hidden" {...register('platform')} value={selectedPlatform} />

            {/* League ID */}
            <div>
              <label htmlFor="league_id" className="block text-sm font-medium text-gray-700 mb-2">
                League ID
              </label>
              <input
                {...register('league_id', { required: 'League ID is required' })}
                type="text"
                id="league_id"
                className="input-field"
                placeholder={selectedPlatform === 'sleeper' ? 'e.g., 1103905062545362944' : 'e.g., 64612107'}
              />
              {errors.league_id && (
                <p className="mt-1 text-sm text-red-600">{errors.league_id.message}</p>
              )}
            </div>

            {/* ESPN Authentication Fields */}
            {selectedPlatform === 'espn' && (
              <>
                <div>
                  <label htmlFor="s2" className="block text-sm font-medium text-gray-700 mb-2">
                    ESPN S2 Token
                  </label>
                  <input
                    {...register('s2')}
                    type="text"
                    id="s2"
                    className="input-field"
                    placeholder="Your ESPN S2 token"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Optional: Required for private leagues
                  </p>
                </div>

                <div>
                  <label htmlFor="swid" className="block text-sm font-medium text-gray-700 mb-2">
                    ESPN SWID
                  </label>
                  <input
                    {...register('swid')}
                    type="text"
                    id="swid"
                    className="input-field"
                    placeholder="Your ESPN SWID"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Optional: Required for private leagues
                  </p>
                </div>
              </>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Processing League...' : 'Process League'}
            </button>
          </form>
        </div>

        {/* Progress and Instructions */}
        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Processing Status</h3>
            <ProgressBar progress={progress} />
          </div>

          {/* Instructions */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">How to Find Your League ID</h3>
            
            {selectedPlatform === 'sleeper' ? (
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Sleeper League ID</h4>
                  <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                    <li>Open your Sleeper league in a web browser</li>
                    <li>Look at the URL: <code className="bg-gray-100 px-1 rounded">https://sleeper.app/league/LEAGUE_ID</code></li>
                    <li>Copy the number after <code className="bg-gray-100 px-1 rounded">/league/</code></li>
                  </ol>
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    <strong>Note:</strong> Sleeper leagues are public, so no authentication is required.
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">ESPN League ID</h4>
                  <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                    <li>Open your ESPN league in a web browser</li>
                    <li>Look at the URL: <code className="bg-gray-100 px-1 rounded">https://fantasy.espn.com/football/league?leagueId=LEAGUE_ID</code></li>
                    <li>Copy the number after <code className="bg-gray-100 px-1 rounded">leagueId=</code></li>
                  </ol>
                </div>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm text-yellow-800">
                    <strong>Note:</strong> For private ESPN leagues, you'll need to provide S2 and SWID tokens.
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Test Data */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Test</h3>
            <p className="text-sm text-gray-600 mb-4">
              Try one of these test leagues to see the analysis in action:
            </p>
            <div className="space-y-2">
              <button
                onClick={() => {
                  const testData: LeagueAssemblyRequest = {
                    platform: 'sleeper',
                    league_id: '1103905062545362944'
                  };
                  streamingAssembly(testData).then(() => {
                    navigate(`/analysis?leagueId=${testData.league_id}`);
                  });
                }}
                disabled={isLoading}
                className="btn-secondary w-full text-sm"
              >
                Test Sleeper League
              </button>
              <button
                onClick={() => {
                  const testData: LeagueAssemblyRequest = {
                    platform: 'espn',
                    league_id: '64612107',
                    s2: 'AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D',
                    swid: 'F71F32C4-9869-4DFB-A620-ADD15AA67520'
                  };
                  streamingAssembly(testData).then(() => {
                    navigate(`/analysis?leagueId=${testData.league_id}`);
                  });
                }}
                disabled={isLoading}
                className="btn-secondary w-full text-sm"
              >
                Test ESPN League
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 