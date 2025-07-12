import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis } from 'recharts';
import type { ChartData } from '../../services/types';

interface ConsistencyChartProps {
  data: ChartData;
  title: string;
}

export const ConsistencyChart: React.FC<ConsistencyChartProps> = ({ data, title }) => {
  if (!data || !data.teams || !data.consistency_scores || !data.avg_points) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">No chart data available</p>
      </div>
    );
  }

  // Transform data for scatter chart
  const chartData = data.teams!.map((team, index) => ({
    team,
    consistency_score: data.consistency_scores![index],
    avg_points: data.avg_points![index]
  }));

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="avg_points" 
              name="Average Points Per Week"
              type="number"
            />
            <YAxis 
              dataKey="consistency_score" 
              name="Consistency Score"
              type="number"
            />
            <ZAxis dataKey="team" />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }}
              formatter={(value, name, props) => [
                `${props.payload.team}: ${value}`,
                name === 'consistency_score' ? 'Consistency Score' : 'Average Points'
              ]}
            />
            <Scatter 
              dataKey="consistency_score" 
              fill="#574D68"
              stroke="#000000"
              strokeWidth={1}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}; 