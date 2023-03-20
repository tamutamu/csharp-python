using frontend.command;
using frontend.util;
using System;
using System.Diagnostics;

namespace frontend.backend
{
    internal class BackendServer
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();

        public ProcessUtil processUtil;
        public DataReceivedEventHandler OupputDataReceivedEventHandler { get; set; }
        public DataReceivedEventHandler ErrorDataReceivedEventHandler { get; set; }
        public EventHandler ExitEventHandler { get; set; }
        public int Port { get; private set; }
        public int ExitCode { get; set; }

        public BackendServer()
        {
        }

        public void Start()
        {
            processUtil = new ProcessUtil();
            processUtil.OupputDataReceivedEventHandler = OupputDataReceivedEventHandler;
            processUtil.ErrorDataReceivedEventHandler = ErrorDataReceivedEventHandler;
            processUtil.ExitEventHandler = ExitEventHandler;

            this.Port = NetworkUtil.GetFreePort();
            LOGGER.Info($"Port = {Port}");

#if DEBUG
            string variable = System.Environment.GetEnvironmentVariable("Path", System.EnvironmentVariableTarget.Process);
            processUtil.FileName = "poetry";
            processUtil.Arguments = $@"run python src\main.py {this.Port}";
            processUtil.WorkingDirectory = @"../../../../backend/";
#else 
            processUtil.FileName = "server.exe";
            processUtil.Arguments = $"{this.Port}";
            processUtil.WorkingDirectory = @"../../../../backend/bin/";
#endif

            processUtil.Execute();
        }

        public int Stop()
        {
            try
            {
                return processUtil.Exit();
            }
            catch (Exception e)
            {
                LOGGER.Debug("process has been deleted.");
            }

            return 1;
        }

        public string Request(IBackendCmd cmd)
        {
            var body = JsonUtil.ToJson(cmd);
            var ret = SocketClient.Request(body, this.Port);
            return ret;
        }
    }
}
