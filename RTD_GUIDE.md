# RTD (Real-Time Data) Guide

## 🚀 Quick Start Guide

### Prerequisites (New Computer Setup):

**Required Software:**
- **Windows** (COM/RTD is Windows-only)
- **Microsoft Excel** (any recent version)
- **.NET 8.0 SDK** - [Download from Microsoft](https://dotnet.microsoft.com/download) or `winget install Microsoft.DotNet.SDK.8`
- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/) or `winget install Python.Python.3.12`
- **Git** (optional) - For cloning repository

**Python Packages:**
```bash
pip install alpaca-py
```

**Environment Variables:**
```bash
# Set your Alpaca API credentials
set ALPACA_API_KEY=your_key_here
set ALPACA_SECRET_KEY=your_secret_here
```

**Development Tools (Optional):**
- **VS Code** with C# and Python extensions
- **Visual Studio Community** (alternative to VS Code)

---

### To Use Our StockRTD Server:

```bash
# 1. Build the RTD server
cd StockRTD
dotnet build --configuration Release

# 2. Register COM (Windows, as Administrator)
build.bat

# 3. Start Python service
python nvda_service.py

# 4. In Excel, use:
=RTD("StockRTD.Server",,"BID")
=RTD("StockRTD.Server",,"ASK")
=RTD("StockRTD.Server",,"LAST")
=RTD("StockRTD.Server",,"TIMESTAMP")
```

---

## 📋 What is RTD?

**RTD (Real-Time Data)** is Excel's native mechanism for receiving live, continuously updating data from external sources. Unlike static formulas, RTD functions automatically refresh when the underlying data changes.

## 🎯 How RTD Works

### Architecture Flow
```
External Data Source → RTD Server → Excel RTD Function → Excel Cell
```

1. **RTD Server**: A COM component that fetches and manages live data
2. **Excel RTD Function**: Built-in Excel function that connects to RTD servers
3. **Automatic Updates**: Excel refreshes cells when RTD server notifies of changes

### RTD vs Other Methods

| Method | Updates | Performance | Complexity | Platform |
|--------|---------|-------------|------------|----------|
| **RTD** | Automatic | High | Medium | Windows Only |
| **xlwings** | Manual/Timer | Medium | Low | Cross-platform |
| **VBA + API** | Timer-based | Low | High | Windows Only |
| **Power Query** | Refresh-based | Medium | Low | Cross-platform |

## 🔧 RTD Function Syntax

### Basic RTD Formula
```excel
=RTD("ProgID", Server, Topic1, Topic2, ...)
```

### Parameters
- **ProgID**: Unique identifier of the RTD server (e.g., `"StockRTD.Server"`)
- **Server**: Usually empty (`""`) for local servers
- **Topics**: Parameters that specify what data to retrieve

### Our Stock RTD Examples
```excel
=RTD("StockRTD.Server",,"BID")       // Get bid price
=RTD("StockRTD.Server",,"ASK")       // Get ask price
=RTD("StockRTD.Server",,"LAST")      // Get last trade price
=RTD("StockRTD.Server",,"TIMESTAMP") // Get update timestamp
```

## 🏗️ RTD Server Requirements

### COM Interface Implementation
An RTD server must implement the `IRtdServer` interface:

```csharp
public interface IRtdServer
{
    int ServerStart(IRTDUpdateEvent CallbackObject);     // Initialize
    object ConnectData(int TopicID, ref Array Strings, ref bool GetNewValues); // Subscribe
    void DisconnectData(int TopicID);                    // Unsubscribe
    int Heartbeat();                                     // Health check
    Array RefreshData(ref int TopicCount);               // Send updates
    void ServerTerminate();                              // Cleanup
}
```

### Registration
RTD servers must be registered as COM components:
```cmd
regasm YourRtdServer.dll /codebase /tlb
```

## 📊 Excel RTD Usage Patterns

### Simple Data Display
```excel
A1: =RTD("StockRTD.Server",,"BID")
A2: =RTD("StockRTD.Server",,"ASK")
A3: =RTD("StockRTD.Server",,"LAST")
```

### Calculated Fields
```excel
A1: =RTD("StockRTD.Server",,"BID")      // 142.50
A2: =RTD("StockRTD.Server",,"ASK")      // 142.55
A3: =A2-A1                              // Spread: 0.05
A4: =(A1+A2)/2                         // Mid price: 142.525
```

### Conditional Formatting
Use RTD values to trigger color changes:
- Green when price > previous price
- Red when price < previous price
- Yellow when spread > threshold

