from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stock_analysis import StockAnalyzer

# Create your views here.

class StockAnalysisView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = StockAnalyzer()

    def get(self, request):
        try:
            # Get portfolio suggestions
            portfolios = self.analyzer.get_portfolio_suggestions()
            
            # Get performance metrics for each portfolio
            central_performance = self.analyzer.get_portfolio_performance(portfolios['central_portfolio'])
            peripheral_performance = self.analyzer.get_portfolio_performance(portfolios['peripheral_portfolio'])
            
            return Response({
                'portfolios': portfolios,
                'performance': {
                    'central': central_performance,
                    'peripheral': peripheral_performance
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
