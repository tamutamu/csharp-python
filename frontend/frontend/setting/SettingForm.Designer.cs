namespace frontend
{
    partial class SettingForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.txtSettingsFilePath = new System.Windows.Forms.TextBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.btnSelectSettingsFile = new System.Windows.Forms.Button();
            this.btnOk = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // txtSettingsFilePath
            // 
            this.txtSettingsFilePath.Location = new System.Drawing.Point(31, 56);
            this.txtSettingsFilePath.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.txtSettingsFilePath.Name = "txtSettingsFilePath";
            this.txtSettingsFilePath.Size = new System.Drawing.Size(656, 28);
            this.txtSettingsFilePath.TabIndex = 0;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.btnSelectSettingsFile);
            this.groupBox1.Controls.Add(this.txtSettingsFilePath);
            this.groupBox1.Location = new System.Drawing.Point(28, 40);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.groupBox1.Size = new System.Drawing.Size(783, 136);
            this.groupBox1.TabIndex = 1;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "設定ファイルの選択";
            // 
            // btnSelectSettingsFile
            // 
            this.btnSelectSettingsFile.Image = global::frontend.Properties.Resources._62917openfilefolder_109270;
            this.btnSelectSettingsFile.Location = new System.Drawing.Point(712, 56);
            this.btnSelectSettingsFile.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.btnSelectSettingsFile.Name = "btnSelectSettingsFile";
            this.btnSelectSettingsFile.Size = new System.Drawing.Size(44, 35);
            this.btnSelectSettingsFile.TabIndex = 1;
            this.btnSelectSettingsFile.UseVisualStyleBackColor = true;
            this.btnSelectSettingsFile.Click += new System.EventHandler(this.btnSelectSettingsFile_Click);
            // 
            // btnOk
            // 
            this.btnOk.Location = new System.Drawing.Point(547, 246);
            this.btnOk.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(122, 44);
            this.btnOk.TabIndex = 2;
            this.btnOk.Text = "OK";
            this.btnOk.UseVisualStyleBackColor = true;
            this.btnOk.Click += new System.EventHandler(this.btnOk_Click);
            // 
            // btnCancel
            // 
            this.btnCancel.Location = new System.Drawing.Point(689, 246);
            this.btnCancel.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(122, 44);
            this.btnCancel.TabIndex = 2;
            this.btnCancel.Text = "キャンセル";
            this.btnCancel.UseVisualStyleBackColor = true;
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
            // 
            // SettingForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(11F, 21F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(838, 328);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.groupBox1);
            this.Margin = new System.Windows.Forms.Padding(3, 4, 3, 4);
            this.Name = "SettingForm";
            this.Text = "設定ファイル";
            this.Load += new System.EventHandler(this.SettingForm_Load);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TextBox txtSettingsFilePath;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button btnSelectSettingsFile;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.Button btnCancel;
    }
}