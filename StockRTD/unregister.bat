@echo off
echo Unregistering Stock RTD Server...

regasm bin\Release\net8.0-windows\StockRTD.dll /unregister

echo Unregistration complete!
pause