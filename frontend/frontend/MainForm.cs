using frontend.backend;
using frontend.command;
using frontend.db;
using frontend.help;
using frontend.model;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace frontend
{
    public partial class MainForm : Form
    {
        static NLog.Logger LOGGER = NLog.LogManager.GetCurrentClassLogger();
        public BackendServer backendServer = null;
        public int frontendServerPort = 0;

        private BindingList<StockPrice> _stockPriceList = new BindingList<StockPrice>();

        public MainForm()
        {
            InitializeComponent();
            Application.ApplicationExit += new EventHandler(Application_ApplicationExit);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Python側バックエンドサーバ起動
            backendServer = new BackendServer();
            backendServer.OupputDataReceivedEventHandler = BackendServerOutputDataReceived;
            backendServer.ErrorDataReceivedEventHandler = BackendServerErrorDataReceived;
            backendServer.ExitEventHandler = BackendServerExited;
            backendServer.Start();

            // DataGridView初期化
            SetupDataGridView();
        }

        private void SetupDataGridView()
        {
            dgvStockPrice.AutoGenerateColumns = false;
            dgvStockPrice.RowHeadersVisible = false;
            dgvStockPrice.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvStockPrice.DataSource = _stockPriceList;

            Action<string, string, string> genColumn = (dpName, name, headerText) =>
            {
                var textColumn = new DataGridViewTextBoxColumn();
                textColumn.DataPropertyName = dpName;
                textColumn.Name = name;
                textColumn.HeaderText = headerText;
                dgvStockPrice.Columns.Add(textColumn);
            };

            genColumn("Code", "Code", "コード");
            genColumn("Open", "Open", "始値");
            genColumn("Enable", "Enable", "有効");
        }

        public void RefreshData()
        {
            var dbm = new DBManager();
            var dataList = dbm.QueryList(BackendResult.createEntity);

            _stockPriceList.Clear();

            var _list = dataList.Select(d =>
            {
                var result = d.Result;
                var sp = JsonSerializer.Deserialize<StockPrice>(result);
                return new StockPrice() { Open = sp.Open, Enable = sp.Enable };
            });

            foreach (var sp in _list)
            {
                _stockPriceList.Add(sp);
            }
        }

        async private void button1_Click(object sender, EventArgs e)
        {
            var startCommand = new StartCmd(textBox1.Text);
            var ret = await RequestBackend(startCommand);
        }

        private async Task<Dictionary<string, string>> RequestBackend(BackendCmd cmd)
        {
            return await Task.Run(() =>
            {
                this.Invoke((Action)(() =>
                {
                    btnExit.Enabled = false;
                }));

                var ret = backendServer.Request(cmd, null);

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
                    rtbMessage.AppendText("[ERROR] " + e.Data + "\n");
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

        private void contextMenuStrip1_Opening(object sender, System.ComponentModel.CancelEventArgs e) { }

        private void btnExit_Click(object sender, EventArgs e)
        {
            backendServer?.Stop();
        }

        private void btnPreLogin_Click(object sender, EventArgs e)
        {
            //RefreshData();
            var ret = this.backendServer.Request(new YahooAuctionSellCmd(), Callback);
        }

        private void Callback(Dictionary<string, string> r)
        {
            if (r["status"] == Const.Status.EXIT && r["result"] == Const.Result.SUCCESS)
            {
                MessageBox.Show("完了しました");
            }
            else if (r["status"] == Const.Status.EXIT && r["result"] == Const.Result.FAILED)
            {
                MessageBox.Show("処理が失敗しました: " + r["detail"]);
            }
        }

        private void SettingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var f = new SettingForm();
            f.ShowDialog(this);
        }

        private void ExitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void PreLoginToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var f = new PreLoginForm();
            f.ShowDialog(this);
        }

        private void VersionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var f = new VersionInfo();
            f.ShowDialog(this);
        }
    }
}
