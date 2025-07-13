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
      <div className="w-full h-[28rem]">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="avg_points" 
              name="Average Points Per Week"
              type="number"
              label={{ value: 'Average Points Per Week', position: 'bottom', offset: -7 }}
              domain={['dataMin - 5', 'dataMax + 5']}
              tickFormatter={(value) => Math.round(value).toString()}
            />
            <YAxis 
              dataKey="consistency_score" 
              name="Consistency Score"
              type="number"
              label={{ value: 'Consistency Score (%)', angle: -90, position: 'insideLeft' }}
              domain={['dataMin - 5', 'dataMax + 5']}
              tickFormatter={(value) => Math.round(value).toString()}
            />
            <ZAxis dataKey="team" />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
                      <p className="font-medium">{data.team}</p>
                      <p className="text-sm text-gray-600">
                        Average Points: {Number(data.avg_points).toFixed(2)}
                      </p>
                      <p className="text-sm text-gray-600">
                        Consistency Score: {Number(data.consistency_score).toFixed(2)}%
                      </p>
                    </div>
                  );
                }
                return null;
              }}
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