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

            // DBから設定ファイルのパスをロードする
        }

        private void btnSelectSettingsFile_Click(object sender, System.EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
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
            // DBに保存、親に設定した値を返す??
            this.Close();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
