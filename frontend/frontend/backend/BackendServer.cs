using frontend.command;
using frontend.util;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text.Json;
using System.Threading.Tasks;
using static frontend.FrontendServer;

namespace frontend.backend
{
    public class BackendServer
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();
        public ProcessUtil processUtil;
        public DataReceivedEventHandler OupputDataReceivedEventHandler { get; set; }
        public DataReceivedEventHandler ErrorDataReceivedEventHandler { get; set; }
        public EventHandler ExitEventHandler { get; set; }
        public int Port { get; private set; }
        public int ExitCode { get; set; }
        public FrontendServer frontendServer;

        public void Start()
        {
            // C#フロントエンド側サーバ起動
            var frontendServerPort = NetworkUtil.GetFreePort();
            Task.Run(() =>
            {
                this.frontendServer = FrontendServer.Get(port: frontendServerPort);
            });

            processUtil = new ProcessUtil();
            processUtil.OupputDataReceivedEventHandler = OupputDataReceivedEventHandler;
            processUtil.ErrorDataReceivedEventHandler = ErrorDataReceivedEventHandler;
            processUtil.ExitEventHandler = ExitEventHandler;

            this.Port = NetworkUtil.GetFreePort();
            LOGGER.Info($"Port = {Port}");
#if DEBUG
            string variable = System.Environment.GetEnvironmentVariable("Path", System.EnvironmentVariableTarget.Process);
            processUtil.FileName = "poetry";
            processUtil.Arguments = $@"run python src\main.py {this.Port} {frontendServerPort}";
            processUtil.WorkingDirectory = System.IO.Path.GetFullPath(@"../../../../backend");
#else 
            string variable = System.Environment.GetEnvironmentVariable("Path", System.EnvironmentVariableTarget.Process);
            processUtil.FileName = "poetry";
            processUtil.Arguments = $@"run python src\main.py {this.Port} {this.FrontendServerPort}";
            processUtil.WorkingDirectory = System.IO.Path.GetFullPath(@"../../../../backend");
#endif
            processUtil.Execute();
        }

        public void PressEnter()
        {
            processUtil.SendInputToProcess(ConsoleKey.Enter);
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
                LOGGER.Debug(e);
            }
            return 1;
        }

        public Dictionary<string, string> Request(IBackendCmd cmd, Callback callback)
        {
            this.frontendServer.callback += callback;
            var body = JsonUtil.ToJson(cmd);
            var ret = SocketClient.Request(body, this.Port);
            var json = JsonSerializer.Deserialize<Dictionary<string, string>>(ret);
            return json;
        }
    }
}
