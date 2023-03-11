using frontend.util;

namespace frontend.backend
{
    internal class BackendServer
    {
        public int Port { get; private set; }
        public int ExitCode { get; set; }

        public BackendServer()
        {
        }

        public void Start()
        {
            var processUtil = new ProcessUtil();
            processUtil.FileName = "python";

            this.Port = NetworkUtil.GetFreePort();
            processUtil.Arguments = $"server.py {this.Port}";
            processUtil.WorkingDirectory = @"../../../../backend/";

            processUtil.Execute();
        }

        public string Request(string data)
        {
            var ret = SocketClientcs.Request(data, this.Port);
            return ret;
        }
    }
}
