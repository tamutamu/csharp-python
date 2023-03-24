namespace frontend.command
{
    public interface IBackendCmd
    {
        string _CommandName { get; }
    }

    abstract public class BackendCmd : IBackendCmd
    {
        public virtual string _CommandName { get { return this.GetType().Name; } }
    }

    public class StartCmd : BackendCmd
    {
        public StartCmd(string Text)
        {
            this.Text = Text;
        }

        public string Text { get; }
    }

    public class ExitCmd : BackendCmd
    {
    }

    public class PreLoginCmd : BackendCmd
    {
        public PreLoginCmd(string yahooUserName, string yahooUserPass, string keepaUserName, string keepaUserPass)
        {
            this.yahooUserName = yahooUserName;
            this.yahooUserPass = yahooUserPass;
            this.keepaUserName = keepaUserName;
            this.keepaUserPass = keepaUserPass;
        }

        public string yahooUserName { get; }
        public string yahooUserPass { get; }
        public string keepaUserName { get; }
        public string keepaUserPass { get; }
    }
}
