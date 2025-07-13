import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { ChartData } from '../../services/types';
import { useResponsiveChart } from '../../hooks/useResponsiveChart';

interface SleepersChartProps {
  data: ChartData;
  title: string;
}

export const SleepersChart: React.FC<SleepersChartProps> = ({ data, title }) => {
  const { fontSize } = useResponsiveChart();

  if (!data || !data.positions || !data.player_names || !data.sleeper_scores) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for bar chart
  const chartData = data.positions!.map((position, index) => ({
    position: position,
    player: data.player_names![index],
    sleeperScore: data.sleeper_scores![index]
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <div className="w-full h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="position" 
              name="Position"
              label={{ value: 'Position', position: 'bottom', offset: 0 }}
              tick={{ fontSize }}
            />
            <YAxis 
              dataKey="sleeperScore" 
              name="Sleeper Score"
              label={{ value: 'Sleeper Score', angle: -90, position: 'insideLeft' }}
              tick={{ fontSize }}
            />
            <Tooltip 
              formatter={(value) => [value, 'Sleeper Score']}
              labelFormatter={(label) => `${label}`}
            />
            <Bar 
              dataKey="sleeperScore" 
              fill="#574D68"
              stroke="#000000"
              strokeWidth={1}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}; 