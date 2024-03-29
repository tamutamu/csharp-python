﻿using frontend.db;
using frontend.model;
using System;
using System.Windows.Forms;

namespace frontend
{
    public partial class SettingForm : Form
    {
        public SettingForm()
        {
            InitializeComponent();
            this.StartPosition = FormStartPosition.CenterParent;
        }

        private void btnSelectSettingsFile_Click(object sender, System.EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.InitialDirectory = Environment.CurrentDirectory;
            ofd.Title = "使用する設定.xlsxを選択してください";
            ofd.Filter = "Excelファイル(*.xls;*.xlsx)|*.xls;*.xlsx";
            ofd.RestoreDirectory = true;

            if (ofd.ShowDialog() == DialogResult.OK)
            {
                Console.WriteLine(ofd.FileName);
                txtSettingsFilePath.Text = ofd.FileName;
            }
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            var dbm = new DBManager();
            var setting = new SystemSetting() { Name = "SETTING_FILE_PATH", Value = txtSettingsFilePath.Text };
            dbm.Mutate(setting.GetMutate());

            this.Close();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void SettingForm_Load(object sender, EventArgs e)
        {
            var dbm = new DBManager();
            var setting = dbm.Query(SystemSetting.GetQuery("SETTING_FILE_PATH"));
            txtSettingsFilePath.Text = setting.Value;
        }
    }
}
