namespace frontend.command
{
    public interface IBackendCmd
    {
        string _CommandName { get; }
    }

    abstract public class BackendCmd : IBackendCmd
    {
        public virtual string _CommandName { get; }
    }

    public class Start : BackendCmd
    {
        public Start(string Text)
        {
            this.Text = Text;
        }

        public override string _CommandName { get; } = "START";
        public string Text { get; }
    }

    public class Exit : BackendCmd
    {
        public override string _CommandName { get; } = "EXIT";
    }
}
