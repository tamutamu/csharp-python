using frontend.command;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;
using static frontend.FrontendServer;

namespace frontend
{
    public partial class PreLoginForm : Form
    {
        private MainForm mainForm;

        public PreLoginForm()
        {
            InitializeComponent();
            this.StartPosition = FormStartPosition.CenterParent;
        }

        private void PreLoginForm_Load(object sender, EventArgs e)
        {
            this.mainForm = ((MainForm)this.Owner);
        }

        private Callback CreateCallback()
        {
            return (Dictionary<string, string> r) =>
            {
                this.Invoke(new Action(async () =>
                {
                    await Task.Factory.StartNew(() =>
                    {
                        MessageBox.Show("ログインできました？");
                        this.mainForm.backendServer.Request(new EventCmd(r["process_id"]));
                    }
                    );
                }));
            };
        }

        private void btnStart_Click(object sender, System.EventArgs e)
        {
            this.mainForm.frontendServer.callback += CreateCallback();
            var ret = this.mainForm.backendServer.Request(new AmazonLoginCmd());
        }

        private void btnExit_Click(object sender, System.EventArgs e)
        {
            this.Close();
        }
    }
}
