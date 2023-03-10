using System;
using System.IO;
using System.IO.MemoryMappedFiles;
using System.Text;
using System.Windows.Forms;

namespace frontend
{

    public partial class Form1 : Form
    {
        //const string MMAP_NAME = "MAP_TEST";
        //MemoryMappedViewAccessor accessor;

        public Form1()
        {
            InitializeComponent();

            //MemoryMappedFile share_mem = MemoryMappedFile.CreateFromFile(@"./_memory.dat", FileMode.Open, MMAP_NAME);
            //accessor = share_mem.CreateViewAccessor();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            textBox1.AutoSize = false;
            textBox1.Size = new System.Drawing.Size(200, 34);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Write data to shared memory
            //string str = "ああHelloworld3049999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999ppppppppppppppppppppppppppppppppppppppppppppp@";
            //Encoding utf8 = Encoding.GetEncoding("UTF-8");
            //byte[] data = utf8.GetBytes(str);
            //Console.WriteLine(data.Length);
            //accessor.WriteArray(0, data, 0, data.Length);

            var python = new PythonExecutor();
            python.FileName = "python";
            //python.Arguments = "server.py";
            python.WorkingDirectory = @"C:\Users\tamu0\R\WORK\csharp-python\backend";
            python.Execute();
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
    }
}
