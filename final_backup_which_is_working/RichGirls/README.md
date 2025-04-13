# Stock Portfolio Analysis Web App

This web application analyzes S&P 500 stocks using network analysis to suggest central and peripheral portfolios. It uses Django for the backend API and React for the frontend interface.

## Features

- Network analysis of S&P 500 stocks
- Portfolio suggestions based on centrality measures
- Performance metrics visualization
- Interactive UI with real-time updates

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

## Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the Django backend:
   ```bash
   python manage.py runserver
   ```

2. Start the React frontend (in a new terminal):
   ```bash
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Project Structure

- `/api` - Django backend API
- `/frontend` - React frontend application
- `/data` - Stock data files

## Data Sources

The application uses historical S&P 500 data from 2011-2020 for analysis. The data is stored in CSV format in the data directory.

## Algorithm

The portfolio suggestion algorithm uses the following steps:
1. Compute log returns for stocks
2. Create correlation matrix
3. Build and filter network using Minimum Spanning Tree
4. Calculate centrality measures
5. Select stocks based on centrality scores

## Performance Metrics

The application calculates the following metrics for each portfolio:
- Average Return
- Volatility
- Sharpe Ratio 