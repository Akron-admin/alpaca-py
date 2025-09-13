# Stock RTD Server for Excel

Real-time stock data in Excel using C# RTD server and Python data service.

## 🏗️ Architecture

**Python Service** (`nvda_service.py`) → **JSON File** → **C# RTD Server** → **Excel**

## 📦 Setup Requirements

### Prerequisites
- **.NET 8.0 SDK** or later
- **Python 3.8+** with alpaca-py
- **Excel** (Windows only)
- **Alpaca API keys**

### VS Code Extensions (Recommended)
- C# for Visual Studio Code
- Python

## 🚀 Build Instructions

### 1. Set Environment Variables
```bash
export ALPACA_API_KEY="your_key_here"
export ALPACA_SECRET_KEY="your_secret_here"
```

### 2. Build C# RTD Server
```bash
cd StockRTD
dotnet build --configuration Release
```

### 3. Register COM Component (Windows)
Run as **Administrator**:
```cmd
build.bat
```

Or manually:
```cmd
regasm bin\Release\net8.0-windows\StockRTD.dll /codebase /tlb
```

## 🏃‍♂️ Running the System

### 1. Start Python Data Service
```bash
python nvda_service.py
# or with custom interval (seconds)
python nvda_service.py 3
```

### 2. Use in Excel
Add these formulas to Excel cells:

```excel
=RTD("StockRTD.Server",,"BID")      // Current bid price
=RTD("StockRTD.Server",,"ASK")      // Current ask price  
=RTD("StockRTD.Server",,"LAST")     // Last trade price
=RTD("StockRTD.Server",,"TIMESTAMP") // Last update time
```

## 📁 Project Files

- **`StockRtdServer.cs`** - Main RTD server implementation
- **`nvda_service.py`** - Background Python service for data fetching
- **`build.bat`** - Build and register script
- **`unregister.bat`** - Unregister COM component

## 🔧 Configuration

### Data Update Frequency
- **Python service**: Default 5 seconds (configurable)
- **RTD server**: Checks for updates every 1 second
- **Excel**: Updates when RTD notifies of changes

### Data Communication
- Uses temporary JSON file: `%TEMP%\nvda_price_data.json`
- Python writes, C# reads
- Thread-safe with proper error handling

## 🐛 Troubleshooting

### COM Registration Issues
```cmd
# Run as Administrator
regasm /unregister bin\Release\net8.0-windows\StockRTD.dll
regasm bin\Release\net8.0-windows\StockRTD.dll /codebase /tlb
```

### Excel RTD Not Working
1. Check if COM component is registered
2. Verify Python service is running
3. Check data file exists: `%TEMP%\nvda_price_data.json`
4. Restart Excel

### Python Service Issues
- Verify API keys are set
- Check network connectivity
- Ensure alpaca-py is installed: `pip install alpaca-py`

## 🔒 Security Notes
- API keys stored in environment variables only
- No hardcoded credentials in source code
- Local file communication (no network exposure)

## 🚧 Limitations
- **Windows only** (COM requirement)
- **IEX feed only** (BOATS requires subscription upgrade)
- **Market hours** data availability depends on exchange
- **Single symbol** (NVDA only - can be extended)

## 🎯 Future Enhancements
- Multiple symbol support
- BOATS feed integration
- Real-time streaming (WebSocket)
- Advanced error handling
- Configuration file support