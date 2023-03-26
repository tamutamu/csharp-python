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

    public class ExitCmd : BackendCmd { }

    public class GetStockPriceCmd : BackendCmd { }

    public class PreLoginCmd : BackendCmd
    {
        public PreLoginCmd(string yahooUserName, string yahooUserPass)
        {
            this.yahoo_user_name = yahooUserName;
            this.yahoo_user_pass = yahooUserPass;
        }

        public string yahoo_user_name { get; }
        public string yahoo_user_pass { get; }
    }

    public class EventCmd : BackendCmd
    {
        public EventCmd(string processId)
        {
            this.process_id = processId;
        }

        public string process_id { get; }
    }
}
