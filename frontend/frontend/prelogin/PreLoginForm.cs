using frontend.command;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace frontend
{
    public partial class PreLoginForm : Form
    {
        public PreLoginForm()
        {
            InitializeComponent();
            this.StartPosition = FormStartPosition.CenterParent;
        }

        async private void btnStart_Click(object sender, System.EventArgs e)
        {
            var ret = ((MainForm)this.Owner).backendServer.Request(new AmazonLoginCmd("x10atamutamu@gmail.com", "tamuranaoki1981"));

            await Task.Factory.StartNew(() =>
            {
                MessageBox.Show("ログインできました？");
                ((MainForm)this.Owner).backendServer.Request(new EventCmd(ret["process_id"]));
            }
            );
        }

        private void btnExit_Click(object sender, System.EventArgs e)
        {

        }
    }
}
