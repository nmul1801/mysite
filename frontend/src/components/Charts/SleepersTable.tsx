import React from 'react';
import type { ChartData } from '../../services/types';

interface SleepersTableProps {
  data: ChartData;
  title: string;
}

export const SleepersTable: React.FC<SleepersTableProps> = ({ data, title }) => {
  if (!data || !data.positions || !data.player_names || !data.sleeper_scores) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for table
  const tableData = data.positions!.map((position, index) => ({
    position: position,
    playerName: data.player_names![index],
    sleeperScore: data.sleeper_scores![index],
    playerId: data.player_ids?.[index] || '',
    positionPick: data.position_picks?.[index] || 0,
    positionalRank: data.positional_ranks?.[index] || 0,
    firstInitial: data.first_initials?.[index] || '',
    lastName: data.last_names?.[index] || ''
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="mb-4 text-sm text-gray-600">
        <p>
          <strong>Sleeper Score (SS)</strong> is calculated by taking a player's Position Pick (PP) and subtracting their 
          Positional Rank (PR). This measures their difference in their perceived value (PP) and their actual value (PR).
          Players with a high sleeper score were thought to be poor-performing and turned out to perform well.
        </p>
        <p className="mt-2">
          For example, {tableData[0]?.playerName} was the <strong>{tableData[0]?.positionPick} {tableData[0]?.position}</strong> drafted.
          He ended up scoring the <strong>{tableData[0]?.positionalRank}</strong> most among his position, giving
          him a sleeper score of <strong>{tableData[0]?.sleeperScore}</strong>.
        </p>
        <p className="mt-2 text-gray-500">Note that this is not a good metric for dynasty leagues</p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm">Pos</th>
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm" colSpan={2}>Name</th>
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm">PP</th>
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm">PR</th>
              <th className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm">SS</th>
            </tr>
          </thead>
          <tbody>
            {tableData.map((row, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-2 py-2 text-center text-sm">
                  {row.position}
                </td>
                <td className="border border-gray-300 px-1 py-2 text-center">
                  <img 
                    className="w-12 h-9 object-cover rounded"
                    src={`https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/${row.playerId}.png&w=48&h=35&cb=1`}
                    alt={row.playerName}
                    onError={(e) => {
                      // Fallback to a placeholder if image fails to load
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                </td>
                <td className="border border-gray-300 px-2 py-2 text-left text-sm min-w-0">
                  <div className="truncate">
                    {row.firstInitial} {row.lastName}
                  </div>
                </td>
                <td className="border border-gray-300 px-2 py-2 text-center text-sm">
                  {row.positionPick}
                </td>
                <td className="border border-gray-300 px-2 py-2 text-center text-sm">
                  {row.positionalRank}
                </td>
                <td className="border border-gray-300 px-2 py-2 text-center font-semibold text-sm">
                  {row.sleeperScore}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}; 