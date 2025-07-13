import React, { useState } from 'react';
import type { ChartData } from '../../services/types';

interface DraftInjuryTableProps {
  data: ChartData;
  title: string;
}

interface PickData {
  name: string;
  percent_inj: number;
  id: string;
  bg_color: string;
}

export const DraftInjuryTable: React.FC<DraftInjuryTableProps> = ({ data, title }) => {
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);

  if (!data || !data.draft_injury_data) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Handle the data structure - it could be the new format with team names or the old format
  const injuryData = data.draft_injury_data as any;
  let draftData: any;
  let teamNames: string[] = [];

  if (injuryData.draft_data && injuryData.team_names) {
    // New format with team names
    draftData = injuryData.draft_data;
    teamNames = injuryData.team_names;
  } else {
    // Old format - just the draft data
    draftData = injuryData;
    teamNames = [];
  }

  // The data structure is: { round_number: [team_picks_array] }
  // Each team_picks_array contains arrays of picks for each team
  const rounds = Object.keys(draftData).sort((a, b) => parseInt(a) - parseInt(b));
  const firstRound = draftData[rounds[0]];
  const teamCount = firstRound ? firstRound.length : 0;

  // Use provided team names or fall back to generic names
  const displayTeamNames = teamNames.length > 0 ? teamNames : 
    Array.from({ length: teamCount }, (_, index) => `Team ${index + 1}`);

  const handleCellClick = (pick: PickData) => {
    if (activeTooltip === pick.id) {
      setActiveTooltip(null);
    } else {
      setActiveTooltip(pick.id);
    }
  };

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="mb-4 text-sm text-gray-600">
        <p>
          The table below measures how injured each roster's draft class was throughout the season. Each 
          column represents a roster slot, and each row represents a draft round. Each cell has the picture
          of the player associated with that particular draft pick, as well as a background color representing
          a players inactivity. A player with a green background was mostly active, while a player with a red
          background missed a significant amount of the season. Clicking on a player's cell will display their 
          name, and the percentage of the season they were inactive.
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300" style={{ tableLayout: 'fixed' }}>
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-xs" style={{ width: '80px', writingMode: 'vertical-lr', textOrientation: 'mixed' }}>Round</th>
              {displayTeamNames.map((teamName, index) => (
                <th key={index} className="border border-gray-300 px-2 py-2 text-center font-semibold text-xs" style={{ writingMode: 'vertical-lr', textOrientation: 'mixed' }}>
                  {teamName}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rounds.map((roundNum) => {
              const roundPicks = draftData[roundNum];
              return roundPicks.map((pickRow: (PickData | null)[], rowIndex: number) => (
                <tr key={`${roundNum}-${rowIndex}`} className="hover:bg-gray-50">
                  {rowIndex === 0 && (
                    <td 
                      className="border border-gray-300 px-4 py-2 font-semibold text-center align-middle" 
                      rowSpan={roundPicks.length}
                      style={{ width: '80px' }}
                    >
                      {roundNum}
                    </td>
                  )}
                  {pickRow.map((pick, colIndex) => (
                    <td key={colIndex} className="border border-gray-300 p-0 relative">
                      {pick ? (
                        <div
                          className="cursor-pointer relative w-full h-full"
                          onClick={() => handleCellClick(pick)}
                          style={{
                            backgroundColor: pick.bg_color,
                            minHeight: '60px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}
                        >
                          <img 
                            className="w-full h-full object-cover"
                            src={`https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/${pick.id}.png&w=48&h=35&cb=1`}
                            alt={pick.name}
                            onError={(e) => {
                              // Fallback to a placeholder if image fails to load
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                          
                          {/* Tooltip */}
                          {activeTooltip === pick.id && (
                            <div className="absolute z-10 bg-gray-800 text-white text-xs rounded px-2 py-1 whitespace-nowrap"
                                 style={{
                                   bottom: '100%',
                                   left: '50%',
                                   transform: 'translateX(-50%)',
                                   marginBottom: '5px'
                                 }}>
                              {pick.name}, missed {pick.percent_inj}% of games
                              <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="w-full h-16"></div>
                      )}
                    </td>
                  ))}
                </tr>
              ));
            })}
          </tbody>
        </table>
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p><strong>Color Legend:</strong></p>
        <div className="flex flex-wrap gap-4 mt-2">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
            <span>Low Injury Risk (Green)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-500 rounded mr-2"></div>
            <span>Medium Injury Risk (Yellow)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
            <span>High Injury Risk (Red)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-black rounded mr-2"></div>
            <span>Very High Injury Risk (Black)</span>
          </div>
        </div>
      </div>
    </div>
  );
}; 