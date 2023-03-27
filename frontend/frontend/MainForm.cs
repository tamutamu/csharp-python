﻿using frontend.backend;
using frontend.command;
using frontend.db;
using frontend.model;
using frontend.util;
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
        private int FrontendServerPort = 0;

        private BindingList<StockPrice> _stockPriceList = new BindingList<StockPrice>();
        private BindingSource source = new BindingSource();

        public MainForm()
        {
            InitializeComponent();
            Application.ApplicationExit += new EventHandler(Application_ApplicationExit);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // C#側サーバ起動
            FrontendServerPort = NetworkUtil.GetFreePort();
            Task.Run(() =>
            {
                FrontendServer.Start(port: FrontendServerPort, this);
            });

            // Python側バックエンドサーバ起動
            backendServer = new BackendServer();
            backendServer.OupputDataReceivedEventHandler = BackendServerOutputDataReceived;
            backendServer.ErrorDataReceivedEventHandler = BackendServerErrorDataReceived;
            backendServer.ExitEventHandler = BackendServerExited;
            backendServer.FrontendServerPort = FrontendServerPort;
            backendServer.Start();

            // DataGridView初期化
            SetupDataGridView();
        }

        private void SetupDataGridView()
        {
            //this.source.DataSource = _stockPriceList;

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

                var ret = backendServer.Request(cmd);

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

        async private void btnPreLogin_Click(object sender, EventArgs e)
        {
            RefreshData();
            //var ret = await RequestBackend(new AmazonLoginCmd("x10atamutamu@gmail.com", "tamuranaoki1981"));

            //await Task.Factory.StartNew(() =>
            //{
            //    MessageBox.Show("ログインできました？");
            //    backendServer.Request(new EventCmd(ret["process_id"]));
            //}
            //);
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
    }
}
