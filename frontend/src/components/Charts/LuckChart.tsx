import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import type { ChartData } from '../../services/types';

interface LuckChartProps {
  data: ChartData;
  title: string;
  summary?: {
    l_prob?: number;
    u_prob?: number;
    perc_lucky?: number;
  };
}

export const LuckChart: React.FC<LuckChartProps> = ({ data, title, summary }) => {
  if (!data || !data.teams || !data.likelihood) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for bar chart
  const chartData = data.teams!.map((team, index) => ({
    team,
    likelihood: data.likelihood![index]
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      {summary && (
        <div className="mb-4 p-4 bg-gray-50 rounded-lg">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div className="min-w-0">
              <h4 className="font-medium text-gray-700">Luckiest Team</h4>
              <p className="text-2xl font-bold text-green-600">{summary.l_prob}%</p>
              <p className="text-sm text-gray-600">Likelihood of performing worse</p>
            </div>
            <div className="min-w-0">
              <h4 className="font-medium text-gray-700">Unluckiest Team</h4>
              <p className="text-2xl font-bold text-red-600">{summary.u_prob}%</p>
              <p className="text-sm text-gray-600">Likelihood of performing worse</p>
            </div>
            <div className="min-w-0">
              <h4 className="font-medium text-gray-700">Luck Gap</h4>
              <p className="text-2xl font-bold text-blue-600">{summary.perc_lucky}%</p>
              <p className="text-sm text-gray-600">Difference between teams</p>
            </div>
          </div>
        </div>
      )}
      
      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="team" 
              angle={-45}
              textAnchor="end"
              height={80}
              interval={0}
            />
            <YAxis />
            <Tooltip />
            <ReferenceLine y={50} stroke="red" strokeDasharray="3 3" label="Line of Luck" />
            <Bar 
              dataKey="likelihood"
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