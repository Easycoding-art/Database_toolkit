namespace Database_toolkit;
using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;
using System.IO;
using System.Runtime.InteropServices;
using System.Diagnostics;

public partial class Form1 : Form
{
    public Form1()
    {
        Settings_create();
        InitializeComponent();
    }
    string db_name = "Postgres";
    string db_password = "1234";
    Form settings;
    Button settings_close;
    TextBox name_value;
    TextBox password_value;
    private void play_Click(object sender,EventArgs e) {
        Process p = new Process();
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.Arguments = "Schemas\\config\\main.py";
        // Перехватываем вывод
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.CreateNoWindow = true;
        // Запускаемое приложение
        p.StartInfo.FileName = "python";
        //p.StartInfo.FileName = "example.exe";

        // Передаем необходимые аргументы
        // p.Arguments = "example.txt";
        p.Start();
        // Результат работы консольного приложения
        p.StandardInput.WriteLine(db_name);
        p.StandardInput.WriteLine(db_password);
        p.StandardInput.WriteLine("config");
        // Дождаться завершения запущенного приложения
        p.WaitForExit();
    }
    private void query_Click(object sender,EventArgs e) {
        Process p = new Process();
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.Arguments = "query.py";
        // Перехватываем вывод
        p.StartInfo.RedirectStandardOutput = false;
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.CreateNoWindow = false;
        // Запускаемое приложение
        p.StartInfo.FileName = "python";
        //p.StartInfo.FileName = "example.exe";

        // Передаем необходимые аргументы
        // p.Arguments = "example.txt";
        p.Start();
        // Результат работы консольного приложения
        p.StandardInput.WriteLine(db_name);
        p.StandardInput.WriteLine(db_password);
        p.StandardInput.WriteLine(code.Text);
        // Дождаться завершения запущенного приложения
        p.WaitForExit();
    }
    private void Settings_create() {
        settings=new Form();
        settings.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
        settings.ClientSize = new System.Drawing.Size(400, 200);
        settings.Text = "Доступ к БД";
        settings.BackColor = System.Drawing.Color.DarkGoldenrod;
        settings.MaximumSize = new System.Drawing.Size(400, 250);
        settings.MinimumSize = new System.Drawing.Size(400, 250);
        settings.MaximizeBox = false;
        settings.Show();

        settings_close = new Button();
        settings_close.Text = "Continue";
        settings_close.Location = new Point(150, 140);
        settings_close.Size = new Size(80,56);
        settings_close.BackColor = Color.BurlyWood;
        settings.Controls.Add(settings_close);

        name_value = new TextBox();
        name_value.Location = new Point(35, 10);
        name_value.Size = new Size(85,90);
        name_value.Text = db_name;
        name_value.BackColor = Color.OrangeRed;
        name_value.ForeColor = Color.OliveDrab;
        settings.Controls.Add(name_value);

        password_value = new TextBox();
        password_value.Text = db_password;
        password_value.Enabled = false;
        password_value.Location = new Point(35, 35);
        password_value.Size = new Size(85,90);
        password_value.BackColor = Color.GreenYellow;
        settings.Controls.Add(password_value);

        settings_close.Click += new EventHandler(Settings_close);
    }

    private void Settings_close(object sender, System.EventArgs e) {  
        db_name = name_value.Text;
        db_password = password_value.Text;
        project_name_change(db_name);
        settings.Dispose();
}
}
