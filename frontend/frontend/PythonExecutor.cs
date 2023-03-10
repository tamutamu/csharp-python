using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.NetworkInformation;
using System.Text;

namespace frontend
{
    internal class PythonExecutor
    {
        private static int GetFreePort()
        {
            IPGlobalProperties ipGlobalProperties = IPGlobalProperties.GetIPGlobalProperties();
            IPEndPoint[] tcpConnInfoArray = ipGlobalProperties.GetActiveTcpListeners();

            int port = new Random().Next(1025, 65535);

            return port;
        }

        public String FileName { get; set; }
        public String WorkingDirectory { get; set; }
        public String Arguments { get; set; }
        public String InputString { get; set; }
        public String StandardOutput { get; set; }
        public int ExitCode { get; set; }

        private StringBuilder standardOutputStringBuilder = new StringBuilder();

        public PythonExecutor()
        {
        }

        public void Execute()
        {
            ProcessStartInfo psInfo = new ProcessStartInfo();
            psInfo.FileName = this.FileName;
            psInfo.WorkingDirectory = this.WorkingDirectory;
            psInfo.Arguments = this.Arguments;

            psInfo.CreateNoWindow = true;
            psInfo.UseShellExecute = false;
            psInfo.RedirectStandardInput = true;
            psInfo.RedirectStandardOutput = true;
            psInfo.RedirectStandardError = true;

            // Process p = Process.Start(psInfo);
            Process p = new System.Diagnostics.Process();
            p.StartInfo = psInfo;
            p.OutputDataReceived += p_OutputDataReceived;
            p.ErrorDataReceived += p_ErrorDataReceived;

            // プロセスの実行
            p.Start();

            // 標準入力への書き込み
            using (StreamWriter sw = p.StandardInput)
            {
                sw.Write(InputString);
            }

            //非同期で出力とエラーの読み取りを開始
            p.BeginOutputReadLine();
            p.BeginErrorReadLine();

            // 終わるまでまつ
            p.WaitForExit();
            this.ExitCode = p.ExitCode;
            this.StandardOutput = standardOutputStringBuilder.ToString();
        }

        /// <summary>
        /// 標準出力データを受け取った時の処理
        /// </summary>
        void p_OutputDataReceived(object sender,
            System.Diagnostics.DataReceivedEventArgs e)
        {
            //processMessage(sender, e);
            if (e != null && e.Data != null && e.Data.Length > 0)
            {
                standardOutputStringBuilder.Append(e.Data + "\n");
                Console.WriteLine(standardOutputStringBuilder.ToString());
            }
        }

        /// <summary>
        /// 標準エラーを受け取った時の処理
        /// </summary>
        void p_ErrorDataReceived(object sender,
            System.Diagnostics.DataReceivedEventArgs e)
        {
             Console.WriteLine(e.ToString());
        }
    }
}
