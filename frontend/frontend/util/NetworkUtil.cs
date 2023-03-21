using System.Net;
using System.Net.Sockets;

namespace frontend.util
{
    class NetworkUtil
    {
        public static int GetFreePort()
        {
            //IPGlobalProperties ipGlobalProperties = IPGlobalProperties.GetIPGlobalProperties();
            //// @TODO 空きポートを見つける
            //IPEndPoint[] tcpConnInfoArray = ipGlobalProperties.GetActiveTcpListeners();
            //int port = new Random().Next(1025, 65535);
            //return port;

            TcpListener l = new TcpListener(IPAddress.Loopback, 0);
            l.Start();
            int port = ((IPEndPoint)l.LocalEndpoint).Port;
            l.Stop();
            return port;
        }
    }
}
