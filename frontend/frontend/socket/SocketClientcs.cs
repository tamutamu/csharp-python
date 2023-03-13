using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace frontend
{
    internal class SocketClientcs
    {
        public static String Request(string body, int port)
        {
            Console.WriteLine($"[SendData] => {body}");

            // ソケット生成
            using (Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                //client.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), port));
                var clientDone = client.BeginConnect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), port), null, null);
                var ret = clientDone.AsyncWaitHandle.WaitOne(10000, true);
                if (!ret)
                {
                    //タイムアウトの例外
                    throw new SocketException(10060);
                }

                // 送るメッセージをUTF8タイプのbyte配列で変換する。
                var sendData = Encoding.UTF8.GetBytes(body);

                // 転送するデータの長さをbigエンディアンで変換してサーバで送る。(4byte)
                client.Send(BitConverter.GetBytes(sendData.Length));
                // データを転送する。
                client.Send(sendData);

                // データの長さを受信するための配列を生成する。(4byte)	
                var recvData = new byte[4];

                // データの長さを受信する。
                client.Receive(recvData, recvData.Length, SocketFlags.None);

                // serverでbigエンディアンを転送してもlittleエンディアンで受信される。bigエンディアンとlittleエンディアンは配列の順番が逆なのでreverseする。
                Array.Reverse(recvData);

                // データ長さでbyte配列を生成する。
                recvData = new byte[BitConverter.ToInt32(recvData, 0)];

                // データを受信する。
                client.Receive(recvData, recvData.Length, SocketFlags.None);

                // 受信したデータをUTF8エンコードでstringタイプに変換してコンソールに出力する。
                var returnData = Encoding.UTF8.GetString(recvData);
                Console.WriteLine($"[ReturnData] => {returnData}");

                return returnData;
            }

            // いずれかのキーを押下すると終了。
            //Console.WriteLine("Press any key...");
            //Console.ReadLine();
        }
    }
}
