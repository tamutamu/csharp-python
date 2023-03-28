using frontend.command;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;

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

        private void Callback(Dictionary<string, string> r)
        {
            if (r["status"] == Const.Status.WAITING)
            {
                this.Invoke(new Action(async () =>
                {
                    await Task.Factory.StartNew(() =>
                    {
                        MessageBox.Show("ログインできました？");
                        this.mainForm.backendServer.Request(new EventCmd(r["process_id"]), Callback);
                    }
                    );
                }));
            }
            else if (r["status"] == Const.Status.EXIT && r["result"] == Const.Result.SUCCESS)
            {
                MessageBox.Show("完了しました");
            }
            else if (r["status"] == Const.Status.EXIT && r["result"] == Const.Result.FAILED)
            {
                MessageBox.Show("処理が失敗しました");
            }
        }

        private void btnStart_Click(object sender, System.EventArgs e)
        {
            var ret = this.mainForm.backendServer.Request(new AmazonLoginCmd(), Callback);
        }

        private void btnExit_Click(object sender, System.EventArgs e)
        {
            this.Close();
        }

        private void PreLoginForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            this.mainForm.backendServer.RemoveFrontendServerCallback();
        }

        //private Callback CreateCallback()
        //{
        //    return (Dictionary<string, string> r) =>
        //    {
        //        this.Invoke(new Action(async () =>
        //        {
        //            await Task.Factory.StartNew(() =>
        //            {
        //                MessageBox.Show("ログインできました？");
        //                this.mainForm.backendServer.Request(new EventCmd(r["process_id"]));
        //            }
        //            );
        //        }));
        //    };
        //}

    }
}
