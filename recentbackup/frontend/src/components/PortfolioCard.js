import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

const PortfolioCard = ({ title, stocks, performance }) => {
  return (
    <Paper style={{ padding: '1rem', height: '100%' }}>
      <Typography variant="h5" gutterBottom>
        {title}
      </Typography>
      
      <Typography variant="h6" gutterBottom>
        Performance Metrics
      </Typography>
      <List dense>
        <ListItem>
          <ListItemText 
            primary="Average Return" 
            secondary={`${(performance.average_return * 100).toFixed(2)}%`} 
          />
        </ListItem>
        <ListItem>
          <ListItemText 
            primary="Volatility" 
            secondary={`${(performance.volatility * 100).toFixed(2)}%`} 
          />
        </ListItem>
        <ListItem>
          <ListItemText 
            primary="Sharpe Ratio" 
            secondary={performance.sharpe_ratio.toFixed(2)} 
          />
        </ListItem>
      </List>
      
      <Divider style={{ margin: '1rem 0' }} />
      
      <Typography variant="h6" gutterBottom>
        Stocks
      </Typography>
      <List dense>
        {stocks.map((stock, index) => (
          <ListItem key={index}>
            <ListItemText primary={stock} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default PortfolioCard; 