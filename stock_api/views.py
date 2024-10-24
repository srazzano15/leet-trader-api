from alpaca.data.requests import MarketMoversRequest
from alpaca.data.historical.screener import ScreenerClient
import asyncio
import yfinance as yf

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import re


ALPACA_API_KEY_ID = 'PKXVKQTFW701A3PJAPBQ'
ALPACA_API_SECRET_KEY = 'LfaD2SZnbjrZMhuGNrnMHU8zWFJGNBO2LuwghaEE'


def extract_domain(url):
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1)
    else:
        return None

def validate_keys(query, keys_list):
    l = query #if type(query) is 'list' else list(query)
    for key in l:
        if key not in keys_list:
            return False
    return True

def warrant_filter(ticker):
    ticker_keys = ticker.keys()

    # filters prior to fetching yfinance data
    if '.' in ticker['symbol']:
        return False
    elif len(ticker['symbol']) > 4:
        return False
    elif ticker['price'] < 0.01:
        return False

    # filters post fetching yfinance data
    pattern = r'(1x|2x|ETF)'
    if validate_keys(['name'], ticker_keys):
        matches = re.findall(pattern, ticker['name'], re.IGNORECASE)
        if len(matches) > 0:
            return False

    if validate_keys(['website'], ticker_keys) and not validate_keys(['name'], ticker_keys):
        return False

    return True

def calculate_percent_change(previous_close, current_price):
    if current_price > previous_close:
        return round((current_price / previous_close - 1) * 100, 2)
    else:
        return round(100 * (current_price / previous_close) - 100, 2)

class StockMoversView(APIView):
    def get(self, request):
        client = ScreenerClient(api_key=ALPACA_API_KEY_ID, secret_key=ALPACA_API_SECRET_KEY)
        try:
            # Fetch default Stock data view for non-authorized users
            movers_data = client.get_market_movers(request_params=MarketMoversRequest(top=50))
            # format data better
            movers = dict(movers_data)
            tickers = [dict(pair) for pair in movers['gainers']]
            tickers.extend([dict(pair) for pair in movers['losers']])
            filtered = list(filter(warrant_filter, tickers))
            for ticker in filtered:
                try:
                    stock = yf.Ticker(ticker['symbol'])
                    info_keys = stock.info.keys()
                    fast_info_keys = stock.fast_info.keys()
                    if validate_keys(['shortName'], info_keys) or validate_keys(['longName'], info_keys):
                        ticker['name'] = stock.info['shortName'] if validate_keys('shortName', info_keys) else stock.info[
                            'longName']
                    if validate_keys(['website'], info_keys):
                        domain = extract_domain(stock.info['website'])
                        ticker['logo'] = f'https://cdn.brandfetch.io/{domain}/icon/fallback/lettermark/'
                    else:
                        ticker['logo'] = f'https://cdn.brandfetch.io/{ticker['symbol']}{ticker['symbol']}.com/icon/fallback/lettermark/'

                    if validate_keys(['previousClose', 'lastPrice'], fast_info_keys):
                        ticker['percent_change'] = calculate_percent_change(
                            stock.fast_info['previousClose'],
                            stock.fast_info['lastPrice']
                        )
                        ticker['price'] = round(stock.fast_info['lastPrice'], 3)

                except:
                    continue

            data = {
                'tickers': filter(warrant_filter, filtered)
                # 'losers': [dict(pair) for pair in movers['losers']]
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed retrieving stock data", 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

