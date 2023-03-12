namespace frontend.command
{
    public interface IBackendCmd
    {
        string command { get; }
    }

    abstract public class BackendCmd : IBackendCmd
    {
        public virtual string command { get; }
    }

    public class Exit : BackendCmd
    {
        public override string command { get; } = "EXIT";

    }
}
