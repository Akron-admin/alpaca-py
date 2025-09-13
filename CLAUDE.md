# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Alpaca-py is the official Python SDK for Alpaca APIs, providing access to trading, market data, and broker APIs. The SDK uses Poetry for dependency management and follows an OOP design with extensive use of Pydantic models for validation.

## Development Commands

### Setup
```bash
poetry install                    # Install dependencies
poetry run pre-commit install     # Setup pre-commit hooks
```

### Testing
```bash
poetry run pytest                 # Run all tests
poetry run pytest tests/broker/   # Run broker-specific tests
poetry run pytest tests/trading/  # Run trading-specific tests
poetry run pytest tests/data/     # Run data API tests
```

### Code Quality
```bash
poetry run black --check alpaca/ tests/  # Check formatting (lint)
poetry run black alpaca/ tests/          # Format code
```

### Documentation
```bash
./tools/scripts/generate-docs.sh  # Generate documentation
```

### Makefile shortcuts
```bash
make install    # Install dependencies
make test       # Run tests
make lint       # Check formatting
make generate   # Generate docs
```

## Architecture

### Core Structure
The SDK is organized into three main API modules:

1. **Broker API** (`alpaca.broker`): Account management, funding, rebalancing
   - `BrokerClient`: Main client for broker operations
   - Models in `alpaca.broker.models`
   - Requests in `alpaca.broker.requests`

2. **Trading API** (`alpaca.trading`): Order management, portfolio operations
   - `TradingClient`: Main client for trading operations
   - Models in `alpaca.trading.models`
   - Streaming via `alpaca.trading.stream`

3. **Data API** (`alpaca.data`): Historical and live market data
   - Asset-specific clients: `StockHistoricalDataClient`, `CryptoHistoricalDataClient`, `OptionHistoricalDataClient`, `NewsClient`
   - Live streaming: `StockDataStream`, `CryptoDataStream`, `OptionDataStream`
   - Models organized by data type in `alpaca.data.models`

### Common Components
- **`alpaca.common.rest.RESTClient`**: Base class for all API clients
- **`alpaca.common.models.ValidateBaseModel`**: Base Pydantic model with validation
- **`alpaca.common.models.NonEmptyRequest`**: Base for request models with `to_request_fields()` method
- **`alpaca.common.enums`**: Shared enums and constants

### Design Patterns
- **Request Objects**: All API methods use dedicated request classes (e.g., `GetOrdersRequest`, `CryptoBarsRequest`)
- **Pydantic Models**: Extensive use for validation, serialization, and type safety
- **Asset-Specific Clients**: Separate clients for different asset classes and data types
- **Streaming Support**: WebSocket and SSE clients for real-time data

### Testing
- Uses pytest with requests-mock for HTTP mocking
- Test factories in `tests/*/factories/` for generating test data
- Async testing support via pytest-asyncio
- Client fixtures in `conftest.py` for consistent test setup

## Key Conventions

### Model Development
- All models must extend `ValidateBaseModel` for response models
- Request models must extend `NonEmptyRequest` which provides `to_request_fields()` method
- Use Pydantic validators for custom validation logic

### Method Naming
Request methods follow the pattern: `{verb}_{noun}_by_{value}` or `{verb}_{noun1}_(for|from|to)_{noun2}`

Examples:
- `remove_symbol_from_watchlist_by_id()`
- `get_crypto_bars()`
- `create_order()`

### URL Parameters vs Request Bodies
- URL parameters become individual method parameters
- Query/body parameters are grouped into request objects
- This ensures type safety and validation while maintaining clean method signatures