using frontend.backend;
using frontend.command;
using frontend.model;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace frontend
{
    public partial class MainForm : Form
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();

        private BackendServer backendServer = null;

        private List<StockPrice> _stockPriceList = new List<StockPrice>();

        public MainForm()
        {
            InitializeComponent();

            //ApplicationExitイベントハンドラを追加
            Application.ApplicationExit += new EventHandler(Application_ApplicationExit);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //textBox1.AutoSize = false;
            //textBox1.Size = new System.Drawing.Size(251, 28);

            // Python側バックエンドサーバ起動
            backendServer = new BackendServer();
            backendServer.OupputDataReceivedEventHandler = BackendServerOutputDataReceived;
            backendServer.ErrorDataReceivedEventHandler = BackendServerErrorDataReceived;
            backendServer.ExitEventHandler = BackendServerExited;
            backendServer.Start();

            // C#側サーバ起動
            Task.Run(() =>
            {
                SocketServer.Start(port: 9999);
            });


            var sp = new StockPrice() { Code = "11", Open = 100, Enable = true };
            _stockPriceList.Add(sp);

            dgvStockPrice.AutoGenerateColumns = false;
            dgvStockPrice.DataSource = _stockPriceList;


            var textColumn = new DataGridViewTextBoxColumn();
            textColumn.DataPropertyName = "Code";
            textColumn.Name = "Code";
            textColumn.HeaderText = "コード";
            dgvStockPrice.Columns.Add(textColumn);

            textColumn = new DataGridViewTextBoxColumn();
            textColumn.DataPropertyName = "Open";
            textColumn.Name = "Open";
            textColumn.HeaderText = "始値";
            dgvStockPrice.Columns.Add(textColumn);

            var checkBoxColumn = new DataGridViewCheckBoxColumn();
            checkBoxColumn.DataPropertyName = "Enable";
            checkBoxColumn.Name = "Enable";
            checkBoxColumn.HeaderText = "有効";
            dgvStockPrice.Columns.Add(checkBoxColumn);

        }

        async private void button1_Click(object sender, EventArgs e)
        {
            var ret = await RequestBackend(textBox1.Text);
        }

        private async Task<string> RequestBackend(string data)
        {
            return await Task.Run(() =>
            {
                this.Invoke((Action)(() =>
                {
                    btnExit.Enabled = false;
                }));


                var StartCommand = new Start(textBox1.Text);
                var ret = backendServer.Request(StartCommand);

                this.Invoke((Action)(() =>
                {
                    btnExit.Enabled = true;
                }));

                return ret;
            });
        }

        void BackendServerOutputDataReceived(object sender,
            System.Diagnostics.DataReceivedEventArgs e)
        {
            if (e != null && e.Data != null && e.Data.Length > 0)
            {
                this.Invoke((Action)(() =>
                {
                    rtbMessage.AppendText(e.Data + "\n");
                }));
            }
        }

        void BackendServerErrorDataReceived(object sender,
            System.Diagnostics.DataReceivedEventArgs e)
        {
            if (e != null && e.Data != null && e.Data.Length > 0)
            {
                this.Invoke((Action)(() =>
                {
                    rtbMessage.AppendText(e.Data + "\n");
                }));
            }
        }

        private void BackendServerExited(object sender, EventArgs e)
        {
            Console.WriteLine("BackendServer ended...");
        }

        private void Application_ApplicationExit(object sender, EventArgs e)
        {
            backendServer?.Stop();
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
