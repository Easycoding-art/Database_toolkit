namespace Database_toolkit;

partial class Form1
{
    /// <summary>
    ///  Required designer variable.
    /// </summary>
    private System.ComponentModel.IContainer components = null;

    /// <summary>
    ///  Clean up any resources being used.
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
    ///  Required method for Designer support - do not modify
    ///  the contents of this method with the code editor.
    /// </summary>
    Button button_play;
    Button button_query;
    TextBox code;
    void project_name_change(string project_name) {
        this.Text = project_name;
    }
    private void InitializeComponent()
    {
        this.components = new System.ComponentModel.Container();
        this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
        this.ClientSize = new System.Drawing.Size(800, 500);
        this.AutoSize = true;
        project_name_change("Новый проект");
        this.BackColor = System.Drawing.Color.Blue;

        code = new TextBox();
        code.Location = new Point(10, 10);
        code.Size = new Size(690,480);
        code.Text = "";
        code.BackColor = Color.Gray;
        code.Multiline = true;
        code.ForeColor = Color.Black;
        // Добавьте вертикальные полосы прокрутки к элементу управления TextBox.
        code.ScrollBars = ScrollBars.Vertical;
        // Разрешить ввод клавиши TAB в элементе управления TextBox.
        code.AcceptsReturn = true;
        // Разрешить ввод клавиши TAB в элементе управления TextBox.
        code.AcceptsTab = true;
        // Установите значение WordWrap в true, чтобы текст переходил на следующую строку.
        code.WordWrap = true;
        code.Anchor = (AnchorStyles.Right | AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Bottom);
        this.Controls.Add(code);

        button_play = new Button();
        button_play.Location = new Point(710, 180);
        button_play.Text = "FILL";
        button_play.Size = new Size(90,56);
        button_play.BackColor = Color.Teal;
        button_play.Anchor = (AnchorStyles.Right);
        this.Controls.Add(button_play);
        button_play.Click += new EventHandler(play_Click);

        button_query = new Button();
        button_query.Location = new Point(710, 240);
        button_query.Text = "QUERY";
        button_query.Size = new Size(90,56);
        button_query.BackColor = Color.Teal;
        button_query.Anchor = (AnchorStyles.Right);
        this.Controls.Add(button_query);
        button_query.Click += new EventHandler(query_Click);

    }
    #endregion
}
