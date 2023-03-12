using frontend.util;

namespace frontend.backend
{
    internal class BackendServer
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();

        public ProcessUtil processUtil;
        public int Port { get; private set; }
        public int ExitCode { get; set; }

        public BackendServer()
        {
        }

        public void Start()
        {
            processUtil = new ProcessUtil();
            this.Port = NetworkUtil.GetFreePort();
            LOGGER.Info($"Port = {Port}");

#if DEBUG
            processUtil.FileName = "python";
            processUtil.Arguments = $"server.py {this.Port}";
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
            return processUtil.Exit();
        }

        public string Request(string data)
        {
            var ret = SocketClientcs.Request(data, this.Port);
            return ret;
        }
    }
}
