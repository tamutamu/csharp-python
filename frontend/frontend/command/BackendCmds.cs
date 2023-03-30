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

    public class AmazonLoginCmd : BackendCmd { }

    public class YahooAuctionSellCmd : BackendCmd { }

    public class EventCmd : BackendCmd
    {
        public EventCmd(string processId)
        {
            this.process_id = processId;
        }

        public string process_id { get; }
    }
}