### Charts and Graphs
RTD data can feed into Excel charts for real-time visualization:
- Time series price charts
- Bid/ask spread monitoring
- Volume indicators

## 🔄 Update Mechanisms

### Push vs Pull
- **RTD (Push)**: Server notifies Excel when data changes
- **Traditional (Pull)**: Excel requests data on a schedule

### Update Flow
1. RTD server detects data change
2. Server calls `CallbackObject.UpdateNotify()`
3. Excel calls `RefreshData()` to get new values
4. Excel updates affected cells automatically
5. Dependent formulas recalculate

## ⚡ Performance Considerations

### Optimization Tips
- **Batch updates**: Send multiple changes in one `RefreshData()` call
- **Change detection**: Only notify when data actually changes
- **Throttling**: Limit update frequency (e.g., max 10/second)
- **Selective updates**: Only refresh subscribed topics

### Memory Management
- Properly implement `DisconnectData()` for cleanup
- Avoid memory leaks in background threads
- Dispose of resources in `ServerTerminate()`

## 🐛 Common Issues & Solutions

### RTD Not Working
**Problem**: Formula shows `#N/A` or doesn't update
**Solutions**:
- Check COM registration: `regasm /unregister` then re-register
- Verify RTD server is running
- Restart Excel
- Check Windows Registry for ProgID

### Slow Updates
**Problem**: Data updates are delayed
**Solutions**:
- Reduce update throttling interval
- Optimize data source queries
- Check network latency
- Verify `UpdateNotify()` is being called

### Excel Crashes
**Problem**: Excel becomes unstable
**Solutions**:
- Add proper exception handling in RTD server
- Test COM registration with simple test server
- Check for threading issues
- Validate all data types returned to Excel

## 🔒 Security & Deployment

### Security Considerations
- RTD servers run with Excel's security context
- Validate all input data
- Avoid exposing sensitive information
- Use proper authentication for external data sources

### Deployment Options
- **Local installation**: Register COM on each machine
- **Network deployment**: Use ClickOnce or MSI installers
- **Corporate deployment**: Group Policy or SCCM

## 🎯 Best Practices

### Design Patterns
1. **Separation of concerns**: Keep data fetching separate from Excel interface
2. **Error handling**: Graceful degradation when data sources fail
3. **Configuration**: External config files for server settings
4. **Logging**: Debug information for troubleshooting

### Development Workflow
1. **Start simple**: Basic RTD server with hardcoded data
2. **Add data source**: Connect to real data provider
3. **Implement caching**: Avoid redundant API calls
4. **Add error handling**: Handle network failures gracefully
5. **Performance testing**: Verify updates under load

## 🌟 Advanced Features

### Multiple Symbols
```excel
=RTD("StockRTD.Server",,"NVDA","BID")
=RTD("StockRTD.Server",,"AAPL","BID") 
=RTD("StockRTD.Server",,"MSFT","BID")
```

### Historical Data
```excel
=RTD("StockRTD.Server",,"NVDA","PRICE","1MIN")  // 1-minute ago
=RTD("StockRTD.Server",,"NVDA","PRICE","5MIN")  // 5-minutes ago
```

### Calculated Fields
```excel
=RTD("StockRTD.Server",,"NVDA","RSI")           // Technical indicators
=RTD("StockRTD.Server",,"NVDA","MACD")          // Moving averages
```

## 📚 Resources

### Microsoft Documentation
- [RTD Function Reference](https://docs.microsoft.com/en-us/office/client-developer/excel/rtd-function)
- [Creating RTD Servers](https://docs.microsoft.com/en-us/office/client-developer/excel/creating-rtd-servers)

### Development Tools
- **Visual Studio**: Full RTD project templates
- **VS Code**: Manual setup but works fine
- **Excel Developer Tab**: Enable for RTD testing

### Testing Tools
- **RTD Monitor**: Excel add-in for debugging RTD connections
- **Process Monitor**: Track file/registry access
- **Event Viewer**: Windows logs for COM errors

## 🚀 Our Implementation

Our **StockRTD** server demonstrates:
- ✅ **Clean architecture**: Python data service + C# RTD server
- ✅ **Real-time updates**: Sub-second refresh rates
- ✅ **Error handling**: Graceful failure modes
- ✅ **Easy deployment**: Automated build/register scripts
- ✅ **Extensible design**: Ready for multiple symbols/feeds

Ready to bring real-time market data directly into Excel! 📈