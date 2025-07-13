import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { ChartData } from '../../services/types';
import { useResponsiveChart } from '../../hooks/useResponsiveChart';

interface EWDifferenceChartProps {
  data: ChartData;
  title: string;
  summary?: {
    lucky_name?: string;
    l_total_wins?: number;
    l_total_ex_wins?: number;
    l_ew_diff?: number;
    unlucky_name?: string;
    u_total_wins?: number;
    u_total_ex_wins?: number;
    u_ew_diff?: number;
  };
}

export const EWDifferenceChart: React.FC<EWDifferenceChartProps> = ({ data, title, summary }) => {
  const { fontSize, angle, height } = useResponsiveChart();

  if (!data || !data.teams || !data.ew_difference) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for bar chart
  const chartData = data.teams!.map((team, index) => ({
    team,
    ew_difference: data.ew_difference![index]
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      {summary && (
        <div className="mb-4 p-4 bg-gray-50 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="min-w-0">
              <h4 className="font-medium text-green-700 truncate">Lucky Team: {summary.lucky_name}</h4>
              <p className="text-sm text-gray-600 break-words">
                Total Wins: {summary.l_total_wins} | Expected: {summary.l_total_ex_wins}
              </p>
              <p className="text-sm text-green-600">Difference: +{summary.l_ew_diff}</p>
            </div>
            <div className="min-w-0">
              <h4 className="font-medium text-red-700 truncate">Unlucky Team: {summary.unlucky_name}</h4>
              <p className="text-sm text-gray-600 break-words">
                Total Wins: {summary.u_total_wins} | Expected: {summary.u_total_ex_wins}
              </p>
              <p className="text-sm text-red-600">Difference: {summary.u_ew_diff}</p>
            </div>
          </div>
        </div>
      )}
      
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
              label={{ value: 'Wins - Expected Wins', angle: -90, position: 'insideLeft' }}
              tick={{ fontSize }}
            />
            <Tooltip formatter={(value) => [Number(value).toFixed(2), 'EW Difference']} />
            <Bar 
              dataKey="ew_difference"
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