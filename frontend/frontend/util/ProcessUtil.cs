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

        public DataReceivedEventHandler OupputDataReceivedEventHandler { get; set; }
        public DataReceivedEventHandler ErrorDataReceivedEventHandler { get; set; }
        public EventHandler ExitEventHandler { get; set; }

        public int ExitCode { get; set; }
        private Process process { get; set; }

        private StringBuilder standardOutputStringBuilder = new StringBuilder();

        public ProcessUtil()
        {
        }
        public int Exit()
        {
            this.process.CloseMainWindow();
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

#if DEBUG
            psInfo.CreateNoWindow = false;
#else 
            psInfo.CreateNoWindow = true;
#endif
            psInfo.UseShellExecute = false;
            psInfo.RedirectStandardInput = true;
            psInfo.RedirectStandardOutput = true;
            psInfo.RedirectStandardError = true;

            // Process p = Process.Start(psInfo);
            process = new System.Diagnostics.Process();
            process.StartInfo = psInfo;
            process.EnableRaisingEvents = true;

            process.OutputDataReceived += OupputDataReceivedEventHandler;
            process.ErrorDataReceived += ErrorDataReceivedEventHandler;
            process.Exited += new EventHandler(ExitEventHandler);

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
    }
}
