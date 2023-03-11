using System;
using System.Net;
using System.Net.NetworkInformation;

namespace frontend.util
{
    class NetworkUtil
    {
        public static int GetFreePort()
        {
            IPGlobalProperties ipGlobalProperties = IPGlobalProperties.GetIPGlobalProperties();

            // @TODO 空きポートを見つける
            IPEndPoint[] tcpConnInfoArray = ipGlobalProperties.GetActiveTcpListeners();

            int port = new Random().Next(1025, 65535);

            return port;
        }
    }
}
