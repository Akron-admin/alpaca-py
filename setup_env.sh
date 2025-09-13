#!/bin/bash
# Setup script for Alpaca API environment variables

echo "Setting up Alpaca API environment variables..."
echo

# Check if .env file exists
if [ -f ".env" ]; then
    echo "Found .env file, loading environment variables..."
    export $(cat .env | xargs)
else
    echo "No .env file found. You can either:"
    echo "1. Copy .env.example to .env and fill in your keys:"
    echo "   cp .env.example .env"
    echo "   # Then edit .env with your actual API keys"
    echo
    echo "2. Or set environment variables directly:"
    echo "   export ALPACA_API_KEY='your_key_here'"
    echo "   export ALPACA_SECRET_KEY='your_secret_here'"
    echo
fi

# Check if environment variables are set
if [ -z "$ALPACA_API_KEY" ] || [ -z "$ALPACA_SECRET_KEY" ]; then
    echo "⚠️  Environment variables not set!"
    echo "Please set ALPACA_API_KEY and ALPACA_SECRET_KEY"
    echo
    echo "You can get your API keys from:"
    echo "• Paper trading: https://app.alpaca.markets/paper/dashboard/overview"
    echo "• Live trading: https://app.alpaca.markets/live/dashboard/overview"
else
    echo "✅ Environment variables are set!"
    echo "ALPACA_API_KEY: ${ALPACA_API_KEY:0:8}..."
    echo "ALPACA_SECRET_KEY: ${ALPACA_SECRET_KEY:0:8}..."
fi