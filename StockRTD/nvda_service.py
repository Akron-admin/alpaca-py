#!/usr/bin/env python3
"""
NVDA Price Service - Continuously updates data for C# RTD server
This runs as a background service, polling Alpaca API every 5 seconds
"""

import os
import json
import tempfile
import time
import sys
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest, StockLatestQuoteRequest
from alpaca.data.enums import DataFeed

class NvdaPriceService:
    def __init__(self):
        # Get API credentials
        self.api_key = os.environ.get('ALPACA_API_KEY')
        self.secret_key = os.environ.get('ALPACA_SECRET_KEY')
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables")
        
        # Initialize client
        self.client = StockHistoricalDataClient(
            api_key=self.api_key,
            secret_key=self.secret_key
        )
        
        # File path for RTD communication
        self.rtd_file_path = os.path.join(tempfile.gettempdir(), "nvda_price_data.json")
        self.running = True
        
        print(f"NVDA Price Service initialized")
        print(f"Data file: {self.rtd_file_path}")
        print("Press Ctrl+C to stop the service")

    def fetch_nvda_data(self):
        """Fetch latest NVDA data from Alpaca API"""
        try:
            # Get latest trade
            trade_request = StockLatestTradeRequest(
                symbol_or_symbols="NVDA",
                feed=DataFeed.IEX
            )
            latest_trade = self.client.get_stock_latest_trade(trade_request)
            trade_data = latest_trade["NVDA"]

            # Get latest quote
            quote_request = StockLatestQuoteRequest(
                symbol_or_symbols="NVDA",
                feed=DataFeed.IEX
            )
            latest_quote = self.client.get_stock_latest_quote(quote_request)
            quote_data = latest_quote["NVDA"]

            # Prepare data for RTD
            data = {
                "BidPrice": float(quote_data.bid_price),
                "AskPrice": float(quote_data.ask_price),
                "LastPrice": float(trade_data.price),
                "Timestamp": str(quote_data.timestamp),
                "UpdateTime": datetime.now().isoformat()
            }

            return data

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def save_data(self, data):
        """Save data to JSON file for RTD server"""
        try:
            with open(self.rtd_file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def run(self, update_interval=5):
        """Run the service continuously"""
        print(f"\nStarting service with {update_interval} second intervals...")
        
        while self.running:
            try:
                # Fetch new data
                data = self.fetch_nvda_data()
                
                if data:
                    # Save to file
                    if self.save_data(data):
                        print(f"{datetime.now().strftime('%H:%M:%S')} - Updated: "
                              f"Bid=${data['BidPrice']:.2f}, Ask=${data['AskPrice']:.2f}, "
                              f"Last=${data['LastPrice']:.2f}")
                    else:
                        print(f"{datetime.now().strftime('%H:%M:%S')} - Failed to save data")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - Failed to fetch data")
                
                # Wait for next update
                time.sleep(update_interval)
                
            except KeyboardInterrupt:
                print("\nShutting down service...")
                self.running = False
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(update_interval)

def main():
    try:
        service = NvdaPriceService()
        
        # Check if update interval is provided
        update_interval = 5
        if len(sys.argv) > 1:
            try:
                update_interval = int(sys.argv[1])
                if update_interval < 1:
                    update_interval = 1
                    print("Minimum update interval is 1 second")
            except ValueError:
                print("Invalid interval, using default 5 seconds")
        
        service.run(update_interval)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set your API keys first:")
        print("export ALPACA_API_KEY='your_key'")
        print("export ALPACA_SECRET_KEY='your_secret'")
    except Exception as e:
        print(f"Service error: {e}")

if __name__ == "__main__":
    main()