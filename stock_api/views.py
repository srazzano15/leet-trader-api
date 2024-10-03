from alpaca.data.requests import StockQuotesRequest, CryptoSnapshotRequest
from alpaca.data.timeframe import TimeFrame

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class StockDataView(APIView):
    def get(self, request, ticker):
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period="1d")  # You can adjust the period as needed

            # Check if stock data is available
            if stock_info.empty:
                return Response({"error": "No data found for the ticker"}, status=status.HTTP_404_NOT_FOUND)

            # Convert the index (which contains Timestamps) to strings and then convert the data to dict
            stock_info.index = stock_info.index.strftime('%Y-%m-%d %H:%M:%S')
            stock_data = stock_info.to_dict(orient="index")

            return Response(stock_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Error retrieving stock data", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
