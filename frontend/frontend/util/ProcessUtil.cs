using System;
using System.Diagnostics;
using System.Text;

namespace frontend.util
{
    internal class ProcessUtil
    {
        public String FileName { get; set; }
        public String WorkingDirectory { get; set; }
        public String Arguments { get; set; }
        public String InputString { get; set; }
        public String StandardOutput { get; set; }
        public int ExitCode { get; set; }
        private Process process { get; set; }

        private StringBuilder standardOutputStringBuilder = new StringBuilder();

        public ProcessUtil()
        {
        }
        public int Exit()
        {
            this.process.Kill();
            process.WaitForExit();
            this.ExitCode = process.ExitCode;
            return this.ExitCode;
        }

        public void Execute(bool daemon = false)
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
            process = new System.Diagnostics.Process();
            process.StartInfo = psInfo;
            process.OutputDataReceived += p_OutputDataReceived;
            process.ErrorDataReceived += p_ErrorDataReceived;

            // プロセスの実行
            process.Start();

            // 標準入力への書き込み
            //using (StreamWriter sw = p.StandardInput)
            //{
            //    sw.Write(InputString);
            //}

            //非同期で出力とエラーの読み取りを開始
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            if (daemon)
            {
                // 終わるまでまつ
                process.WaitForExit();
                this.ExitCode = process.ExitCode;
                this.StandardOutput = standardOutputStringBuilder.ToString();
            }
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
