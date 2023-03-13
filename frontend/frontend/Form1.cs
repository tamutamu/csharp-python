using frontend.backend;
using frontend.command;
using System;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace frontend
{
    public partial class Form1 : Form
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();

        private BackendServer backendServer = null;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //textBox1.AutoSize = false;
            //textBox1.Size = new System.Drawing.Size(251, 28);
        }

        async private void button1_Click(object sender, EventArgs e)
        {
            var ret = await RequestBackend(textBox1.Text);
            MessageBox.Show(ret);
        }

        private async Task<string> RequestBackend(string data)
        {
            return await Task.Run(() =>
            {
                backendServer = new BackendServer();

                this.Invoke((Action)(() =>
                {
                    btnExit.Enabled = false;
                }));

                backendServer.Start();

                var StartCommand = new Start(textBox1.Text);
                var ret = backendServer.Request(StartCommand);

                this.Invoke((Action)(() =>
                {
                    btnExit.Enabled = true;
                }));

                return ret;
            });
        }

        /// ApplicationExitイベントハンドラ
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Application_ApplicationExit(object sender, EventArgs e)
        {
            //if (accessor != null)
            //{
            //    accessor.Dispose();
            //}

            Application.ApplicationExit -= new EventHandler(Application_ApplicationExit);
        }

        private void contextMenuStrip1_Opening(object sender, System.ComponentModel.CancelEventArgs e)
        {

        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            backendServer?.Stop();
        }
    }
}
