@echo off
echo Building Stock RTD Server...

REM Build the project
dotnet build --configuration Release

REM Register COM component
echo Registering COM component...
regasm bin\Release\net8.0-windows\StockRTD.dll /codebase /tlb

echo.
echo Build and registration complete!
echo.
echo To use in Excel, use these formulas:
echo =RTD("StockRTD.Server",,"BID")
echo =RTD("StockRTD.Server",,"ASK") 
echo =RTD("StockRTD.Server",,"LAST")
echo =RTD("StockRTD.Server",,"TIMESTAMP")
echo.
pause