using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Threading;
using System.IO;
using Newtonsoft.Json;

namespace StockRTD
{
    // RTD Server Interface - Required by Excel
    [ComVisible(true)]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IRtdServer
    {
        int ServerStart(IRTDUpdateEvent CallbackObject);
        object ConnectData(int TopicID, ref Array Strings, ref bool GetNewValues);
        void DisconnectData(int TopicID);
        int Heartbeat();
        Array RefreshData(ref int TopicCount);
        void ServerTerminate();
    }

    // RTD Update Event Interface - Excel callback
    [ComVisible(true)]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IRTDUpdateEvent
    {
        void UpdateNotify();
    }

    // Data structure for NVDA price information
    public class NvdaData
    {
        public decimal BidPrice { get; set; }
        public decimal AskPrice { get; set; }
        public string Timestamp { get; set; }
        public decimal LastPrice { get; set; }
    }

    // Main RTD Server Implementation
    [ComVisible(true)]
    [ClassInterface(ClassInterfaceType.None)]
    [ProgId("StockRTD.Server")]
    [Guid("12345678-1234-1234-1234-123456789ABC")]
    public class StockRtdServer : IRtdServer
    {
        private IRTDUpdateEvent _callbackObject;
        private Dictionary<int, string> _topics;
        private Timer _timer;
        private NvdaData _lastData;
        private readonly string _dataFilePath;
        private bool _isActive;

        public StockRtdServer()
        {
            _topics = new Dictionary<int, string>();
            // Path to shared data file (Python service will write here)
            _dataFilePath = Path.Combine(Path.GetTempPath(), "nvda_price_data.json");
            _lastData = new NvdaData();
        }

        public int ServerStart(IRTDUpdateEvent CallbackObject)
        {
            _callbackObject = CallbackObject;
            _isActive = true;

            // Start timer to check for data updates every 1 second
            _timer = new Timer(CheckForUpdates, null, 0, 1000);
            
            return 1; // Success
        }

        public object ConnectData(int TopicID, ref Array Strings, ref bool GetNewValues)
        {
            if (Strings.Length > 0)
            {
                string topicName = Strings.GetValue(0).ToString().ToUpper();
                _topics[TopicID] = topicName;

                // Return current value based on topic
                switch (topicName)
                {
                    case "BID":
                        return _lastData.BidPrice;
                    case "ASK":
                        return _lastData.AskPrice;
                    case "TIMESTAMP":
                        return _lastData.Timestamp ?? "N/A";
                    case "LAST":
                        return _lastData.LastPrice;
                    default:
                        return "Invalid Topic";
                }
            }

            GetNewValues = false;
            return "No Topic";
        }

        public void DisconnectData(int TopicID)
        {
            if (_topics.ContainsKey(TopicID))
            {
                _topics.Remove(TopicID);
            }
        }

        public int Heartbeat()
        {
            return 1; // Server is alive
        }

        public Array RefreshData(ref int TopicCount)
        {
            if (_topics.Count == 0)
            {
                TopicCount = 0;
                return null;
            }

            // Prepare data array for Excel
            object[,] data = new object[2, _topics.Count];
            int index = 0;

            foreach (var topic in _topics)
            {
                data[0, index] = topic.Key; // Topic ID
                
                // Get current value for this topic
                switch (topic.Value)
                {
                    case "BID":
                        data[1, index] = _lastData.BidPrice;
                        break;
                    case "ASK":
                        data[1, index] = _lastData.AskPrice;
                        break;
                    case "TIMESTAMP":
                        data[1, index] = _lastData.Timestamp ?? "N/A";
                        break;
                    case "LAST":
                        data[1, index] = _lastData.LastPrice;
                        break;
                    default:
                        data[1, index] = "Invalid Topic";
                        break;
                }
                
                index++;
            }

            TopicCount = _topics.Count;
            return data;
        }

        public void ServerTerminate()
        {
            _isActive = false;
            _timer?.Dispose();
            _callbackObject = null;
        }

        private void CheckForUpdates(object state)
        {
            if (!_isActive || _callbackObject == null)
                return;

            try
            {
                // Check if data file exists and read it
                if (File.Exists(_dataFilePath))
                {
                    string jsonContent = File.ReadAllText(_dataFilePath);
                    var newData = JsonConvert.DeserializeObject<NvdaData>(jsonContent);

                    // Check if data has changed
                    if (newData != null && HasDataChanged(newData))
                    {
                        _lastData = newData;
                        // Notify Excel that data has been updated
                        _callbackObject.UpdateNotify();
                    }
                }
            }
            catch (Exception ex)
            {
                // Log error (in production, use proper logging)
                System.Diagnostics.Debug.WriteLine($"RTD Error: {ex.Message}");
            }
        }

        private bool HasDataChanged(NvdaData newData)
        {
            return newData.BidPrice != _lastData.BidPrice ||
                   newData.AskPrice != _lastData.AskPrice ||
                   newData.LastPrice != _lastData.LastPrice ||
                   newData.Timestamp != _lastData.Timestamp;
        }
    }

    // COM Registration Helper
    [ComVisible(false)]
    public static class ComRegistration
    {
        [ComRegisterFunction]
        public static void RegisterFunction(Type type)
        {
            // Registry entries will be handled by regasm
        }

        [ComUnregisterFunction]
        public static void UnregisterFunction(Type type)
        {
            // Cleanup registry entries
        }
    }
}