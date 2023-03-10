using System;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text;

namespace frontend
{
    internal class SocketClientcs
    {
        public static String request(string body, int port)
        {
            // ソケット生成
            using (Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                // Connect関数でローカル(127.0.0.1)のポート番号9999で待機するソケットに接続する。
                client.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), port));
                // 送るメッセージをUTF8タイプのbyte配列で変換する。
                var data = Encoding.UTF8.GetBytes(body);

                // 転送するデータの長さをbigエンディアンで変換してサーバで送る。(4byte)
                client.Send(BitConverter.GetBytes(data.Length));
                // データを転送する。
                client.Send(data);

                // データの長さを受信するための配列を生成する。(4byte)	
                data = new byte[4];
                // データの長さを受信する。
                client.Receive(data, data.Length, SocketFlags.None);
                // serverでbigエンディアンを転送してもlittleエンディアンで受信される。bigエンディアンとlittleエンディアンは配列の順番が逆なのでreverseする。
                Array.Reverse(data);
                // データ長さでbyte配列を生成する。
                data = new byte[BitConverter.ToInt32(data, 0)];
                // データを受信する。
                client.Receive(data, data.Length, SocketFlags.None);
                // 受信したデータをUTF8エンコードでstringタイプに変換してコンソールに出力する。
                Console.WriteLine(Encoding.UTF8.GetString(data));
            }

            // いずれかのキーを押下すると終了。
            //Console.WriteLine("Press any key...");
            //Console.ReadLine();

            return "";
        }
    }
}
