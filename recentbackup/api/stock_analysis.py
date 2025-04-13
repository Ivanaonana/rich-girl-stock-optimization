import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple

class StockAnalyzer:
    def __init__(self):
        # Load historical data
        self.price_data = pd.read_csv('SNP 500 Price Data 2011-2020.csv', index_col=[0])
        self.price_data_cleaned = self.price_data.dropna(axis=1)
        
    def compute_log_returns(self) -> pd.DataFrame:
        """Compute log returns for the entire dataset."""
        return np.log(self.price_data_cleaned.shift(1)) - np.log(self.price_data_cleaned)
        
    def compute_correlation_matrix(self, log_returns: pd.DataFrame) -> pd.DataFrame:
        """Compute correlation matrix from log returns."""
        return log_returns.corr()
        
    def create_filtered_network(self, correlation_matrix: pd.DataFrame) -> nx.Graph:
        """Create and filter network using MST."""
        distance_matrix = np.sqrt(2 * (1 - correlation_matrix))
        distance_graph = nx.Graph(distance_matrix)
        return nx.minimum_spanning_tree(distance_graph)
        
    def compute_centrality_measures(self, graph: nx.Graph) -> Dict[str, Dict[str, float]]:
        """Compute various centrality measures for the network."""
        return {
            'degree': nx.degree_centrality(graph),
            'betweenness': nx.betweenness_centrality(graph),
            'closeness': nx.closeness_centrality(graph)
        }
        
    def get_portfolio_suggestions(self) -> Dict[str, List[str]]:
        """Get central and peripheral portfolio suggestions."""
        # Compute all necessary metrics
        log_returns = self.compute_log_returns()
        correlation_matrix = self.compute_correlation_matrix(log_returns)
        filtered_network = self.create_filtered_network(correlation_matrix)
        centrality_measures = self.compute_centrality_measures(filtered_network)
        
        # Combine centrality scores
        combined_scores = {}
        for stock in centrality_measures['degree'].keys():
            combined_scores[stock] = (
                centrality_measures['degree'][stock] + 
                centrality_measures['betweenness'][stock]
            ) / 2
            
        # Sort stocks by combined centrality
        sorted_stocks = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 15 central and bottom 15 peripheral stocks
        central_portfolio = [stock[0] for stock in sorted_stocks[:15]]
        peripheral_portfolio = [stock[0] for stock in sorted_stocks[-15:]]
        
        return {
            'central_portfolio': central_portfolio,
            'peripheral_portfolio': peripheral_portfolio
        }

    def get_portfolio_performance(self, portfolio: List[str]) -> Dict[str, float]:
        """Calculate portfolio performance metrics."""
        if not portfolio:
            return {}
            
        # Get relevant price data
        portfolio_data = self.price_data_cleaned[portfolio]
        
        # Calculate basic metrics
        returns = portfolio_data.pct_change()
        avg_return = returns.mean()
        volatility = returns.std()
        
        return {
            'average_return': float(avg_return.mean()),
            'volatility': float(volatility.mean()),
            'sharpe_ratio': float(avg_return.mean() / volatility.mean() if volatility.mean() != 0 else 0)
        } 