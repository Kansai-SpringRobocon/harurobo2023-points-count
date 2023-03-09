#
# harurobo2023-points-count/main.py
#
# (c) 2022 関西春ロボコン運営委員会 / Haru Robocon in Kansai
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#
#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk
from PIL import ImageTk
import json
import datetime
from enum import Enum
import pygame
from enum import IntEnum


class Application(tk.Frame):
    class time_mode(Enum):
        setting1 = 1
        setting2 = 2
        display_time = 3
        sales_time = 4
        NONE = 99

    class timer_mode(Enum):
        stop = 0
        run = 1
        pause = 2
        end = 3
        count_down_to_run = 4
        count_down = 5
        restart = 6

    class field_color(IntEnum):
        red = 0
        blue = 1
        NONE = 99

    class object(IntEnum):
        hat = 0
        sword = 1

    pygame.mixer.init(frequency=44100)    # 音声初期設定

    class sound():
        start = pygame.mixer.Sound(
            ".\sound\start.mp3")
        count_down = pygame.mixer.Sound(
            ".\sound\count_down.mp3")
        end = pygame.mixer.Sound(".\sound\end.mp3")

    red_points = 0
    blue_points = 0

    red_toy_counters = 0
    blue_toy_counters = 0

    class state():
        red_toy_acquisition = False
        blue_toy_acquisition = False

        red_sold_out = False
        blue_sold_out = False

        shelves_setting_time2 = [
            [[False, False]for i in range(2)]for i in range(8)]

    state_time_mode = time_mode.NONE
    state_timer_mode = timer_mode.stop
    state_first_sold_out = field_color.NONE
    state_first_end_display_time = field_color.NONE

    btn_exist = False

    red_team_name = "チーム名を\n選択してください"
    blue_team_name = "チーム名を\n選択してください"

    team_list = {}
    with open("./setting/team.json", mode="r", encoding="utf-8") as team_list_file:
        team_list = json.load(team_list_file)

    position_state_red = {}
    position_state_blue = {}
    with open("./setting/area_state.json", mode="r", encoding="utf-8") as area_state:
        position_state_red = json.load(area_state)
    with open("./setting/area_state.json", mode="r", encoding="utf-8") as area_state:
        position_state_blue = json.load(area_state)

    def __init__(self):
        self.master = tk.Tk()

        self.master.title("春ロボコン2023 得点計算ツール")       # ウィンドウタイトル
        self.master.geometry("1792x1008")     # ウィンドウサイズ(幅x高さ)
        # self.master.attributes('-fullscreen', True)
        self.master.iconbitmap(default='./img/harurobo.ico')  # アイコン設定

        self.canvas = tk.Canvas(self.master)  # Canvasの作成
        self.canvas.pack(expand=True, fill=tk.BOTH)  # Canvasを配置

        app_name_label = tk.Label(self.master, text="春ロボコン2023\n得点計算ツール",
                                  fg="#000000", font=("HGPゴシックE", 18, "bold"), anchor=tk.CENTER)
        app_name_label.place(x=80, y=20)

        # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        self.photo_image = ImageTk.PhotoImage(file="./img/field.png")
        self.kansai_harurobo_logo = ImageTk.PhotoImage(
            file="./img/kansai-harurobo.png")

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

        self.btn_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=14, weight="bold")
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
        self.timer_record_txt = tk.StringVar()

        self.timer_record_display_time_str = ""
        self.timer_record_sales_time_str = ""
        self.timer_sold_out_time = [999, 999]

        timer_font = tk_font.Font(self.master, family="HGPゴシックE",
                                  size=42, weight="bold")
        timer_state_font = tk_font.Font(self.master, family="HGPゴシックE",
                                        size=20, weight="bold")
        timer_record_font = tk_font.Font(self.master, family="HGPゴシックE",
                                         size=16, weight="bold")
        self.timer_state_label = tk.Label(
            self.master, textvariable=self.timer_state_txt, font=timer_state_font, anchor=tk.CENTER)
        self.timer_min_label = tk.Label(
            self.master, textvariable=self.timer_min_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_colon_label = tk.Label(
            self.master, textvariable=self.timer_colon_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_sec_label = tk.Label(
            self.master, textvariable=self.timer_sec_txt, font=timer_font, anchor=tk.CENTER)
        self.timer_record_label = tk.Label(
            self.master, textvariable=self.timer_record_txt, font=timer_record_font, anchor=tk.CENTER)

        self.btn_shelves_x_pos = [70, 400, 300,
                                  350, 260, 170, 80, 400, 300, 120, 40]
        self.btn_shelves_y_pos = [872, 938, 730, 635, 550, 418, 262]

        self.btn_shelves_pos = [[[] for i in range(2)]for i in range(2)]
        self.btn_shelves_pos[self.object.hat] = [
            [self.btn_shelves_x_pos[0], self.btn_shelves_y_pos[0]], [self.btn_shelves_x_pos[1], self.btn_shelves_y_pos[2]], [self.btn_shelves_x_pos[1], self.btn_shelves_y_pos[3]], [self.btn_shelves_x_pos[1], self.btn_shelves_y_pos[4]], [self.btn_shelves_x_pos[3], self.btn_shelves_y_pos[5]], [self.btn_shelves_x_pos[5], self.btn_shelves_y_pos[5]], [self.btn_shelves_x_pos[7], self.btn_shelves_y_pos[6]], [self.btn_shelves_x_pos[9], self.btn_shelves_y_pos[6]]]
        self.btn_shelves_pos[self.object.sword] = [
            [self.btn_shelves_x_pos[0], self.btn_shelves_y_pos[1]], [self.btn_shelves_x_pos[2], self.btn_shelves_y_pos[2]], [self.btn_shelves_x_pos[2], self.btn_shelves_y_pos[3]], [self.btn_shelves_x_pos[2], self.btn_shelves_y_pos[4]], [self.btn_shelves_x_pos[4], self.btn_shelves_y_pos[5]], [self.btn_shelves_x_pos[6], self.btn_shelves_y_pos[5]], [self.btn_shelves_x_pos[8], self.btn_shelves_y_pos[6]], [self.btn_shelves_x_pos[10], self.btn_shelves_y_pos[6]]]

        self.btn_txt = ['ハット', '剣']

        self.timer_set_state_txt()
        self.timer_set_sec()

        self.def_btns_field_display_time()
        self.def_btns_field_setting_time2()
        self.def_btns_field_sales_time()
        self.setup_timer_btn()
        self.setup_cmd_btn()

        self.master.mainloop()

    def setup_timer_btn(self):
        self.canvas.create_line(1494, 170, 1792, 170, fill="#696969", width=5)
        btn_timer_label_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=24, weight="bold")
        cmd_btn_label = tk.Label(self.master, text='タイマー操作',
                                 font=btn_timer_label_font, anchor=tk.CENTER)
        cmd_btn_label.place(x=1500, y=180)
        btn_timer_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=15, weight="bold")
        self.btn_timer_start = tk.Button(self.master, text='開始', command=self.timer_start,
                                         width=4, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#4169e1", fg="#FFFFFF")
        self.btn_timer_start.place(x=1530, y=230)
        self.btn_timer_pause = tk.Button(self.master, text='一時停止', command=self.timer_pause,
                                         width=8, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#e0e041")
        # btn_timer_pause.place(x=1510, y=230)
        self.btn_timer_reset = tk.Button(self.master, text='リセット', command=self.timer_reset,
                                         width=8, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#e04141", fg="#FFFFFF")
        self.btn_timer_reset.place(x=1650, y=230)
        self.btn_timer_restart = tk.Button(self.master, text='再開', command=self.timer_restart,
                                           width=8, font=btn_timer_font, relief=tk.RAISED, bd=6, anchor=tk.CENTER, bg="#3838ff", fg="#FFFFFF")
        # self.btn_timer_restart.place(x=1650, y=230)
        notes_timer_label_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=11, weight="bold")
        notes_btn_label = tk.Label(self.master, text='※カウントダウン中に一時停止すると\n　バグるのでリセットすること',
                                   font=notes_timer_label_font, anchor=tk.W)
        notes_btn_label.place(x=1500, y=290)

    def timer_start(self):
        self.btn_timer_pause.place(x=1510, y=230)
        self.btn_timer_start.place_forget()
        self.state_timer_mode = self.timer_mode.count_down
        self.timer_sec = 5
        self.timer_set_state_txt()
        self.timer()

    def timer_restart(self):
        self.btn_timer_pause.place(x=1510, y=230)
        self.btn_timer_restart.place_forget()
        self.state_timer_mode = self.timer_mode.restart
        self.timer_set_state_txt()
        self.timer()

    def timer_pause(self):
        self.btn_timer_restart.place(x=1510, y=230)
        self.btn_timer_pause.place_forget()
        self.state_timer_mode = self.timer_mode.pause
        self.timer_set_state_txt()

    def timer_set_state_txt(self):
        self.timer_record_str = ""
        if self.state_timer_mode == self.timer_mode.count_down:
            self.timer_state_txt.set("Ready?")
        elif self.state_timer_mode == self.timer_mode.pause:
            self.timer_state_txt.set("一時停止中")
        elif self.state_timer_mode == self.timer_mode.restart:
            self.timer_state_txt.set("再開！")
        elif self.state_time_mode == self.time_mode.setting1:
            self.timer_state_txt.set("セッティングタイム1")
        elif self.state_time_mode == self.time_mode.setting2:
            self.timer_state_txt.set("セッティングタイム2")
        elif self.state_time_mode == self.time_mode.display_time:
            self.timer_state_txt.set("陳列タイム")
            self.timer_record_str = self.timer_record_display_time_str
        elif self.state_time_mode == self.time_mode.sales_time:
            self.timer_state_txt.set("販売タイム")
            self.timer_record_str = self.timer_record_sales_time_str
        elif self.state_time_mode == self.time_mode.NONE:
            self.timer_state_txt.set("")

        self.timer_state_label.place(x=1643, y=35, anchor=tk.CENTER)

        self.timer_record_txt.set(self.timer_record_str)
        self.timer_record_label.place(x=1643, y=140, anchor=tk.CENTER)

    def timer_set_sec(self):
        if (self.state_time_mode == self.time_mode.NONE) or (self.state_time_mode == self.time_mode.setting1) or (self.state_time_mode == self.time_mode.setting2):
            self.timer_sec = 60
        else:
            self.timer_sec = 90
        self.timer_colon_txt.set(":")
        self.timer_min_label.place(x=1593, y=85, anchor=tk.CENTER)
        self.timer_colon_label.place(x=1643, y=80, anchor=tk.CENTER)
        self.timer_sec_label.place(x=1693, y=85, anchor=tk.CENTER)
        self.timer_show()

    def timer_reset(self):
        self.timer_set_sec()
        self.state_timer_mode = self.timer_mode.stop
        self.timer_set_state_txt()
        self.btn_timer_start.place(x=1530, y=230)
        self.btn_timer_pause.place_forget()
        self.btn_timer_restart.place_forget()

    def timer(self):
        if self.state_timer_mode == self.timer_mode.count_down:
            if self.timer_sec == 0:
                self.timer_sec_label.place_forget()
                self.timer_min_label.place_forget()
                self.timer_state_label.place_forget()
                self.timer_colon_txt.set("START!")
                self.sound.start.play()
                self.state_timer_mode = self.timer_mode.count_down_to_run
            else:
                self.timer_show()
                self.timer_sec -= 1
                self.sound.count_down.play()

            self.master.after(1000, self.timer)
        elif self.state_timer_mode == self.timer_mode.count_down_to_run:
            self.timer_set_sec()
            self.state_timer_mode = self.timer_mode.run
            self.timer_set_state_txt()

        if self.state_timer_mode == self.timer_mode.run:
            self.timer_set_state_txt()
            if self.timer_sec == 0:
                self.timer_sec_label.place_forget()
                self.timer_min_label.place_forget()
                self.timer_colon_txt.set("Finish!")
                self.sound.end.play()
                self.state_timer_mode = self.timer_mode.end
            if self.state_timer_mode == self.timer_mode.run:
                self.timer_show()
                self.timer_sec -= 1
                self.master.after(1000, self.timer)
        if self.state_timer_mode == self.timer_mode.restart:
            self.state_timer_mode = self.timer_mode.run
            self.master.after(1000, self.timer)

    def timer_show(self):
        if self.timer_sec < 60:
            self.timer_sec_txt.set(str(self.timer_sec).zfill(2))
            self.timer_min_txt.set("00")
        else:
            self.timer_min_txt.set(str(int(self.timer_sec/60)).zfill(2))
            self.timer_sec_txt.set(str(self.timer_sec % 60).zfill(2))

    def setup_cmd_btn(self):
        btn_cmd_x = 1643

        btn_rst_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")
        btn_rst = tk.Button(self.master, text='リセット', command=self.btn_reset, height=int(
            self.canvas_height/1000), width=18, font=btn_rst_font, relief=tk.RAISED, bd=5, anchor=tk.CENTER)
        btn_rst.place(x=btn_cmd_x, y=self.canvas_height*0.8, anchor=tk.CENTER)

        btn_close_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=25, weight="bold")
        btn_close = tk.Button(self.master, text='閉じる', command=self.btn_close, height=int(
            self.canvas_height/1000), width=int(18*18/25)+2, bg='#FF0000', fg='#FFFFFF', font=btn_close_font, anchor=tk.CENTER)
        btn_close.place(x=btn_cmd_x, y=self.canvas_height *
                        0.9, anchor=tk.CENTER)

        self.canvas.create_line(1494, 340, 1792, 340, fill="#696969", width=5)
        self.canvas.create_line(1494, 760, 1792, 760, fill="#696969", width=5)
        btn_times_label_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=24, weight="bold")
        cmd_btn_label = tk.Label(self.master, text='試合進行',
                                 font=btn_times_label_font, anchor=tk.CENTER)
        cmd_btn_label.place(x=1510, y=370)

        btn_times_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")
        btn_times_width = 18
        self.btn_setting_time1 = tk.Button(self.master, text='セッティングタイム1', command=lambda: self.set_mode_timer(self.time_mode.setting1), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_display_time = tk.Button(self.master, text='陳列タイム', command=lambda: self.set_mode_timer(self.time_mode.display_time), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_setting_time2 = tk.Button(self.master, text='セッティングタイム2', command=lambda: self.set_mode_timer(self.time_mode.setting2), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font, anchor=tk.CENTER)
        self.btn_sales_time = tk.Button(self.master, text='販売タイム', command=lambda: self.set_mode_timer(self.time_mode.sales_time), height=int(
            self.canvas_height/1000), width=btn_times_width, bg='#FFFFFF', fg='#000000', font=btn_times_font)

        self.btn_setting_time1.place(x=btn_cmd_x, y=460, anchor=tk.CENTER)
        self.btn_display_time.place(x=btn_cmd_x, y=540, anchor=tk.CENTER)
        self.btn_setting_time2.place(x=btn_cmd_x, y=620, anchor=tk.CENTER)
        self.btn_sales_time.place(x=btn_cmd_x, y=700, anchor=tk.CENTER)

    # 陳列タイムのボタン設定
    def def_btns_field_display_time(self):
        self.btn_red_shelves_hat = []
        self.btn_red_shelves_sword = []

        self.btn_red_sashelves_hat = []
        self.btn_red_sashelves_sword = []

        self.btn_red_shshelves_hat = []
        self.btn_red_shshelves_sword = []

        self.btn_blue_shelves_hat = []
        self.btn_blue_shelves_sword = []

        self.btn_blue_sashelves_hat = []
        self.btn_blue_sashelves_sword = []

        self.btn_blue_shshelves_hat = []
        self.btn_blue_shshelves_sword = []

        self.btn_red_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_red_toy_acquisition_act, bg="#FFFFFF", font=self.btn_font)
        self.btn_blue_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_blue_toy_acquisition_act, bg="#FFFFFF", font=self.btn_font)

        self.btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_byshelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_byshelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_byshelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_byshelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_byshelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_byshelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_byshelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_byshelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_byshelves_act("hat", 2), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_byshelves_act("sword", 2), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_byshelves_act("hat", 2), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_byshelves_act("sword", 2), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_byshelves_act("hat", 3), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_byshelves_act("sword", 3), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_byshelves_act("hat", 3), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_byshelves_act("sword", 3), bg="#FFFFFF", font=self.btn_font))

        self.btn_red_sashelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_sashelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_sashelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_sashelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_sashelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_sashelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_sashelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_sashelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_sashelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_sashelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_sashelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_sashelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_sashelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_sashelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_sashelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_sashelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))

        self.btn_red_shshelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_shshelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shshelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_shshelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shshelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_shshelves_act("hat", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shshelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_shshelves_act("sword", 0), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shshelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_red_shshelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_red_shshelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_red_shshelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shshelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.btn_blue_shshelves_act("hat", 1), bg="#FFFFFF", font=self.btn_font))
        self.btn_blue_shshelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.btn_blue_shshelves_act("sword", 1), bg="#FFFFFF", font=self.btn_font))

    def show_btns_field_display_time(self):
        btn_toy_acquisition_pos = 70
        self.btn_red_toy_acquisition.place(
            x=self.canvas_width/2-btn_toy_acquisition_pos+self.field_center_shift, y=self.canvas_height*0.63, anchor=tk.CENTER)
        self.btn_blue_toy_acquisition.place(
            x=self.canvas_width/2+btn_toy_acquisition_pos+self.field_center_shift, y=self.canvas_height*0.63, anchor=tk.CENTER)

        self.btn_red_shelves_hat[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[0]+self.field_center_shift, y=self.btn_shelves_y_pos[0], anchor=tk.CENTER)
        self.btn_red_shelves_sword[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[0]+self.field_center_shift, y=self.btn_shelves_y_pos[1], anchor=tk.CENTER)
        self.btn_blue_shelves_hat[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[0]+self.field_center_shift, y=self.btn_shelves_y_pos[0], anchor=tk.CENTER)
        self.btn_blue_shelves_sword[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[0]+self.field_center_shift, y=self.btn_shelves_y_pos[1], anchor=tk.CENTER)

        self.btn_red_shelves_hat[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[2], anchor=tk.CENTER)
        self.btn_red_shelves_sword[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[2], anchor=tk.CENTER)
        self.btn_blue_shelves_hat[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[2], anchor=tk.CENTER)
        self.btn_blue_shelves_sword[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[2], anchor=tk.CENTER)

        self.btn_red_shelves_hat[2].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[3], anchor=tk.CENTER)
        self.btn_red_shelves_sword[2].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[3], anchor=tk.CENTER)
        self.btn_blue_shelves_hat[2].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[3], anchor=tk.CENTER)
        self.btn_blue_shelves_sword[2].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[3], anchor=tk.CENTER)

        self.btn_red_shelves_hat[3].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[4], anchor=tk.CENTER)
        self.btn_red_shelves_sword[3].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[4], anchor=tk.CENTER)
        self.btn_blue_shelves_hat[3].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[1]+self.field_center_shift, y=self.btn_shelves_y_pos[4], anchor=tk.CENTER)
        self.btn_blue_shelves_sword[3].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[2]+self.field_center_shift, y=self.btn_shelves_y_pos[4], anchor=tk.CENTER)

        self.btn_red_sashelves_hat[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[3]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_blue_sashelves_hat[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[3]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_red_sashelves_sword[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[4]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_blue_sashelves_sword[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[4]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)

        self.btn_red_sashelves_hat[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[5]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_blue_sashelves_hat[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[5]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_red_sashelves_sword[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[6]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)
        self.btn_blue_sashelves_sword[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[6]+self.field_center_shift, y=self.btn_shelves_y_pos[5], anchor=tk.CENTER)

        self.btn_red_shshelves_hat[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[7]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_blue_shshelves_hat[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[7]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_red_shshelves_sword[0].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[8]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_blue_shshelves_sword[0].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[8]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)

        self.btn_red_shshelves_hat[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[9]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_blue_shshelves_hat[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[9]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_red_shshelves_sword[1].place(
            x=self.canvas_width/2-self.btn_shelves_x_pos[10]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)
        self.btn_blue_shshelves_sword[1].place(
            x=self.canvas_width/2+self.btn_shelves_x_pos[10]+self.field_center_shift, y=self.btn_shelves_y_pos[6], anchor=tk.CENTER)

        self.btn_exist = True

    def hide_btns_field_display_time(self):
        self.btn_red_toy_acquisition.place_forget()
        self.btn_blue_toy_acquisition.place_forget()
        for i in range(len(self.position_state_red["back_yard"]["shelves"]["hat"])):
            self.btn_red_shelves_hat[i].place_forget()
            self.btn_blue_shelves_hat[i].place_forget()
            self.btn_red_shelves_sword[i].place_forget()
            self.btn_blue_shelves_sword[i].place_forget()
        for i in range(len(self.position_state_red["sales_floor"]["shelves"]["hat"])):
            self.btn_red_sashelves_hat[i].place_forget()
            self.btn_blue_sashelves_hat[i].place_forget()
            self.btn_red_sashelves_sword[i].place_forget()
            self.btn_blue_sashelves_sword[i].place_forget()
        for i in range(len(self.position_state_red["showcase"]["shelves"]["hat"])):
            self.btn_red_shshelves_hat[i].place_forget()
            self.btn_blue_shshelves_hat[i].place_forget()
            self.btn_red_shshelves_sword[i].place_forget()
            self.btn_blue_shshelves_sword[i].place_forget()

    def reset_btns_field_display_time(self):
        self.btn_red_toy_acquisition["bg"] = "#FFFFFF"
        self.state.red_toy_acquisition = False
        self.btn_blue_toy_acquisition["bg"] = "#FFFFFF"
        self.state.blue_toy_acquisition = False
        self.timer_record_display_time_str = ""
        for i in range(len(self.position_state_red["back_yard"]["shelves"]["hat"])):
            self.btn_red_shelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_red["back_yard"]["shelves"]["hat"][i] = False
            self.btn_blue_shelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_blue["back_yard"]["shelves"]["hat"][i] = False
            self.btn_red_shelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_red["back_yard"]["shelves"]["sword"][i] = False
            self.btn_blue_shelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_blue["back_yard"]["shelves"]["sword"][i] = False
        for i in range(len(self.position_state_red["sales_floor"]["shelves"]["hat"])):
            self.btn_red_sashelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_red["sales_floor"]["shelves"]["hat"][i] = False
            self.btn_blue_sashelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_blue["sales_floor"]["shelves"]["hat"][i] = False
            self.btn_red_sashelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_blue["sales_floor"]["shelves"]["sword"][i] = False
            self.btn_blue_sashelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_blue["sales_floor"]["shelves"]["sword"][i] = False
        for i in range(len(self.position_state_red["showcase"]["shelves"]["hat"])):
            self.btn_red_shshelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_red["showcase"]["shelves"]["hat"][i] = False
            self.btn_blue_shshelves_hat[i]["bg"] = "#FFFFFF"
            self.position_state_blue["showcase"]["shelves"]["hat"][i] = False
            self.btn_red_shshelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_red["showcase"]["shelves"]["sword"][i] = False
            self.btn_blue_shshelves_sword[i]["bg"] = "#FFFFFF"
            self.position_state_blue["showcase"]["shelves"]["sword"][i] = False

    def def_btns_field_setting_time2(self):
        self.st2btn_red_shelves_hat = []
        self.st2btn_red_shelves_sword = []

        self.st2btn_blue_shelves_hat = []
        self.st2btn_blue_shelves_sword = []

        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 0), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 0), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 0), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 0), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 1), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 1), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 1), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 1), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 2), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 2), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 2), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 2), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 3), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 3), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 3), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 3), bg="#FFFFFF", font=self.btn_font))

        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 4), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 4), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 4), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 4), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 5), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 5), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 5), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 5), bg="#FFFFFF", font=self.btn_font))

        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 6), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 6), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 6), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 6), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_red_shelves_act(self.object.hat, 7), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_red_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_red_shelves_act(self.object.sword, 7), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_hat.append(tk.Button(
            self.master, text=self.btn_txt[self.object.hat], command=lambda: self.st2btn_blue_shelves_act(self.object.hat, 7), bg="#FFFFFF", font=self.btn_font))
        self.st2btn_blue_shelves_sword.append(tk.Button(
            self.master, text=self.btn_txt[self.object.sword], command=lambda: self.st2btn_blue_shelves_act(self.object.sword, 7), bg="#FFFFFF", font=self.btn_font))

        btn_st2_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")
        self.btn_count_st2 = [[]for i in range(2)]
        btn_width = 1

        self.btn_count_st2[self.field_color.red].append(tk.Button(
            self.master, text="+", command=lambda: self.btn_count_st2_act(self.field_color.red, 1), bg="#FFFFFF", font=btn_st2_font, width=btn_width))
        self.btn_count_st2[self.field_color.red].append(tk.Button(
            self.master, text="-", command=lambda: self.btn_count_st2_act(self.field_color.red, -1), bg="#FFFFFF", font=btn_st2_font, width=btn_width))

        self.btn_count_st2[self.field_color.blue].append(tk.Button(
            self.master, text="+", command=lambda: self.btn_count_st2_act(self.field_color.blue, 1), bg="#FFFFFF", font=btn_st2_font, width=btn_width))
        self.btn_count_st2[self.field_color.blue].append(tk.Button(
            self.master, text="-", command=lambda: self.btn_count_st2_act(self.field_color.blue, -1), bg="#FFFFFF", font=btn_st2_font, width=btn_width))

        self.warehouse_num = [0, 0]
        self.warehouse_num_text = []
        self.warehouse_num_label = []
        for i in range(2):
            self.warehouse_num_text.append(tk.StringVar())
            self.warehouse_num_text[i].set(
                str(self.warehouse_num[i]))
            self.warehouse_num_label.append(tk.Label(self.master, textvariable=self.warehouse_num_text[i],
                                                     fg="#000000", bg="#FFFFFF", font=btn_st2_font, width=2))

    def show_btns_field_setting_time2(self):
        for i in range(len(self.st2btn_red_shelves_hat)):
            self.st2btn_red_shelves_hat[i].place(
                x=self.canvas_width/2-self.btn_shelves_pos[self.object.hat][i][0]+self.field_center_shift, y=self.btn_shelves_pos[self.object.hat][i][1], anchor=tk.CENTER)
            self.st2btn_blue_shelves_hat[i].place(
                x=self.canvas_width/2+self.btn_shelves_pos[self.object.hat][i][0]+self.field_center_shift, y=self.btn_shelves_pos[self.object.hat][i][1], anchor=tk.CENTER)
            self.st2btn_red_shelves_sword[i].place(
                x=self.canvas_width/2-self.btn_shelves_pos[self.object.sword][i][0]+self.field_center_shift, y=self.btn_shelves_pos[self.object.sword][i][1], anchor=tk.CENTER)
            self.st2btn_blue_shelves_sword[i].place(
                x=self.canvas_width/2+self.btn_shelves_pos[self.object.sword][i][0]+self.field_center_shift, y=self.btn_shelves_pos[self.object.sword][i][1], anchor=tk.CENTER)

        # +,-ボタン設置
        place_warehouse_btn = [[370, 379], [870, 910]]  # +,-ボタンx,y
        place_warehouse_num = [[340, 349], [885]]  # 個数x,y
        for i in range(2):  # field_color
            self.warehouse_num_label[i].place(x=self.canvas_width/2+self.field_center_shift+pow(
                -1, i+1)*place_warehouse_num[0][i], y=place_warehouse_num[1][0], anchor=tk.CENTER)
            for j in range(2):  # kinds of btn
                self.btn_count_st2[i][j].place(
                    x=self.canvas_width/2+self.field_center_shift+pow(-1, i+1)*place_warehouse_btn[0][i], y=place_warehouse_btn[1][j], anchor=tk.CENTER)

    def hide_btns_field_setting_time2(self):
        for i in range(len(self.st2btn_red_shelves_sword)):
            self.st2btn_red_shelves_hat[i].place_forget()
            self.st2btn_blue_shelves_hat[i].place_forget()
            self.st2btn_red_shelves_sword[i].place_forget()
            self.st2btn_blue_shelves_sword[i].place_forget()
        for i in range(2):  # field_color
            self.warehouse_num_label[i].place_forget()
            for j in range(2):  # kinds of btn
                self.btn_count_st2[i][j].place_forget()

    def reset_btns_field_setting_time2(self):
        for color in range(2):
            self.warehouse_num[color] = 0
            self.warehouse_num_text[color].set(str(self.warehouse_num[color]))
        for i in range(len(self.st2btn_red_shelves_sword)):
            self.st2btn_red_shelves_hat[i]["bg"] = "#FFFFFF"
            self.state.shelves_setting_time2[i][self.field_color.red][self.object.hat] = False
            self.st2btn_blue_shelves_hat[i]["bg"] = "#FFFFFF"
            self.state.shelves_setting_time2[i][self.field_color.blue][self.object.hat] = False
            self.st2btn_red_shelves_sword[i]["bg"] = "#FFFFFF"
            self.state.shelves_setting_time2[i][self.field_color.red][self.object.sword] = False
            self.st2btn_blue_shelves_sword[i]["bg"] = "#FFFFFF"
            self.state.shelves_setting_time2[i][self.field_color.blue][self.object.sword] = False

    def st2btn_red_shelves_act(self, type, num):
        if type == self.object.hat:
            if self.state.shelves_setting_time2[num][self.field_color.red][type] == False:
                self.st2btn_red_shelves_hat[num]["bg"] = "#00FF00"
            else:
                self.st2btn_red_shelves_hat[num]["bg"] = "#FFFFFF"
        elif type == self.object.sword:
            if self.state.shelves_setting_time2[num][self.field_color.red][type] == False:
                self.st2btn_red_shelves_sword[num]["bg"] = "#00FF00"
            else:
                self.st2btn_red_shelves_sword[num]["bg"] = "#FFFFFF"

        self.state.shelves_setting_time2[num][self.field_color.red][
            type] = not self.state.shelves_setting_time2[num][self.field_color.red][type]

    def st2btn_blue_shelves_act(self, type, num):
        if type == self.object.hat:
            if self.state.shelves_setting_time2[num][self.field_color.blue][type] == False:
                self.st2btn_blue_shelves_hat[num]["bg"] = "#00FF00"
            else:
                self.st2btn_blue_shelves_hat[num]["bg"] = "#FFFFFF"
        elif type == self.object.sword:
            if self.state.shelves_setting_time2[num][self.field_color.blue][type] == False:
                self.st2btn_blue_shelves_sword[num]["bg"] = "#00FF00"
            else:
                self.st2btn_blue_shelves_sword[num]["bg"] = "#FFFFFF"

        self.state.shelves_setting_time2[num][self.field_color.blue][
            type] = not self.state.shelves_setting_time2[num][self.field_color.blue][type]

    def btn_count_st2_act(self, color, kind):
        self.warehouse_num[color] += kind
        if self.warehouse_num[color] < 0:
            self.warehouse_num[color] = 0
        elif self.warehouse_num[color] > 6:
            self.warehouse_num[color] = 6
        else:
            if self.field_color.red == color:
                color_str = "赤コート"
            else:
                color_str = "青コート"
            write_str = color_str+":\t倉庫\t"+str(kind)+"個追加"
            self.writeToLog(write_str)
        self.warehouse_num_text[color].set(
            str(self.warehouse_num[color]))

    def def_btns_field_sales_time(self):
        btn_sales_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=18, weight="bold")

        self.btn_sold_out = []
        btn_sold_out_width = 12
        self.btn_sold_out.append(tk.Button(
            self.master, text='完売\n達成', command=lambda: self.btn_sold_out_act(self.field_color.red), bg="#FFFFFF", font=btn_sales_font, width=btn_sold_out_width))
        self.btn_sold_out.append(tk.Button(
            self.master, text='完売\n達成', command=lambda: self.btn_sold_out_act(self.field_color.blue), bg="#FFFFFF", font=btn_sales_font, width=btn_sold_out_width))

        self.btn_count_sales = [[]for i in range(2)]
        btn_width = 1

        self.btn_count_sales[self.field_color.red].append(tk.Button(
            self.master, text="+", command=lambda: self.btn_count_sales_act(self.field_color.red, 1), bg="#FFFFFF", font=btn_sales_font, width=btn_width))
        self.btn_count_sales[self.field_color.red].append(tk.Button(
            self.master, text="-", command=lambda: self.btn_count_sales_act(self.field_color.red, -1), bg="#FFFFFF", font=btn_sales_font, width=btn_width))

        self.btn_count_sales[self.field_color.blue].append(tk.Button(
            self.master, text="+", command=lambda: self.btn_count_sales_act(self.field_color.blue, 1), bg="#FFFFFF", font=btn_sales_font, width=btn_width))
        self.btn_count_sales[self.field_color.blue].append(tk.Button(
            self.master, text="-", command=lambda: self.btn_count_sales_act(self.field_color.blue, -1), bg="#FFFFFF", font=btn_sales_font, width=btn_width))

        self.collection_room_num = [0, 0]
        self.collection_room_num_text = []
        self.collection_room_num_label = []
        for i in range(2):
            self.collection_room_num_text.append(tk.StringVar())
            self.collection_room_num_text[i].set(
                str(self.collection_room_num[i]))
            self.collection_room_num_label.append(tk.Label(self.master, textvariable=self.collection_room_num_text[i],
                                                           fg="#000000", bg="#FFFFFF", font=btn_sales_font, width=2))

        self.max_collection_room_num = [0, 0]

    def show_btns_field_sales_time(self):
        # 完売ボタン設置
        place_sold_out = [200, 700]  # x,y
        for i in range(2):
            self.btn_sold_out[i].place(
                x=self.canvas_width/2+self.field_center_shift+pow(-1, i+1)*place_sold_out[0], y=place_sold_out[1], anchor=tk.CENTER)

        # +,-ボタン設置
        place_collection_room_btn = [[43, 52], [630, 680]]  # +,-ボタンx,y
        place_collection_room_num = [[73, 82], [655]]  # 個数x,y
        for i in range(2):  # field_color
            self.collection_room_num_label[i].place(x=self.canvas_width/2+self.field_center_shift+pow(
                -1, i+1)*place_collection_room_num[0][i], y=place_collection_room_num[1][0], anchor=tk.CENTER)
            for j in range(2):  # kinds of btn
                self.btn_count_sales[i][j].place(
                    x=self.canvas_width/2+self.field_center_shift+pow(-1, i+1)*place_collection_room_btn[0][i], y=place_collection_room_btn[1][j], anchor=tk.CENTER)

        self.cal_max_collection_room_num()  # 最大値の計算

    def reset_btns_field_sales_time(self):
        self.timer_record_sales_time_str = ""
        for color in range(2):
            self.btn_sold_out[color]["bg"] = "#FFFFFF"
            self.collection_room_num[color] = 0
            self.collection_room_num_text[color].set(
                str(self.collection_room_num[color]))
            self.collection_room_num_label[color]['bg'] = "#FFFFFF"

    def cal_max_collection_room_num(self):
        for color in range(2):
            self.max_collection_room_num[color] = self.warehouse_num[color]
            for object_type in range(2):
                for num in range(7):
                    if self.state.shelves_setting_time2[num][color][object_type] == True:
                        self.max_collection_room_num[color] = + 1

    def hide_btns_field_sales_time(self):
        for i in range(2):  # field_color
            self.btn_sold_out[i].place_forget()
            self.collection_room_num_label[i].place_forget()
            for j in range(2):  # kinds of btn
                self.btn_count_sales[i][j].place_forget()

    def btn_sold_out_act(self, team):
        if team == self.field_color.red:
            if self.state.red_sold_out == False:
                self.timer_sold_out_time[self.field_color.red] = 90 - \
                    self.timer_sec

                if self.state_first_sold_out == self.field_color.NONE:
                    self.red_points += 50
                    self.state_first_sold_out = self.field_color.red
                    self.writeToLog("赤チーム：完売 先達成\t +50点")
                else:
                    self.red_points += 40
                    self.timer_record_sales_time_str = self.timer_record_sales_time_str+"\n赤チーム 完売達成 " + \
                        str(int((90-self.timer_sec)/60)).zfill(2) + \
                        ":"+str((90-self.timer_sec) % 60).zfill(2)
                    self.writeToLog("赤チーム：完売　達成\t +40点")
                self.btn_sold_out[team]["bg"] = "#00FF00"
                self.state.red_sold_out = True
            else:
                if self.state_first_sold_out == self.field_color.red:
                    self.red_points -= 50
                    self.writeToLog("赤チーム：完売　取り消し\t -50点")
                    if self.state.blue_sold_out == True:
                        self.state_first_sold_out = self.field_color.blue
                        self.blue_points += 10
                        self.writeToLog("青チーム：完売 先達成\t +10点")
                    else:
                        self.state_first_sold_out = self.field_color.NONE
                        self.timer_record_sales_time_str = ""
                else:
                    self.red_points -= 40
                    self.writeToLog("赤チーム：完売　取り消し\t -40点")
                    if self.state.blue_sold_out == False:
                        self.state_first_sold_out = self.field_color.NONE
                self.btn_sold_out[team]["bg"] = "#FFFFFF"
                self.state.red_sold_out = False
        elif team == self.field_color.blue:
            if self.state.blue_sold_out == False:
                self.timer_sold_out_time[self.field_color.blue] = 90 - \
                    self.timer_sec

                if self.state_first_sold_out == self.field_color.NONE:
                    self.blue_points += 50
                    self.state_first_sold_out = self.field_color.blue
                    self.timer_record_sales_time_str = "青チーム 完売達成 " + \
                        str(int((90-self.timer_sec)/60)).zfill(2) + \
                        ":"+str((90-self.timer_sec) % 60).zfill(2)
                    self.writeToLog("青チーム：完売 先達成\t +50点")
                else:
                    self.blue_points += 40
                    self.timer_record_sales_time_str = self.timer_record_sales_time_str+"\n青チーム 完売達成 " + \
                        str(int((90-self.timer_sec)/60)).zfill(2) + \
                        ":"+str((90-self.timer_sec) % 60).zfill(2)
                    self.writeToLog("青チーム：完売　達成\t +40点")
                self.btn_sold_out[team]["bg"] = "#00FF00"
                self.state.blue_sold_out = True
            else:
                if self.state_first_sold_out == self.field_color.blue:
                    self.blue_points -= 50
                    self.writeToLog("青チーム：完売　取り消し\t -50点")
                    if self.state.red_sold_out == True:
                        self.state_first_sold_out = self.field_color.red
                        self.red_points += 10
                        self.writeToLog("赤チーム：完売 先達成\t +10点")
                    else:
                        self.state_first_sold_out = self.field_color.NONE
                        self.timer_record_sales_time_str = ""
                else:
                    self.blue_points -= 40
                    self.writeToLog("青チーム：完売　取り消し\t -40点")
                    if self.state.red_sold_out == False:
                        self.state_first_sold_out = self.field_color.NONE
                self.btn_sold_out[team]["bg"] = "#FFFFFF"
                self.state.blue_sold_out = False

        self.update_points()
        self.update_record_txt_sold_out()

    def update_record_txt_sold_out(self):
        if self.state_first_sold_out == self.field_color.NONE:
            self.timer_record_sales_time_str = ""
        elif self.state_first_sold_out == self.field_color.red:
            self.timer_record_sales_time_str = "赤チーム 完売達成 " + str(int((self.timer_sold_out_time[self.field_color.red])/60)).zfill(
                2) + ":"+str((self.timer_sold_out_time[self.field_color.red]) % 60).zfill(2)
            if self.state.blue_sold_out == True:
                self.timer_record_sales_time_str += "\n青チーム 完売達成 " + str(int((self.timer_sold_out_time[self.field_color.blue])/60)).zfill(
                    2) + ":"+str((self.timer_sold_out_time[self.field_color.blue]) % 60).zfill(2)
        elif self.state_first_sold_out == self.field_color.blue:
            self.timer_record_sales_time_str = "青チーム 完売達成 " + str(int((self.timer_sold_out_time[self.field_color.blue])/60)).zfill(
                2) + ":"+str((self.timer_sold_out_time[self.field_color.blue]) % 60).zfill(2)
            if self.state.red_sold_out == True:
                self.timer_record_sales_time_str += "\n赤チーム 完売達成 " + str(int((self.timer_sold_out_time[self.field_color.red])/60)).zfill(
                    2) + ":"+str((self.timer_sold_out_time[self.field_color.red]) % 60).zfill(2)

        self.timer_record_txt.set(self.timer_record_sales_time_str)

    def btn_count_sales_act(self, color, kind):
        self.collection_room_num[color] += kind
        if self.collection_room_num[color] < 0:
            self.collection_room_num[color] = 0
        if self.collection_room_num[color] > self.max_collection_room_num[color]:
            self.collection_room_num[color] = self.max_collection_room_num[color]
        else:
            if color == self.field_color.red:
                self.red_points += (10*kind)
            else:
                self.blue_points += (10*kind)

        self.collection_room_num_text[color].set(
            str(self.collection_room_num[color]))
        if self.collection_room_num[color] == self.max_collection_room_num[color]:
            self.collection_room_num_label[color]['bg'] = "#00FF00"
        else:
            self.collection_room_num_label[color]['bg'] = "#FFFFFF"

        self.update_points()  # 得点更新

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
                self.writeToLog("試合進行：セッティングタイム1　が選択されました。")
                self.hide_btns_field_sales_time()
                self.hide_btns_field_setting_time2()
                self.show_btns_field_display_time()
            elif mode == self.time_mode.setting2:
                self.btn_setting_time2['bg'] = "#00FF00"
                self.writeToLog("試合進行：セッティングタイム2　が選択されました。")
                self.hide_btns_field_display_time()
                self.hide_btns_field_sales_time()
                self.show_btns_field_setting_time2()
            elif mode == self.time_mode.display_time:
                self.btn_display_time['bg'] = "#00FF00"
                self.writeToLog("試合進行：陳列タイム　が選択されました。")
                self.hide_btns_field_sales_time()
                self.hide_btns_field_setting_time2()
                self.show_btns_field_display_time()
            elif mode == self.time_mode.sales_time:
                self.btn_sales_time['bg'] = "#00FF00"
                self.writeToLog("試合進行：販売タイム　が選択されました。")
                self.hide_btns_field_setting_time2()
                self.hide_btns_field_display_time()
                self.show_btns_field_sales_time()

            self.state_time_mode = mode
            self.timer_reset()
            self.state_timer_mode = self.timer_mode.stop

    def setup_sales_time(self):
        self.hide_btns_field_display_time()

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
        if self.state_time_mode == self.time_mode.display_time:
            self.check_end_display_time()

    def check_end_display_time(self):
        if self.state_first_end_display_time == self.field_color.NONE:
            if self.red_toy_counters >= 6:
                self.state_first_end_display_time = self.field_color.red
                self.timer_record_display_time_str = "赤チーム 陳列タイム終了\n" + \
                    str(int((90-self.timer_sec)/60)).zfill(2) + \
                    ":"+str((90-self.timer_sec) % 60).zfill(2)
                self.writeToLog("赤チーム：陳列タイム　終了")
            if self.blue_toy_counters >= 6:
                self.state_first_end_display_time = self.field_color.blue
                self.timer_record_display_time_str = "青チーム 陳列タイム終了\n" + \
                    str(int((90-self.timer_sec)/60)).zfill(2) + \
                    ":"+str((90-self.timer_sec) % 60).zfill(2)
                self.writeToLog("青チーム：陳列タイム　終了")
        elif (self.state_first_end_display_time == self.field_color.red) and (self.red_toy_counters < 6):
            self.state_first_end_display_time = self.field_color.NONE
            self.timer_record_display_time_str = ""
            self.writeToLog("赤チーム：陳列タイム　取り消し")
        elif (self.state_first_end_display_time == self.field_color.blue) and (self.blue_toy_counters < 6):
            self.state_first_end_display_time = self.field_color.NONE
            self.timer_record_display_time_str = ""
            self.writeToLog("青チーム：陳列タイム　取り消し")

        self.timer_record_txt.set(self.timer_record_display_time_str)

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
            self.btn_red_toy_acquisition['bg'] = "#00FF00"
            self.writeToLog("赤チーム：おもちゃ取得\t+5点")
        else:
            self.red_points = self.red_points-5
            self.btn_red_toy_acquisition['bg'] = "#FFFFFF"
            self.writeToLog("赤チーム：おもちゃ取得取り消し\t-5点")
        self.update_points()
        self.state.red_toy_acquisition = not self.state.red_toy_acquisition

    def btn_blue_toy_acquisition_act(self):
        if self.state.blue_toy_acquisition == False:
            self.blue_points += 5
            self.btn_blue_toy_acquisition['bg'] = "#00FF00"
            self.writeToLog("青チーム：おもちゃ取得\t+5点")
        else:
            self.blue_points -= 5
            self.btn_blue_toy_acquisition['bg'] = "#FFFFFF"
            self.writeToLog("青チーム：おもちゃ取得取り消し\t-5点")
        self.update_points()
        self.state.blue_toy_acquisition = not self.state.blue_toy_acquisition

    def btn_red_byshelves_act(self, type, id):
        if self.position_state_red["back_yard"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_red_shelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_red["back_yard"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points+10
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：バックヤード\tハット　配置\t+10点")
                else:
                    self.red_points = self.red_points+5
                    self.writeToLog("赤チーム：バックヤード\tハット　配置\t+5点")
            else:
                self.btn_red_shelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_red["back_yard"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points+5
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：バックヤード\t剣　配置\t+5点")
                else:
                    self.writeToLog("赤チーム：バックヤード\t剣　配置")
            self.position_state_red["back_yard"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_red_shelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_red["back_yard"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points-10
                    self.writeToLog("赤チーム：バックヤード\tハット　配置取り消し\t-10点")
                    self.red_toy_counters -= 1
                else:
                    self.red_points = self.red_points-5
                    self.writeToLog("赤チーム：バックヤード\tハット　配置取り消し\t-5点")
            else:
                self.btn_red_shelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_red["back_yard"]["shelves"]["hat"][id] == False:
                    self.red_points = self.red_points-5
                    self.red_toy_counters -= 1
                    self.writeToLog("赤チーム：バックヤード\t剣　配置取り消し\t-5点")
                else:
                    self.writeToLog("赤チーム：バックヤード\t剣　配置取り消し")
            self.position_state_red["back_yard"]["shelves"][type][id] = False
        self.update_points()

    def btn_blue_byshelves_act(self, type, id):
        if self.position_state_blue["back_yard"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_blue_shelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_blue["back_yard"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points+10
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：バックヤード\tハット　配置\t+10点")
                else:
                    self.blue_points = self.blue_points+5
                    self.writeToLog("青チーム：バックヤード\tハット　配置\t+5点")
            else:
                self.btn_blue_shelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+5
                    self.blue_toy_counters += 1
                    self.writeToLog("青チーム：バックヤード\t剣　配置\t+5点")
                else:
                    self.writeToLog("青チーム：バックヤード\t剣　配置")
            self.position_state_blue["back_yard"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_shelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-10
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：バックヤード\tハット　配置取り消し\t-10点")
                else:
                    self.blue_points = self.blue_points-5
                    self.writeToLog("青チーム：バックヤード\tハット　配置取り消し\t-5点")
            else:
                self.btn_blue_shelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-5
                    self.blue_toy_counters -= 1
                    self.writeToLog("青チーム：バックヤード\t剣　配置取り消し\t-5点")
                else:
                    self.writeToLog("青チーム：バックヤード\t剣　配置取り消し")
            self.position_state_blue["back_yard"]["shelves"][type][id] = False
        self.update_points()

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
            self.position_state_red["sales_floor"]["shelves"][type][id] = False
        self.update_points()

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
            self.position_state_blue["sales_floor"]["shelves"][type][id] = False
        self.update_points()

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
            self.position_state_red["showcase"]["shelves"][type][id] = False
        self.update_points()

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
            self.position_state_blue["showcase"]["shelves"][type][id] = False
        self.update_points()

    def btn_reset(self):
        self.red_points = 0
        self.blue_points = 0
        self.red_toy_counters = 0
        self.blue_toy_counters = 0

        # 試合進行系のボタンリセット
        self.set_mode_timer(self.time_mode.NONE)

        self.reset_btns_field_display_time()
        self.reset_btns_field_setting_time2()
        self.reset_btns_field_sales_time()

        self.hide_btns_field_display_time()  # フィールド上のボタンを非表示
        self.hide_btns_field_sales_time()
        self.hide_btns_field_setting_time2()

        self.update_points()
        self.writeToLog("リセットしました")


if __name__ == "__main__":
    app = Application()
