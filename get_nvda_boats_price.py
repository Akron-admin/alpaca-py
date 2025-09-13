#!/usr/bin/env python3
"""
Get NVDA last price from BOATS feed using Alpaca-py
"""

import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest, StockLatestQuoteRequest
from alpaca.data.enums import DataFeed

def main():
    # Get API credentials from environment variables
    api_key = os.environ.get('ALPACA_API_KEY')
    secret_key = os.environ.get('ALPACA_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("Error: Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables")
        print("Example:")
        print("export ALPACA_API_KEY='your_key_here'")
        print("export ALPACA_SECRET_KEY='your_secret_here'")
        return
    
    print("Connecting to Alpaca Market Data API...")
    
    # Initialize the stock historical data client
    client = StockHistoricalDataClient(
        api_key=api_key,
        secret_key=secret_key
    )
    
    try:
        # Get latest trade from standard feed (IEX - free tier)
        print("Fetching NVDA latest trade from IEX feed...")
        trade_request = StockLatestTradeRequest(
            symbol_or_symbols="NVDA",
            feed=DataFeed.IEX  # IEX feed (should work with basic subscription)
        )
        
        latest_trade = client.get_stock_latest_trade(trade_request)
        trade_data = latest_trade["NVDA"]
        
        print(f"\n=== NVDA Latest Trade (IEX Feed) ===")
        print(f"Price: ${trade_data.price}")
        print(f"Size: {trade_data.size} shares")
        print(f"Timestamp: {trade_data.timestamp}")
        print(f"Exchange: {trade_data.exchange}")
        
        # Also get latest quote for bid/ask spread
        print("\nFetching NVDA latest quote from IEX feed...")
        quote_request = StockLatestQuoteRequest(
            symbol_or_symbols="NVDA",
            feed=DataFeed.IEX
        )
        
        latest_quote = client.get_stock_latest_quote(quote_request)
        quote_data = latest_quote["NVDA"]
        
        print(f"\n=== NVDA Latest Quote (IEX Feed) ===")
        print(f"Bid Price: ${quote_data.bid_price}")
        print(f"Ask Price: ${quote_data.ask_price}")
        print(f"Bid Size: {quote_data.bid_size}")
        print(f"Ask Size: {quote_data.ask_size}")
        print(f"Timestamp: {quote_data.timestamp}")
        
        # Calculate spread
        spread = quote_data.ask_price - quote_data.bid_price
        print(f"Spread: ${spread:.4f}")
        
        # BOATS feed version (commented out - requires special subscription)
        # To use BOATS feed, uncomment the following and comment out the IEX version above:
        """
        # Get latest trade from BOATS feed
        print("Fetching NVDA latest trade from BOATS feed...")
        trade_request = StockLatestTradeRequest(
            symbol_or_symbols="NVDA",
            feed=DataFeed.BOATS  # Blue Ocean ATS feed - requires subscription
        )
        
        latest_trade = client.get_stock_latest_trade(trade_request)
        trade_data = latest_trade["NVDA"]
        
        print(f"\n=== NVDA Latest Trade (BOATS Feed) ===")
        print(f"Price: ${trade_data.price}")
        print(f"Size: {trade_data.size} shares")
        print(f"Timestamp: {trade_data.timestamp}")
        print(f"Exchange: {trade_data.exchange}")
        
        # Also get latest quote for bid/ask spread
        print("\nFetching NVDA latest quote from BOATS feed...")
        quote_request = StockLatestQuoteRequest(
            symbol_or_symbols="NVDA",
            feed=DataFeed.BOATS
        )
        
        latest_quote = client.get_stock_latest_quote(quote_request)
        quote_data = latest_quote["NVDA"]
        
        print(f"\n=== NVDA Latest Quote (BOATS Feed) ===")
        print(f"Bid Price: ${quote_data.bid_price}")
        print(f"Ask Price: ${quote_data.ask_price}")
        print(f"Bid Size: {quote_data.bid_size}")
        print(f"Ask Size: {quote_data.ask_size}")
        print(f"Timestamp: {quote_data.timestamp}")
        
        # Calculate spread
        spread = quote_data.ask_price - quote_data.bid_price
        print(f"Spread: ${spread:.4f}")
        """
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Note: BOATS feed may require special data subscription")

if __name__ == "__main__":
    main()