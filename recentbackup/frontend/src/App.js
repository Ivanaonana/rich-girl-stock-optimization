import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';
import PortfolioCard from './components/PortfolioCard';
import PerformanceChart from './components/PerformanceChart';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8001/api/analysis/');
        setData(response.data);
        setLoading(false);
      } catch (err) {
        console.error('API Error:', err);  // Add detailed error logging
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Container style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Typography color="error">Error: {error}</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
      <Typography variant="h3" gutterBottom>
        Stock Portfolio Analysis
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <PortfolioCard 
            title="Central Portfolio" 
            stocks={data?.portfolios?.central_portfolio || []}
            performance={data?.performance?.central || {}}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <PortfolioCard 
            title="Peripheral Portfolio" 
            stocks={data?.portfolios?.peripheral_portfolio || []}
            performance={data?.performance?.peripheral || {}}
          />
        </Grid>
        <Grid item xs={12}>
          <Paper style={{ padding: '1rem' }}>
            <Typography variant="h5" gutterBottom>Performance Comparison</Typography>
            <PerformanceChart 
              centralPerformance={data?.performance?.central}
              peripheralPerformance={data?.performance?.peripheral}
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
