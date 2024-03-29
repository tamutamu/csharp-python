﻿using System;
using System.Diagnostics;
using System.IO;
using System.Management;
using System.Text;

namespace frontend.util
{
    public class ProcessUtil
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

        private static void KillProcessAndChildren(int pid)
        {
            // Cannot close 'system idle process'.
            if (pid == 0)
            {
                return;
            }
            ManagementObjectSearcher searcher = new ManagementObjectSearcher
                    ("Select * From Win32_Process Where ParentProcessID=" + pid);
            ManagementObjectCollection moc = searcher.Get();
            foreach (ManagementObject mo in moc)
            {
                KillProcessAndChildren(Convert.ToInt32(mo["ProcessID"]));
            }
            try
            {
                Process proc = Process.GetProcessById(pid);
                proc.Kill();
            }
            catch (ArgumentException)
            {
                // Process already exited.
            }
        }

        public ProcessUtil()
        {
        }
        public int Exit()
        {
#if DEBUG
            this.process.CloseMainWindow();
            KillProcessAndChildren(this.process.Id);
            this.process.CancelErrorRead();
            this.process.CancelOutputRead();
#else
            KillProcessAndChildren(this.process.Id);
            this.process.CancelErrorRead();
            this.process.CancelOutputRead();
#endif
            this.process.Kill();
            this.process.WaitForExit();
            this.ExitCode = process.ExitCode;
            return this.ExitCode;
        }

        public void Execute(bool daemon = false)
        {
            process = new Process();

            ProcessStartInfo psInfo = new ProcessStartInfo();
            psInfo.FileName = this.FileName;
            psInfo.WorkingDirectory = this.WorkingDirectory;
            psInfo.Arguments = this.Arguments;
            //psInfo.RedirectStandardInput = true;

#if DEBUG
            psInfo.CreateNoWindow = false;
            psInfo.RedirectStandardOutput = false;
            psInfo.RedirectStandardError = false;
#else 
            psInfo.CreateNoWindow = true;
            psInfo.RedirectStandardOutput = true;
            psInfo.RedirectStandardError = true;

            process.OutputDataReceived += OupputDataReceivedEventHandler;
            process.ErrorDataReceived += ErrorDataReceivedEventHandler;
#endif
            psInfo.UseShellExecute = false;

            // Process p = Process.Start(psInfo);
            process.StartInfo = psInfo;
            process.EnableRaisingEvents = true;

            process.Exited += new EventHandler(ExitEventHandler);

            // プロセスの実行
            process.Start();

            // 標準入力への書き込み
            //using (StreamWriter sw = p.StandardInput)
            //{
            //    sw.Write(InputString);
            //}

            //非同期で出力とエラーの読み取りを開始
#if DEBUG
#else
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
#endif

            if (daemon)
            {
                // 終わるまでまつ
                process.WaitForExit();
                this.ExitCode = process.ExitCode;
                this.StandardOutput = standardOutputStringBuilder.ToString();
            }
        }

        public void SendInputToProcess(ConsoleKey key)
        {
            // 標準入力への書き込み
            using (StreamWriter sw = process.StandardInput)
            {
                sw.Write(key);
            }
        }
    }
}
