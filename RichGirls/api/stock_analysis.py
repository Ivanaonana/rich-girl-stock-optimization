import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class StockAnalyzer:
    def __init__(self):
        try:
            # Get the absolute path to the data files
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            historical_file = os.path.join(base_dir, 'SNP 500 Price Data 2011-2020.csv')
            validation_file = os.path.join(base_dir, 'SNP 500 Price Data 2021.csv')
            
            # Load historical training data (2011-2020)
            logger.info(f"Loading historical data from {historical_file}")
            self.historical_data = pd.read_csv(historical_file, index_col=[0])
            self.historical_data_cleaned = self.historical_data.dropna(axis=1)
            
            # Load validation data (2021)
            logger.info(f"Loading validation data from {validation_file}")
            self.validation_data = pd.read_csv(validation_file, index_col=[0])
            self.validation_data_cleaned = self.validation_data.dropna(axis=1)
            
            logger.info("Data loaded successfully")
            logger.info(f"Historical data shape: {self.historical_data_cleaned.shape}")
            logger.info(f"Validation data shape: {self.validation_data_cleaned.shape}")
            
        except FileNotFoundError as e:
            logger.error(f"Could not find data file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
        
    def get_year_wise_data(self, year: int) -> pd.DataFrame:
        """Get data for a specific year."""
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        return self.historical_data_cleaned.loc[start_date:end_date]
        
    def compute_log_returns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Compute log returns for the dataset."""
        return np.log(data.shift(1)) - np.log(data)
        
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
            'closeness': nx.closeness_centrality(graph),
            'eigenvector': nx.eigenvector_centrality_numpy(graph)
        }
        
    def compute_distance_criteria(self, graph: nx.Graph, correlation_matrix: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Compute the three distance criteria from the paper."""
        # 1. Distance on degree criterion
        degree_centrality = nx.degree_centrality(graph)
        node_with_largest_degree = max(degree_centrality, key=degree_centrality.get)
        distance_degree = {node: nx.shortest_path_length(graph, node, node_with_largest_degree) 
                         for node in graph.nodes()}
        
        # 2. Distance on correlation criterion
        sum_correlation = {}
        for node in graph.nodes():
            neighbors = list(graph.neighbors(node))
            sum_correlation[node] = sum(correlation_matrix[node][neighbor] for neighbor in neighbors)
        node_with_highest_correlation = max(sum_correlation, key=sum_correlation.get)
        distance_correlation = {node: nx.shortest_path_length(graph, node, node_with_highest_correlation) 
                              for node in graph.nodes()}
        
        # 3. Distance on distance criterion
        mean_distances = {}
        for node in graph.nodes():
            other_nodes = list(graph.nodes())
            other_nodes.remove(node)
            distances = [nx.shortest_path_length(graph, node, other) for other in other_nodes]
            mean_distances[node] = np.mean(distances)
        node_with_minimum_mean_distance = min(mean_distances, key=mean_distances.get)
        distance_distance = {node: nx.shortest_path_length(graph, node, node_with_minimum_mean_distance) 
                           for node in graph.nodes()}
        
        return {
            'degree': distance_degree,
            'correlation': distance_correlation,
            'distance': distance_distance
        }
        
    def get_portfolio_suggestions(self) -> Dict[str, List[str]]:
        """Get central and peripheral portfolio suggestions using the original algorithm criteria."""
        # Analyze each year from 2011-2020
        all_centrality_scores = {}
        all_distance_scores = {}
        
        for year in range(2011, 2021):
            yearly_data = self.get_year_wise_data(year)
            log_returns = self.compute_log_returns(yearly_data)
            correlation_matrix = self.compute_correlation_matrix(log_returns)
            filtered_network = self.create_filtered_network(correlation_matrix)
            
            # Get centrality measures
            centrality_measures = self.compute_centrality_measures(filtered_network)
            
            # For each stock, check if it meets the criteria
            for stock in filtered_network.nodes():
                if stock not in all_centrality_scores:
                    all_centrality_scores[stock] = {'central_years': 0, 'peripheral_years': 0}
                
                degree = centrality_measures['degree'][stock]
                betweenness = centrality_measures['betweenness'][stock]
                
                # Central criteria: in top 10% of either degree or betweenness
                degree_threshold = np.percentile(list(centrality_measures['degree'].values()), 90)
                betweenness_threshold = np.percentile(list(centrality_measures['betweenness'].values()), 90)
                
                if degree >= degree_threshold or betweenness >= betweenness_threshold:
                    all_centrality_scores[stock]['central_years'] += 1
                
                # Peripheral criteria: degree equals 1 or betweenness equals 0
                if degree == min(centrality_measures['degree'].values()) or betweenness == 0:
                    all_centrality_scores[stock]['peripheral_years'] += 1
        
        # Select stocks that meet criteria in majority of years
        central_portfolio = []
        peripheral_portfolio = []
        min_years_threshold = 5  # Stock must meet criteria in at least 5 years
        
        for stock, scores in all_centrality_scores.items():
            if scores['central_years'] >= min_years_threshold:
                central_portfolio.append(stock)
            if scores['peripheral_years'] >= min_years_threshold:
                peripheral_portfolio.append(stock)
        
        # If we have too few stocks, take the top/bottom 15
        if len(central_portfolio) < 15 or len(peripheral_portfolio) < 15:
            # Calculate average centrality scores
            avg_centrality = {}
            avg_peripherality = {}
            
            for stock, scores in all_centrality_scores.items():
                avg_centrality[stock] = scores['central_years'] / 10  # 10 years total
                avg_peripherality[stock] = scores['peripheral_years'] / 10
            
            # Sort stocks by scores
            sorted_central = sorted(avg_centrality.items(), key=lambda x: x[1], reverse=True)
            sorted_peripheral = sorted(avg_peripherality.items(), key=lambda x: x[1], reverse=True)
            
            central_portfolio = [stock for stock, _ in sorted_central[:15]]
            peripheral_portfolio = [stock for stock, _ in sorted_peripheral[:15]]
        
        return {
            'central_portfolio': central_portfolio,
            'peripheral_portfolio': peripheral_portfolio
        }

    def calculate_portfolio_returns(self, portfolio: List[str], data: pd.DataFrame) -> pd.Series:
        """Calculate equal-weighted portfolio returns."""
        if not portfolio or not all(stock in data.columns for stock in portfolio):
            return pd.Series(0, index=data.index)
        
        portfolio_data = data[portfolio]
        portfolio_returns = portfolio_data.pct_change()
        return portfolio_returns.mean(axis=1)  # Equal-weighted portfolio

    def get_portfolio_performance(self, portfolio: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate portfolio performance metrics for each year."""
        if not portfolio:
            return {}

        performance_data = {
            'yearly': {},
            'validation': {}  # 2021 data
        }

        # Calculate yearly performance (2011-2020)
        for year in range(2011, 2021):
            yearly_data = self.get_year_wise_data(year)
            yearly_returns = self.calculate_portfolio_returns(portfolio, yearly_data)
            
            avg_return = yearly_returns.mean()
            volatility = yearly_returns.std()
            sharpe = avg_return / volatility if volatility != 0 else 0
            
            performance_data['yearly'][str(year)] = {
                'average_return': float(avg_return),
                'volatility': float(volatility),
                'sharpe_ratio': float(sharpe)
            }

        # Calculate validation performance (2021)
        validation_returns = self.calculate_portfolio_returns(portfolio, self.validation_data_cleaned)
        validation_avg_return = validation_returns.mean()
        validation_volatility = validation_returns.std()
        validation_sharpe = validation_avg_return / validation_volatility if validation_volatility != 0 else 0

        performance_data['validation'] = {
            'average_return': float(validation_avg_return),
            'volatility': float(validation_volatility),
            'sharpe_ratio': float(validation_sharpe)
        }

        return performance_data 