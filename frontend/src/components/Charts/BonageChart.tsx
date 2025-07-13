import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { ChartData } from '../../services/types';
import { useResponsiveChart } from '../../hooks/useResponsiveChart';

interface BonageChartProps {
  data: ChartData;
  title: string;
}

export const BonageChart: React.FC<BonageChartProps> = ({ data, title }) => {
  const { fontSize, angle, height } = useResponsiveChart();

  if (!data || !data.teams || !data.bi || !data.weeks) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for stacked bar chart
  // Group by team and create stacked data
  const teamData: { [key: string]: any } = {};
  
  data.teams!.forEach((team, index) => {
    const week = data.weeks![index];
    const bi = data.bi![index];
    
    if (!teamData[team]) {
      teamData[team] = { team };
    }
    
    teamData[team][week] = bi;
  });

  const chartData = Object.values(teamData);

  // Get unique weeks for legend
  const uniqueWeeks = [...new Set(data.weeks!)];

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="w-full h-96">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="team" 
              angle={angle}
              textAnchor="end"
              height={height}
              interval={0}
              tick={{ fontSize }}
            />
            <YAxis 
              label={{ value: 'Strength of Schedule (BI)', angle: -90, position: 'insideLeft' }}
              tick={{ fontSize }}
            />
            <Tooltip formatter={(value) => [Number(value).toFixed(2), 'BI']} />
            {uniqueWeeks.map((week, index) => (
              <Bar 
                key={week}
                dataKey={week}
                stackId="a"
                fill={index % 2 === 0 ? '#574D68' : '#DDC9B4'}
                stroke="#000000"
                strokeWidth={1}
                name={week}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}; 