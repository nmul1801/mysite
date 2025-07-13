import React from 'react';
import type { ChartData } from '../../services/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface PositionalRanksChartProps {
  data: ChartData;
  title: string;
}

export const PositionalRanksChart: React.FC<PositionalRanksChartProps> = ({ data, title }) => {
  if (!data || !data.draft_rounds || !data.avg_positional_ranks) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for the chart
  const chartData = data.draft_rounds.map((round, index) => ({
    round: `Round ${round}`,
    avgRank: data.avg_positional_ranks?.[index] || 0
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="mb-4 text-sm text-gray-600">
        <p>
          For each round of drafting, take the average positional rank of all players drafted in that round.
          If your league drafted accurately, this line should have a positive slope.
        </p>
      </div>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="round" 
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              label={{ value: 'Average Positional Rank', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip 
              formatter={(value) => [Number(value).toFixed(2), 'Average Positional Rank']}
              labelFormatter={(label) => `${label}`}
            />
            <Line 
              type="monotone" 
              dataKey="avgRank" 
              stroke="#574D68" 
              strokeWidth={3}
              dot={{ fill: '#574D68', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#574D68', strokeWidth: 2, fill: '#DDC9B4' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}; 