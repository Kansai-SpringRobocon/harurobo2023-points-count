import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk
from PIL import ImageTk
import json
import datetime
from enum import Enum


class Application(tk.Frame):
    class time_mode(Enum):
        NONE = 0
        setting1 = 1
        setting2 = 2
        display_time = 3
        sales_time = 4

    class timer_mode(Enum):
        stop = 0
        run = 1
        pause = 2
        count_down_to_run = 3
        count_down = 4

    red_points = 0
    blue_points = 0

    red_toy_counters = 0
    blue_toy_counters = 0

    class state():
        red_toy_acquisition = False
        blue_toy_acquisition = False

    state_time_mode = time_mode.NONE
    state_timer_mode = timer_mode.stop

    btn_exist = False

    red_team_name = "チーム名を\n選択してください"
    blue_team_name = "チーム名を\n選択してください"

    team_list = {}
    with open("team.json", mode="r", encoding="utf-8") as team_list_file:
        team_list = json.load(team_list_file)

    position_state_red = {}
    position_state_blue = {}
    with open("area_state.json", mode="r", encoding="utf-8") as area_state:
        position_state_red = json.load(area_state)
    with open("area_state.json", mode="r", encoding="utf-8") as area_state:
        position_state_blue = json.load(area_state)

    def __init__(self):
        self.master = tk.Tk()

        self.master.title("春ロボコン2023 得点計算ツール")       # ウィンドウタイトル
        self.master.geometry("1792x1008")     # ウィンドウサイズ(幅x高さ)
        # self.master.attributes('-fullscreen', True)
        self.master.iconbitmap(default='harurobo.ico')

        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        # Canvasを配置
        self.canvas.pack(expand=True, fill=tk.BOTH)

        app_name_label = tk.Label(self.master, text="春ロボコン2023\n得点計算ツール",
                                  fg="#000000", font=("HGPゴシックE", 18, "bold"), anchor=tk.CENTER)
        app_name_label.place(x=80, y=20)

        # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        self.photo_image = ImageTk.PhotoImage(file="field.png")
        self.kansai_harurobo_logo = ImageTk.PhotoImage(
            file="kansai-harurobo.png")

        # キャンバスのサイズを取得
        self.master.update()  # Canvasのサイズを取得するため更新しておく
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.field_center_shift = 150  # フィールド画像中心位置をずらす

        points_width = self.canvas_width/4
        points_height = self.canvas_height/6
        self.canvas.create_rectangle(
            points_width+self.field_center_shift, 0, self.canvas_width/2+self.field_center_shift, points_height, fill='red')
        self.canvas.create_rectangle(
            self.canvas_width/2+self.field_center_shift, 0, self.canvas_width/2+points_width+self.field_center_shift, points_height, fill='blue')
        self.canvas.create_rectangle(
            points_width+self.field_center_shift, points_height+1, self.canvas_width/2+points_width+self.field_center_shift, self.canvas_height, fill='#888786')

        # 画像の描画
        self.canvas.create_image(
            # 画像表示位置(Canvasの中心)
            self.canvas_width / 2+self.field_center_shift,
            self.canvas_height * 0.58,
            image=self.photo_image,  # 表示画像データ
        )

        self.canvas.create_image(
            40,       # 画像表示位置
            55,
            image=self.kansai_harurobo_logo,  # 表示画像データ
            anchor=tk.CENTER
        )

        self.log = tk.Text(self.master, state='disabled', borderwidth=5,
                           width=70, height=50, wrap=tk.CHAR, font=("HGPゴシックE", 11))
        ys = ttk.Scrollbar(self.master, orient='vertical',
                           command=self.log.yview)
        self.log['yscrollcommand'] = ys.set
        self.log.insert('end', "Lorem ipsum...\n...\n...")
        self.log.place(x=18, y=200)

        self.red_points_text = tk.StringVar()
        self.red_points_text.set(str(self.red_points))

        self.blue_points_text = tk.StringVar()
        self.blue_points_text.set(str(self.blue_points))

        red_points_label = tk.Label(self.master, textvariable=self.red_points_text,
                                    fg="#FFFFFF", bg="#FF0000", font=("HGPゴシックE", 36, "bold"))
        blue_points_label = tk.Label(self.master, textvariable=self.blue_points_text,
                                     fg="#FFFFFF", bg="#0000FF", font=("HGPゴシックE", 36, "bold"))
        red_points_label.place(x=int(self.canvas_width/2-points_width/2)+self.field_center_shift,
                               y=120, anchor=tk.CENTER)
        blue_points_label.place(x=int(self.canvas_width/2+points_width/2)+self.field_center_shift,
                                y=120, anchor=tk.CENTER)

        self.red_team_text = tk.StringVar()
        self.red_team_text.set(str(self.red_team_name))

        self.blue_team_text = tk.StringVar()
        self.blue_team_text.set(str(self.blue_team_name))
        red_team_name_label = tk.Label(self.master, textvariable=self.red_team_text,
                                       fg="#FFFFFF", bg="#FF0000", font=("HGPゴシックE", 26, "bold"))
        blue_team_name_label = tk.Label(self.master, textvariable=self.blue_team_text,
                                        fg="#FFFFFF", bg="#0000FF", font=("HGPゴシックE", 26, "bold"))
        red_team_name_label.place(x=int(self.canvas_width/2-points_width/2+self.field_center_shift),
                                  y=50, anchor=tk.CENTER)
        blue_team_name_label.place(x=int(self.canvas_width/2+points_width/2+self.field_center_shift),
                                   y=50, anchor=tk.CENTER)

        combobox_font = tk_font.Font(self.master, family="HGPゴシックE",
                                     size=18, weight="bold")
        self.master.option_add("*TCombobox*Listbox.Font", combobox_font)
        red_team_val = tk.StringVar()
        blue_team_val = tk.StringVar()

        red_team_label = tk.Label(self.master, text="赤コート",
                                  fg="#FFFFFF", bg="#FF0000", font=combobox_font)
        blue_team_label = tk.Label(self.master, text="青コート",
                                   fg="#FFFFFF", bg="#0000FF", font=combobox_font)
        self.red_team = tk.ttk.Combobox(
            self.master, textvariable=red_team_val, value=self.team_list["team_name"], font=combobox_font, width=18)
        self.blue_team = tk.ttk.Combobox(
            self.master, textvariable=blue_team_val, value=self.team_list["team_name"], font=combobox_font, width=18)
        self.red_team.bind('<<ComboboxSelected>>',
                           self.update_team_name)
        self.blue_team.bind('<<ComboboxSelected>>',
                            self.update_team_name)

        red_team_label.place(x=15, y=100)
        blue_team_label.place(x=15, y=140)
        self.red_team.place(x=120, y=100)
        self.blue_team.place(x=120, y=140)

        self.timer_state_txt = tk.StringVar()
        self.timer_min_txt = tk.StringVar()
        self.timer_colon_txt = tk.StringVar()
        self.timer_sec_txt = tk.StringVar()
        timer_font = tk_font.Font(self.master, family="HGPゴシックE",
                                  size=42, weight="bold")
        timer_state_font = tk_font.Font(self.master, family="HGPゴシックE",
                                        size=20, weight="bold")
        self.timer_state_label = tk.Label(
            self.master, textvariable=self.timer_state_txt, font=timer_state_font, anchor=tk.CENTER)
        self.timer_min_label = tk.Label(
            self.master, textvariable=self.timer_min_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_colon_label = tk.Label(
            self.master, textvariable=self.timer_colon_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_sec_label = tk.Label(
            self.master, textvariable=self.timer_sec_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_set_state_txt()
        self.timer_set_sec()

        self.def_btns_field_display_time()
        self.setup_timer_btn()
        self.setup_cmd_btn()

        self.master.mainloop()

    def setup_timer_btn(self):
        self.canvas.create_line(1494, 170, 1792, 170, fill="#696969", width=5)
        btn_timer_label_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=24, weight="bold")
        cmd_btn_label = tk.Label(self.master, text='タイマー操作',
                                 font=btn_timer_label_font, anchor=tk.CENTER)
        cmd_btn_label.place(x=1500, y=200)
        btn_timer_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=15, weight="bold")
        self.btn_timer_start = tk.Button(self.master, text='開始', command=self.timer_start,
                                         width=4, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#4169e1", fg="#FFFFFF")
        self.btn_timer_start.place(x=1530, y=260)
        self.btn_timer_pause = tk.Button(self.master, text='一時停止', command=self.timer_pause,
                                         width=8, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#e0e041")
        # btn_timer_pause.place(x=1510, y=260)
        self.btn_timer_reset = tk.Button(self.master, text='リセット', command=self.timer_reset,
                                         width=8, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#e04141", fg="#FFFFFF")
        self.btn_timer_reset.place(x=1650, y=260)

    def timer_start(self):
        self.btn_timer_pause.place(x=1510, y=260)
        self.btn_timer_start.place_forget()
        self.state_timer_mode = self.timer_mode.count_down
        self.timer_sec = 5
        self.timer_set_state_txt()
        self.timer()

    def timer_pause(self):
        self.btn_timer_start.place(x=1530, y=260)
        self.btn_timer_pause.place_forget()
        self.state_timer_mode = self.timer_mode.pause

    def timer_set_state_txt(self):  # BUG:上手く、タイマーのラベルが表示遷移しない
        if self.state_timer_mode == self.timer_mode.count_down:
            self.timer_state_txt.set("Ready?")
        elif self.state_timer_mode == self.timer_mode.count_down_to_run:
            self.timer_state_label.place_forget()
        elif self.state_time_mode == self.time_mode.setting1:
            self.timer_state_txt.set("セッティングタイム1")
        elif self.state_time_mode == self.time_mode.setting2:
            self.timer_state_txt.set("セッティングタイム2")
        elif self.state_time_mode == self.time_mode.display_time:
            self.timer_state_txt.set("陳列タイム")
        elif self.state_time_mode == self.time_mode.sales_time:
            self.timer_state_txt.set("販売タイム")
        else:
            self.timer_state_txt.set("Test")
        self.timer_state_label.place(x=1630, y=10)

    def timer_set_sec(self):
        if self.state_time_mode == (self.time_mode.NONE or self.time_mode.setting1 or self.time_mode.setting2):
            self.timer_sec = 60
        else:
            self.timer_sec = 90
        self.timer_colon_txt.set(":")
        self.timer_min_label.place(x=1565, y=50)
        self.timer_colon_label.place(x=1630, y=48)
        self.timer_sec_label.place(x=1660, y=50)
        self.timer_show()

    def timer_reset(self):
        self.timer_set_sec()
        self.state_timer_mode = self.timer_mode.stop
        self.btn_timer_start.place(x=1530, y=260)
        self.btn_timer_pause.place_forget()

    def timer(self):
        if self.state_timer_mode == self.timer_mode.count_down:  # TODO:カウントダウンモードも実装する
            if self.timer_sec == 0:
                self.timer_sec_label.place_forget()
                self.timer_min_label.place_forget()
                self.timer_colon_txt.set("START!")
                self.timer_colon_label.place(x=1535, y=28)
                self.state_timer_mode = self.timer_mode.count_down_to_run
            else:
                self.timer_show()
                self.timer_sec -= 1
            self.master.after(1000, self.timer)
        elif self.state_timer_mode == self.timer_mode.count_down_to_run:
            self.timer_set_sec()
            self.state_timer_mode = self.timer_mode.run

        if self.state_timer_mode == self.timer_mode.run:
            if self.timer_sec == 0:  # TODO:音を鳴らす機能を実装する
                self.state_timer_mode = self.timer_mode.stop
            if self.state_timer_mode == self.timer_mode.run:
                self.timer_show()
                self.timer_sec -= 1
                self.master.after(1000, self.timer)

    def timer_show(self):
        if self.timer_sec < 60:
            self.timer_sec_txt.set(str(self.timer_sec).zfill(2))
            self.timer_min_txt.set("00")
        else:
            self.timer_min_txt.set(str(int(self.timer_sec/60)).zfill(2))
            self.timer_sec_txt.set(str(self.timer_sec % 60).zfill(2))

    def setup_cmd_btn(self):
        btn_cmd_x = 1500

        btn_rst_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")
        btn_rst = tk.Button(self.master, text='リセット', command=self.btn_reset, height=int(
            self.canvas_height/1000), width=18, font=btn_rst_font, relief=tk.RAISED, bd=5, anchor=tk.CENTER)
        btn_rst.place(x=btn_cmd_x, y=self.canvas_height*0.8)

        btn_close_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=25, weight="bold")
        btn_close = tk.Button(self.master, text='閉じる', command=self.btn_close, height=int(
            self.canvas_height/1000), width=int(18*18/25)+2, bg='#FF0000', fg='#FFFFFF', font=btn_close_font, anchor=tk.CENTER)
        btn_close.place(x=btn_cmd_x, y=self.canvas_height*0.9)

        self.canvas.create_line(1494, 340, 1792, 340, fill="#696969", width=5)
        self.canvas.create_line(1494, 760, 1792, 760, fill="#696969", width=5)
        btn_times_label_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=24, weight="bold")
        cmd_btn_label = tk.Label(self.master, text='試合進行',
                                 font=btn_times_label_font, anchor=tk.CENTER)
        cmd_btn_label.place(x=1500, y=370)

        btn_times_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")
        btn_times_width = 18
        self.btn_setting_time1 = tk.Button(self.master, text='セッティングタイム1', command=lambda: self.set_mode_timer(self.time_mode.setting1), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_setting_time1.place(x=btn_cmd_x, y=430)

        self.btn_display_time = tk.Button(self.master, text='陳列タイム', command=lambda: self.set_mode_timer(self.time_mode.display_time), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_display_time.place(x=btn_cmd_x, y=500)

        self.btn_setting_time2 = tk.Button(self.master, text='セッティングタイム2', command=lambda: self.set_mode_timer(self.time_mode.setting2), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_setting_time2.place(x=btn_cmd_x, y=590)

        self.btn_sales_time = tk.Button(self.master, text='販売タイム', command=lambda: self.set_mode_timer(self.time_mode.sales_time), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_sales_time.place(x=btn_cmd_x, y=660)

    def def_btns_field_display_time(self):
        self.btn_red_byshelves_hat = []
        self.btn_red_byshelves_sword = []

        self.btn_red_sashelves_hat = []
        self.btn_red_sashelves_sword = []

        self.btn_red_shshelves_hat = []
        self.btn_red_shshelves_sword = []

        self.btn_blue_byshelves_hat = []
        self.btn_blue_byshelves_sword = []

        self.btn_blue_sashelves_hat = []
        self.btn_blue_sashelves_sword = []

        self.btn_blue_shshelves_hat = []
        self.btn_blue_shshelves_sword = []

        btn_toy_acquisition_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=14, weight="bold")
        self.btn_red_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_red_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_blue_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_blue_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)

        for i in range(4):
            self.btn_red_byshelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_red_byshelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_red_byshelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_red_byshelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_byshelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_blue_byshelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_byshelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_blue_byshelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))

        for i in range(2):
            self.btn_red_sashelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_red_sashelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_red_sashelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_red_sashelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_sashelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_blue_sashelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_sashelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_blue_sashelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))

            self.btn_red_shshelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_red_sashelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_red_shshelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_red_sashelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_shshelves_hat.append(tk.Button(
                self.master, text='ハット', command=lambda: self.btn_blue_sashelves_act("hat", i), bg="#FFFFFF", font=btn_toy_acquisition_font))
            self.btn_blue_shshelves_sword.append(tk.Button(
                self.master, text='剣', command=lambda: self.btn_blue_sashelves_act("sword", i), bg="#FFFFFF", font=btn_toy_acquisition_font))

    # TODO: pos変数配列化＆可読性向上
    def show_btns_field_display_time(self):
        btn_toy_acquisition_pos = 70
        self.btn_red_toy_acquisition.place(
            x=self.canvas_width/2-btn_toy_acquisition_pos+self.field_center_shift, y=self.canvas_height*0.63, anchor=tk.CENTER)
        self.btn_blue_toy_acquisition.place(
            x=self.canvas_width/2+btn_toy_acquisition_pos+self.field_center_shift, y=self.canvas_height*0.63, anchor=tk.CENTER)

        btn_byshelves_0_pos = 70
        self.btn_red_byshelves_hat[0].place(
            x=self.canvas_width/2-btn_byshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.825, anchor=tk.CENTER)
        self.btn_red_byshelves_sword[0].place(
            x=self.canvas_width/2-btn_byshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.89, anchor=tk.CENTER)
        self.btn_blue_byshelves_hat[0].place(
            x=self.canvas_width/2+btn_byshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.825, anchor=tk.CENTER)
        self.btn_blue_byshelves_sword[0].place(
            x=self.canvas_width/2+btn_byshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.89, anchor=tk.CENTER)

        btn_byshelves_1_pos = 400
        self.btn_red_byshelves_hat[1].place(
            x=self.canvas_width/2-btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.685, anchor=tk.CENTER)

        btn_byshelves_2_pos = 300
        self.btn_red_byshelves_sword[1].place(
            x=self.canvas_width/2-btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.685, anchor=tk.CENTER)
        self.btn_blue_byshelves_hat[1].place(
            x=self.canvas_width/2+btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.685, anchor=tk.CENTER)
        self.btn_blue_byshelves_sword[1].place(
            x=self.canvas_width/2+btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.685, anchor=tk.CENTER)

        self.btn_red_byshelves_hat[2].place(
            x=self.canvas_width/2-btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.6, anchor=tk.CENTER)
        self.btn_red_byshelves_sword[2].place(
            x=self.canvas_width/2-btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.6, anchor=tk.CENTER)
        self.btn_blue_byshelves_hat[2].place(
            x=self.canvas_width/2+btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.6, anchor=tk.CENTER)
        self.btn_blue_byshelves_sword[2].place(
            x=self.canvas_width/2+btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.6, anchor=tk.CENTER)

        self.btn_red_byshelves_hat[3].place(
            x=self.canvas_width/2-btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.515, anchor=tk.CENTER)
        self.btn_red_byshelves_sword[3].place(
            x=self.canvas_width/2-btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.515, anchor=tk.CENTER)
        self.btn_blue_byshelves_hat[3].place(
            x=self.canvas_width/2+btn_byshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.515, anchor=tk.CENTER)
        self.btn_blue_byshelves_sword[3].place(
            x=self.canvas_width/2+btn_byshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.515, anchor=tk.CENTER)

        btn_sashelves_0_pos = 350
        self.btn_red_sashelves_hat[0].place(
            x=self.canvas_width/2-btn_sashelves_0_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)
        self.btn_blue_sashelves_hat[0].place(
            x=self.canvas_width/2+btn_sashelves_0_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_1_pos = 260
        self.btn_red_sashelves_sword[0].place(
            x=self.canvas_width/2-btn_sashelves_1_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)
        self.btn_blue_sashelves_sword[0].place(
            x=self.canvas_width/2+btn_sashelves_1_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_2_pos = 170
        self.btn_red_sashelves_hat[1].place(
            x=self.canvas_width/2-btn_sashelves_2_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)
        self.btn_blue_sashelves_hat[1].place(
            x=self.canvas_width/2+btn_sashelves_2_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_3_pos = 80
        self.btn_red_sashelves_sword[1].place(
            x=self.canvas_width/2-btn_sashelves_3_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)
        self.btn_blue_sashelves_sword[1].place(
            x=self.canvas_width/2+btn_sashelves_3_pos+self.field_center_shift, y=self.canvas_height*0.405, anchor=tk.CENTER)

        btn_shshelves_0_pos = 400

        self.btn_red_shshelves_hat[0].place(
            x=self.canvas_width/2-btn_shshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)
        self.btn_blue_shshelves_hat[0].place(
            x=self.canvas_width/2+btn_shshelves_0_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_1_pos = 300
        self.btn_red_shshelves_sword[0].place(
            x=self.canvas_width/2-btn_shshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)
        self.btn_blue_shshelves_sword[0].place(
            x=self.canvas_width/2+btn_shshelves_1_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_2_pos = 120
        self.btn_red_shshelves_hat[1].place(
            x=self.canvas_width/2-btn_shshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)
        self.btn_blue_shshelves_hat[1].place(
            x=self.canvas_width/2+btn_shshelves_2_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_3_pos = 40
        self.btn_red_shshelves_sword[1].place(
            x=self.canvas_width/2-btn_shshelves_3_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)
        self.btn_blue_shshelves_sword[1].place(
            x=self.canvas_width/2+btn_shshelves_3_pos+self.field_center_shift, y=self.canvas_height*0.26, anchor=tk.CENTER)

        self.btn_exist = True

    def set_mode_timer(self, mode):
        if self.state_time_mode == mode:
            if mode == self.time_mode.setting1:
                self.btn_setting_time1['bg'] = "#FFFFFF"
            elif mode == self.time_mode.setting2:
                self.btn_setting_time2['bg'] = "#FFFFFF"
            elif mode == self.time_mode.display_time:
                self.btn_display_time['bg'] = "#FFFFFF"
            elif mode == self.time_mode.sales_time:
                self.btn_sales_time['bg'] = "#FFFFFF"

            self.state_time_mode = self.time_mode.NONE
        else:
            # 動作モードは択一式なので、現在のモードを解除
            if self.state_time_mode == self.time_mode.setting1:
                self.btn_setting_time1['bg'] = "#FFFFFF"
            elif self.state_time_mode == self.time_mode.setting2:
                self.btn_setting_time2['bg'] = "#FFFFFF"
            elif self.state_time_mode == self.time_mode.display_time:
                self.btn_display_time['bg'] = "#FFFFFF"
            elif self.state_time_mode == self.time_mode.sales_time:
                self.btn_sales_time['bg'] = "#FFFFFF"

            # 動作モードのボタンを緑色に表示
            if mode == self.time_mode.setting1:
                self.btn_setting_time1['bg'] = "#00FF00"
                self.show_btns_field_display_time()
            elif mode == self.time_mode.setting2:
                self.btn_setting_time2['bg'] = "#00FF00"
            elif mode == self.time_mode.display_time:
                self.btn_display_time['bg'] = "#00FF00"
            elif mode == self.time_mode.sales_time:
                self.btn_sales_time['bg'] = "#00FF00"

            self.timer_reset()
            self.state_time_mode = mode
            self.state_timer_mode = self.timer_mode.stop

    def setup_sales_time(self):
        if self.btn_exist == True:
            self.btn_red_toy_acquisition.place_forget()
            self.btn_blue_toy_acquisition.place_forget()
            for i in range(len(self.btn_red_byshelves_hat)):
                self.btn_red_byshelves_hat[i].place_forget()
                self.btn_red_byshelves_sword[i].place_forget()
                self.btn_blue_byshelves_hat[i].place_forget()
                self.btn_blue_byshelves_sword[i].place_forget()
            for i in range(len(self.btn_red_sashelves_hat)):
                self.btn_red_sashelves_hat[i].place_forget()
                self.btn_red_sashelves_sword[i].place_forget()
                self.btn_blue_sashelves_hat[i].place_forget()
                self.btn_blue_sashelves_sword[i].place_forget()
            for i in range(len(self.btn_red_shshelves_hat)):
                self.btn_red_shshelves_hat[i].place_forget()
                self.btn_red_shshelves_sword[i].place_forget()
                self.btn_blue_shshelves_hat[i].place_forget()
                self.btn_blue_shshelves_sword[i].place_forget()

    def writeToLog(self, msg):
        self.log['state'] = 'normal'
        if self.log.index('end-1c') != '1.0':
            self.log.insert('1.0', '\n')

        # タイムスタンプ付与（0.1秒単位）
        time_raw = datetime.datetime.now()
        time_sec = time_raw.strftime('%Y-%m-%d %H:%M:%S.%f')
        tail = time_sec[-7:]
        f = round(float(tail), 1)
        tmp = "%.1f" % f

        # Log出力
        self.log.insert('1.0', str(time_sec[:-7])+str(tmp[1:]) + "\t" + msg)
        self.log['state'] = 'disabled'

    # 得点更新
    def update_points(self):
        self.red_points_text.set(str(self.red_points))
        self.blue_points_text.set(str(self.blue_points))
        if self.red_toy_counters >= 6:
            self.writeToLog("赤チーム：陳列タイム　終了")
        if self.blue_toy_counters >= 6:
            self.writeToLog("青チーム：陳列タイム　終了")

    def update_team_name(self, event):
        if self.red_team_text.get() != self.red_team.get():
            self.red_team_text.set(self.red_team.get())
            self.writeToLog("赤チーム："+self.red_team_text.get()+"\tが設定されました。")
        if self.blue_team_text.get() != self.blue_team.get():
            self.blue_team_text.set(self.blue_team.get())
            self.writeToLog("青チーム："+self.blue_team_text.get()+"\tが設定されました。")

    # ウィンドウクローズ
    def btn_close(self):
        self.master.destroy()

    def btn_red_toy_acquisition_act(self):
        if self.state.red_toy_acquisition == False:
            self.red_points = self.red_points+5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#00FF00"
            self.state.red_toy_acquisition = True
            self.writeToLog("赤チーム：おもちゃ取得\t+5点")
        else:
            self.red_points = self.red_points-5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#FFFFFF"
            self.state.red_toy_acquisition = False
            self.writeToLog("赤チーム：おもちゃ取得取り消し\t-5点")

    def btn_blue_toy_acquisition_act(self):
        if self.state.blue_toy_acquisition == False:
            self.blue_points = self.blue_points+5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#00FF00"
            self.state.blue_toy_acquisition = True
            self.writeToLog("青チーム：おもちゃ取得\t+5点")
        else:
            self.blue_points = self.blue_points-5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#FFFFFF"
            self.state.blue_toy_acquisition = False
            self.writeToLog("青チーム：おもちゃ取得取り消し\t-5点")

    def btn_red_byshelves_act(self, type, id):
        if self.position_state_red["back_yard"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_red_byshelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_red["back_yard"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points+10
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：バックヤード\tハット　配置\t+10点")
                else:
                    self.red_points = self.red_points+5
                    self.writeToLog("赤チーム：バックヤード\tハット　配置\t+5点")
            else:
                self.btn_red_byshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_red["back_yard"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points+5
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：バックヤード\t剣　配置\t+5点")
                else:
                    self.writeToLog("赤チーム：バックヤード\t剣　配置")
            self.update_points()
            self.position_state_red["back_yard"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_red_byshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_red["back_yard"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points-10
                    self.writeToLog("赤チーム：バックヤード\tハット　配置取り消し\t-10点")
                    self.red_toy_counters -= 1
                else:
                    self.red_points = self.red_points-5
                    self.writeToLog("赤チーム：バックヤード\tハット　配置取り消し\t-5点")
            else:
                self.btn_red_byshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_red["back_yard"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points-5
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：バックヤード\t剣　配置取り消し\t-5点")
                else:
                    self.writeToLog("赤チーム：バックヤード\t剣　配置取り消し")
            self.update_points()
            self.position_state_red["back_yard"]["shelves"][type][id] = False

    def btn_blue_byshelves_act(self, type, id):
        if self.position_state_blue["back_yard"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_blue_byshelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_blue["back_yard"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points+10
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：バックヤード\tハット　配置\t+10点")
                else:
                    self.blue_points = self.blue_points+5
                    self.writeToLog("青チーム：バックヤード\tハット　配置\t+5点")
            else:
                self.btn_blue_byshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+5
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：バックヤード\t剣　配置\t+5点")
                else:
                    self.writeToLog("青チーム：バックヤード\t剣　配置")
            self.update_points()
            self.position_state_blue["back_yard"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_byshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-10
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：バックヤード\tハット　配置取り消し\t-10点")
                else:
                    self.blue_points = self.blue_points-5
                    self.writeToLog("青チーム：バックヤード\tハット　配置取り消し\t-5点")
            else:
                self.btn_blue_byshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-5
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：バックヤード\t剣　配置取り消し\t-5点")
                else:
                    self.writeToLog("青チーム：バックヤード\t剣　配置取り消し")
            self.update_points()
            self.position_state_blue["back_yard"]["shelves"][type][id] = False

    def btn_red_sashelves_act(self, type, id):
        if self.position_state_red["sales_floor"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_red_sashelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_red["sales_floor"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points+20
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：売り場\tハット　配置\t+20点")
                else:
                    self.red_points = self.red_points+5
                    self.writeToLog("赤チーム：売り場\tハット　配置\t+5点")
            else:
                self.btn_red_sashelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_red["sales_floor"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points+15
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：売り場\t剣　配置\t+15点")
                else:
                    self.writeToLog("赤チーム：売り場\t剣　配置")
            self.update_points()
            self.position_state_red["sales_floor"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_red_sashelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_red["sales_floor"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points-20
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：売り場\tハット　配置取り消し\t-20点")
                else:
                    self.red_points = self.red_points-5
                    self.writeToLog("赤チーム：売り場\tハット　配置取り消し\t-5点")
            else:
                self.btn_red_sashelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_red["sales_floor"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points-15
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：売り場\t剣　配置取り消し\t-15点")
                else:
                    self.writeToLog("赤チーム：売り場\t剣　配置取り消し")
            self.update_points()
            self.position_state_red["sales_floor"]["shelves"][type][id] = False

    def btn_blue_sashelves_act(self, type, id):
        if self.position_state_blue["sales_floor"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_blue_sashelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_blue["sales_floor"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points+20
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：売り場\tハット　配置\t+20点")
                else:
                    self.blue_points = self.blue_points+5
                    self.writeToLog("青チーム：売り場\tハット　配置\t+5点")
            else:
                self.btn_blue_sashelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["sales_floor"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+15
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：売り場\t剣　配置\t+15点")
                else:
                    self.writeToLog("青チーム：売り場\t剣　配置")
            self.update_points()
            self.position_state_blue["sales_floor"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_sashelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["sales_floor"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-20
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：売り場\tハット　配置取り消し\t-20点")
                else:
                    self.blue_points = self.blue_points-5
                    self.writeToLog("青チーム：売り場\tハット　配置取り消し\t-5点")
            else:
                self.btn_blue_sashelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["sales_floor"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-15
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：売り場\t剣　配置取り消し\t+15点")
                else:
                    self.writeToLog("青チーム：売り場\t剣　配置取り消し")
            self.update_points()
            self.position_state_blue["sales_floor"]["shelves"][type][id] = False

    def btn_red_shshelves_act(self, type, id):
        if self.position_state_red["showcase"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_red_shshelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_red["showcase"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points+30
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：ショーケース\tハット　配置\t+30点")
                else:
                    self.red_points = self.red_points+5
                    self.writeToLog("赤チーム：ショーケース\tハット　配置\t+5点")
            else:
                self.btn_red_shshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_red["showcase"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points+25
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：ショーケース\t剣　配置\t+25点")
                else:
                    self.writeToLog("赤チーム：ショーケース\t剣　配置")
            self.update_points()
            self.position_state_red["showcase"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_red_shshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_red["showcase"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points-30
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：ショーケース\tハット　配置取り消し\t-30点")
                else:
                    self.red_points = self.red_points-5
                    self.writeToLog("赤チーム：ショーケース\tハット　配置取り消し\t-5点")
            else:
                self.btn_red_shshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_red["showcase"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points-25
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：ショーケース\t剣　配置取り消し\t-25点")
                else:
                    self.writeToLog("赤チーム：ショーケース\t剣　配置取り消し")
            self.update_points()
            self.position_state_red["showcase"]["shelves"][type][id] = False

    def btn_blue_shshelves_act(self, type, id):
        if self.position_state_blue["showcase"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_blue_shshelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_blue["showcase"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points+30
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：ショーケース\tハット　配置\t+30点")
                else:
                    self.blue_points = self.blue_points+5
                    self.writeToLog("青チーム：ショーケース\tハット　配置\t+5点")
            else:
                self.btn_blue_shshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["showcase"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+25
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：ショーケース\t剣　配置\t+25点")
                else:
                    self.writeToLog("青チーム：ショーケース\t剣　配置")
            self.update_points()
            self.position_state_blue["showcase"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_shshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["showcase"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-30
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：ショーケース\tハット　配置取り消し\t-30点")
                else:
                    self.blue_points = self.blue_points-5
                    self.writeToLog("青チーム：ショーケース\tハット　配置取り消し\t-5点")
            else:
                self.btn_blue_shshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["showcase"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-25
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：ショーケース\t剣　配置取り消し\t-25点")
                else:
                    self.writeToLog("青チーム：ショーケース\t剣　配置取り消し")
            self.update_points()
            self.position_state_blue["showcase"]["shelves"][type][id] = False

    def btn_reset(self):
        self.red_points = 0
        self.blue_points = 0
        self.red_toy_counters = 0
        self.blue_toy_counters = 0

        # フィールド上のボタンのリセット
        self.btn_red_toy_acquisition["bg"] = "#FFFFFF"
        self.state.red_toy_acquisition = False
        self.btn_blue_toy_acquisition["bg"] = "#FFFFFF"
        self.state.blue_toy_acquisition = False

        for i in range(len(self.position_state_red["back_yard"]["shelves"]["hat"])):
            self.position_state_red["back_yard"]["shelves"]["hat"][i] = False
            self.btn_red_byshelves_hat[i]['bg'] = "#FFFFFF"
            self.position_state_red["back_yard"]["shelves"]["sword"][i] = False
            self.btn_red_byshelves_sword[i]['bg'] = "#FFFFFF"
        for i in range(len(self.position_state_red["sales_floor"]["shelves"]["hat"])):
            self.position_state_red["sales_floor"]["shelves"]["hat"][i] = False
            self.btn_red_sashelves_hat[i]['bg'] = "#FFFFFF"
            self.position_state_red["sales_floor"]["shelves"]["sword"][i] = False
            self.btn_red_sashelves_sword[i]['bg'] = "#FFFFFF"
        for i in range(len(self.position_state_red["showcase"]["shelves"]["hat"])):
            self.position_state_red["showcase"]["shelves"]["hat"][i] = False
            self.btn_red_shshelves_hat[i]['bg'] = "#FFFFFF"
            self.position_state_red["showcase"]["shelves"]["sword"][i] = False
            self.btn_red_shshelves_sword[i]['bg'] = "#FFFFFF"

        self.update_points()


if __name__ == "__main__":
    app = Application()
