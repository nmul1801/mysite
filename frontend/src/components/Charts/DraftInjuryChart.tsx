import React from 'react';

interface DraftInjuryChartProps {
  data: any; // Draft injury data is complex nested structure
  title: string;
}

export const DraftInjuryChart: React.FC<DraftInjuryChartProps> = ({ data, title }) => {
  if (!data || typeof data !== 'object') {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Extract team names and rounds from the data
  const rounds = Object.keys(data).sort((a, b) => parseInt(a) - parseInt(b));
  const teamIds = Object.keys(data[rounds[0]] || {});

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Round</th>
              {teamIds.map((teamId) => (
                <th key={teamId} className="border border-gray-300 px-4 py-2 text-center font-semibold">
                  Team {teamId}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rounds.map((round) => (
              <tr key={round} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2 font-semibold">
                  {round}
                </td>
                {teamIds.map((teamId) => {
                  const picks = data[round][teamId];
                  return (
                    <td key={teamId} className="border border-gray-300 px-2 py-1">
                      {picks && picks.length > 0 ? (
                        picks.map((pick: any, index: number) => (
                          pick ? (
                            <div
                              key={index}
                              className="text-xs p-1 mb-1 rounded"
                              style={{
                                backgroundColor: pick.bg_color || '#f3f4f6',
                                color: pick.bg_color === 'black' ? 'white' : 'black'
                              }}
                            >
                              <div className="font-medium">{pick.name}</div>
                              <div className="text-xs opacity-75">
                                {pick.percent_inj}% injured
                              </div>
                            </div>
                          ) : (
                            <div key={index} className="text-xs text-gray-400 p-1">
                              -
                            </div>
                          )
                        ))
                      ) : (
                        <div className="text-xs text-gray-400 p-1">-</div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p><strong>Color Legend:</strong></p>
        <div className="flex flex-wrap gap-2 mt-2">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-500 rounded mr-1"></div>
            <span>Low Injury Risk</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-500 rounded mr-1"></div>
            <span>Medium Injury Risk</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-500 rounded mr-1"></div>
            <span>High Injury Risk</span>
          </div>
        </div>
      </div>
    </div>
  );
}; 