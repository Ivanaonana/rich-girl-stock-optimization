import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PerformanceChart = ({ centralPerformance, peripheralPerformance }) => {
  const data = [
    {
      name: 'Average Return',
      Central: centralPerformance?.average_return * 100 || 0,
      Peripheral: peripheralPerformance?.average_return * 100 || 0,
    },
    {
      name: 'Volatility',
      Central: centralPerformance?.volatility * 100 || 0,
      Peripheral: peripheralPerformance?.volatility * 100 || 0,
    },
    {
      name: 'Sharpe Ratio',
      Central: centralPerformance?.sharpe_ratio || 0,
      Peripheral: peripheralPerformance?.sharpe_ratio || 0,
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip 
          formatter={(value) => value.toFixed(2) + (value !== data[2].Central ? '%' : '')}
        />
        <Legend />
        <Bar dataKey="Central" fill="#8884d8" />
        <Bar dataKey="Peripheral" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default PerformanceChart; 