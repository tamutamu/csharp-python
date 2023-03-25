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
            this.yahooUserName = yahooUserName;
            this.yahooUserPass = yahooUserPass;
        }

        public string yahooUserName { get; }
        public string yahooUserPass { get; }
    }

    public class PreLoginEndCmd : BackendCmd { }
}
