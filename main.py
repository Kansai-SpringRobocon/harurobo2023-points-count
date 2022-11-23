import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk
from PIL import ImageTk
import json
import datetime


class Application(tk.Frame):
    red_points = 0
    blue_points = 0

    red_toy_counters = 0
    blue_toy_counters = 0

    state_red_toy_acquisition = False
    state_blue_toy_acquisition = False

    red_team_name = "チーム名を選択してください"
    blue_team_name = "チーム名を選択してください"

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
        self.master.geometry("1920x1080")     # ウィンドウサイズ(幅x高さ)
        self.master.attributes('-fullscreen', True)
        self.master.iconbitmap(default='harurobo.ico')

        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        # Canvasを配置
        self.canvas.pack(expand=True, fill=tk.BOTH)

        app_name_label = tk.Label(self.master, text="春ロボコン2023\n得点計算ツール",
                                  fg="#000000", font=("HGPゴシックE", 18, "bold"))
        app_name_label.place(x=20, y=20)

        # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        self.photo_image = ImageTk.PhotoImage(file="field.png")

        # キャンバスのサイズを取得
        self.master.update()  # Canvasのサイズを取得するため更新しておく
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像の描画
        self.canvas.create_image(
            canvas_width / 2,       # 画像表示位置(Canvasの中心)
            canvas_height * 0.58,
            image=self.photo_image,  # 表示画像データ
        )

        self.log = tk.Text(self.master, state='disabled', borderwidth=5,
                           width=180, height=5, wrap='none',)
        ys = ttk.Scrollbar(self.master, orient='vertical',
                           command=self.log.yview)
        self.log['yscrollcommand'] = ys.set
        self.log.insert('end', "Lorem ipsum...\n...\n...")
        self.log.place(x=20, y=canvas_height*0.91)

        points_width = canvas_width/4
        points_height = canvas_height/6
        self.canvas.create_rectangle(
            points_width, 0, canvas_width/2, points_height, fill='red')
        self.canvas.create_rectangle(
            canvas_width/2, 0, canvas_width/2+points_width, points_height, fill='blue')

        red_label = tk.Label(self.master, text="赤コート",
                             fg="#FFFFFF", bg="#FF0000", font=("HGPゴシックE", 30, "bold"))
        blue_label = tk.Label(self.master, text="青コート",
                              fg="#FFFFFF", bg="#0000FF", font=("HGPゴシックE", 30, "bold"))
        red_label.place(x=int(canvas_width/2-points_width/2),
                        y=40, anchor=tk.CENTER)
        blue_label.place(x=int(canvas_width/2+points_width/2),
                         y=40, anchor=tk.CENTER)

        self.red_points_text = tk.StringVar()
        self.red_points_text.set(str(self.red_points))

        self.blue_points_text = tk.StringVar()
        self.blue_points_text.set(str(self.blue_points))

        red_points_label = tk.Label(self.master, textvariable=self.red_points_text,
                                    fg="#FFFFFF", bg="#FF0000", font=("HGPゴシックE", 42, "bold"))
        blue_points_label = tk.Label(self.master, textvariable=self.blue_points_text,
                                     fg="#FFFFFF", bg="#0000FF", font=("HGPゴシックE", 42, "bold"))
        red_points_label.place(x=int(canvas_width/2-points_width/2),
                               y=100, anchor=tk.CENTER)
        blue_points_label.place(x=int(canvas_width/2+points_width/2),
                                y=100, anchor=tk.CENTER)

        self.red_team_text = tk.StringVar()
        self.red_team_text.set(str(self.red_team_name))

        self.blue_team_text = tk.StringVar()
        self.blue_team_text.set(str(self.blue_team_name))
        red_team_name_label = tk.Label(self.master, textvariable=self.red_team_text,
                                       fg="#FFFFFF", bg="#FF0000", font=("HGPゴシックE", 20, "bold"))
        blue_team_name_label = tk.Label(self.master, textvariable=self.blue_team_text,
                                        fg="#FFFFFF", bg="#0000FF", font=("HGPゴシックE", 20, "bold"))
        red_team_name_label.place(x=int(canvas_width/2-points_width/2),
                                  y=150, anchor=tk.CENTER)
        blue_team_name_label.place(x=int(canvas_width/2+points_width/2),
                                   y=150, anchor=tk.CENTER)

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
            self.master, textvariable=red_team_val, value=self.team_list["team_name"], font=combobox_font, width=20)
        self.blue_team = tk.ttk.Combobox(
            self.master, textvariable=blue_team_val, value=self.team_list["team_name"], font=combobox_font, width=20)
        self.red_team.bind('<<ComboboxSelected>>',
                           self.update_team_name)
        self.blue_team.bind('<<ComboboxSelected>>',
                            self.update_team_name)

        red_team_label.place(x=20, y=90)
        blue_team_label.place(x=20, y=130)
        self.red_team.place(x=120, y=90)
        self.blue_team.place(x=120, y=130)

        # ボタン作成
        btn_rst_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=15, weight="bold")
        btn_rst = tk.Button(self.master, text='リセット', command=self.btn_reset, height=int(
            canvas_height/1000), width=int(canvas_width/148), font=btn_rst_font, relief=tk.RAISED, bd=5)
        btn_rst.place(x=canvas_width*0.905, y=canvas_height*0.8)

        btn_close_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=20, weight="bold")
        btn_close = tk.Button(self.master, text='閉じる', command=self.btn_close, height=int(
            canvas_height/1000), width=int(canvas_width/200), bg='#FF0000', fg='#FFFFFF', font=btn_close_font)
        btn_close.place(x=canvas_width*0.905, y=canvas_height*0.9)

        btn_test = tk.Button(self.master, text='test', command=self.btn_test, height=int(
            canvas_height/1000), width=int(canvas_width/148), font=btn_rst_font, relief=tk.RAISED, bd=5)
        btn_test.place(x=canvas_width*0.905, y=canvas_height*0.5)

        self.setup_btns(canvas_width, canvas_height)

#  print(len(self.btn_red_hat_byshelves))

        self.master.mainloop()

    def setup_btns(self, canvas_width, canvas_height):

        btn_toy_acquisition_pos = 70
        btn_toy_acquisition_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=14, weight="bold")
        self.btn_red_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_red_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_red_toy_acquisition.place(
            x=canvas_width/2-btn_toy_acquisition_pos, y=canvas_height*0.63, anchor=tk.CENTER)
        self.btn_blue_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_blue_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_blue_toy_acquisition.place(
            x=canvas_width/2+btn_toy_acquisition_pos, y=canvas_height*0.63, anchor=tk.CENTER)

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

        btn_byshelves_0_pos = 70
        self.btn_red_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_byshelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_hat[0].place(
            x=canvas_width/2-btn_byshelves_0_pos, y=canvas_height*0.825, anchor=tk.CENTER)

        self.btn_red_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_byshelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_sword[0].place(
            x=canvas_width/2-btn_byshelves_0_pos, y=canvas_height*0.89, anchor=tk.CENTER)

        self.btn_blue_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_byshelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_hat[0].place(
            x=canvas_width/2+btn_byshelves_0_pos, y=canvas_height*0.825, anchor=tk.CENTER)

        self.btn_blue_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_byshelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_sword[0].place(
            x=canvas_width/2+btn_byshelves_0_pos, y=canvas_height*0.89, anchor=tk.CENTER)

        btn_byshelves_1_pos = 400
        self.btn_red_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_byshelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_hat[1].place(
            x=canvas_width/2-btn_byshelves_1_pos, y=canvas_height*0.685, anchor=tk.CENTER)

        btn_byshelves_2_pos = 300
        self.btn_red_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_byshelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_sword[1].place(
            x=canvas_width/2-btn_byshelves_2_pos, y=canvas_height*0.685, anchor=tk.CENTER)

        self.btn_blue_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_byshelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_hat[1].place(
            x=canvas_width/2+btn_byshelves_1_pos, y=canvas_height*0.685, anchor=tk.CENTER)

        self.btn_blue_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_byshelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_sword[1].place(
            x=canvas_width/2+btn_byshelves_2_pos, y=canvas_height*0.685, anchor=tk.CENTER)

        self.btn_red_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_byshelves_act("hat", 2), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_hat[2].place(
            x=canvas_width/2-btn_byshelves_1_pos, y=canvas_height*0.6, anchor=tk.CENTER)

        self.btn_red_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_byshelves_act("sword", 2), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_sword[2].place(
            x=canvas_width/2-btn_byshelves_2_pos, y=canvas_height*0.6, anchor=tk.CENTER)

        self.btn_blue_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_byshelves_act("hat", 2), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_hat[2].place(
            x=canvas_width/2+btn_byshelves_1_pos, y=canvas_height*0.6, anchor=tk.CENTER)

        self.btn_blue_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_byshelves_act("sword", 2), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_sword[2].place(
            x=canvas_width/2+btn_byshelves_2_pos, y=canvas_height*0.6, anchor=tk.CENTER)

        self.btn_red_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_byshelves_act("hat", 3), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_hat[3].place(
            x=canvas_width/2-btn_byshelves_1_pos, y=canvas_height*0.515, anchor=tk.CENTER)

        self.btn_red_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_byshelves_act("sword", 3), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_byshelves_sword[3].place(
            x=canvas_width/2-btn_byshelves_2_pos, y=canvas_height*0.515, anchor=tk.CENTER)

        self.btn_blue_byshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_byshelves_act("hat", 3), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_hat[3].place(
            x=canvas_width/2+btn_byshelves_1_pos, y=canvas_height*0.515, anchor=tk.CENTER)

        self.btn_blue_byshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_byshelves_act("sword", 3), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_byshelves_sword[3].place(
            x=canvas_width/2+btn_byshelves_2_pos, y=canvas_height*0.515, anchor=tk.CENTER)

        btn_sashelves_0_pos = 350
        self.btn_red_sashelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_sashelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_sashelves_hat[0].place(
            x=canvas_width/2-btn_sashelves_0_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_1_pos = 260
        self.btn_red_sashelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_sashelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_sashelves_sword[0].place(
            x=canvas_width/2-btn_sashelves_1_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        self.btn_blue_sashelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_sashelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_sashelves_hat[0].place(
            x=canvas_width/2+btn_sashelves_0_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        self.btn_blue_sashelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_sashelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_sashelves_sword[0].place(
            x=canvas_width/2+btn_sashelves_1_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_2_pos = 170
        self.btn_red_sashelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_sashelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_sashelves_hat[1].place(
            x=canvas_width/2-btn_sashelves_2_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        btn_sashelves_3_pos = 80
        self.btn_red_sashelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_sashelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_sashelves_sword[1].place(
            x=canvas_width/2-btn_sashelves_3_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        self.btn_blue_sashelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_sashelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_sashelves_hat[1].place(
            x=canvas_width/2+btn_sashelves_2_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        self.btn_blue_sashelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_sashelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_sashelves_sword[1].place(
            x=canvas_width/2+btn_sashelves_3_pos, y=canvas_height*0.405, anchor=tk.CENTER)

        btn_shshelves_0_pos = 400
        self.btn_red_shshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_shshelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_shshelves_hat[0].place(
            x=canvas_width/2-btn_shshelves_0_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_1_pos = 300
        self.btn_red_shshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_shshelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_shshelves_sword[0].place(
            x=canvas_width/2-btn_shshelves_1_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        self.btn_blue_shshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_shshelves_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_shshelves_hat[0].place(
            x=canvas_width/2+btn_shshelves_0_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        self.btn_blue_shshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_shshelves_act("sword", 0), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_shshelves_sword[0].place(
            x=canvas_width/2+btn_shshelves_1_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_2_pos = 120
        self.btn_red_shshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_shshelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_shshelves_hat[1].place(
            x=canvas_width/2-btn_shshelves_2_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        btn_shshelves_3_pos = 40
        self.btn_red_shshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_red_shshelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_red_shshelves_sword[1].place(
            x=canvas_width/2-btn_shshelves_3_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        self.btn_blue_shshelves_hat.append(tk.Button(
            self.master, text='ハット', command=lambda: self.btn_blue_shshelves_act("hat", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_shshelves_hat[1].place(
            x=canvas_width/2+btn_shshelves_2_pos, y=canvas_height*0.26, anchor=tk.CENTER)

        self.btn_blue_shshelves_sword.append(tk.Button(
            self.master, text='剣', command=lambda: self.btn_blue_shshelves_act("sword", 1), bg="#FFFFFF", font=btn_toy_acquisition_font))
        self.btn_blue_shshelves_sword[1].place(
            x=canvas_width/2+btn_shshelves_3_pos, y=canvas_height*0.26, anchor=tk.CENTER)

    def writeToLog(self, msg):
        numlines = int(self.log.index('end - 1 line').split('.')[0])
        self.log['state'] = 'normal'
        # if numlines==24:
        # #log.delete(1.0, 2.0)
        if self.log.index('end-1c') != '1.0':
            self.log.insert('1.0', '\n')
        self.log.insert('1.0', str(datetime.datetime.now()
                                   ) + "\t" + msg)
        self.log['state'] = 'disabled'

    # 得点更新
    def update_points(self):
        self.red_points_text.set(str(self.red_points))
        self.blue_points_text.set(str(self.blue_points))
        if self.red_toy_counters >= 6:
            print("陳列タイム終了")
        if self.blue_toy_counters >= 6:
            print("陳列タイム終了")

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
        if self.state_red_toy_acquisition == False:
            self.red_points = self.red_points+5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#00FF00"
            self.state_red_toy_acquisition = True
            self.writeToLog("赤チーム：おもちゃ取得\t+5点")
        else:
            self.red_points = self.red_points-5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#FFFFFF"
            self.state_red_toy_acquisition = False
            self.writeToLog("赤チーム：おもちゃ取得取り消し\t-5点")

    def btn_blue_toy_acquisition_act(self):
        if self.state_blue_toy_acquisition == False:
            self.blue_points = self.blue_points+5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#00FF00"
            self.state_blue_toy_acquisition = True
            self.writeToLog("青チーム：おもちゃ取得\t+5点")
        else:
            self.blue_points = self.blue_points-5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#FFFFFF"
            self.state_blue_toy_acquisition = False
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
                else:
                    self.blue_points = self.blue_points+5
            else:
                self.btn_blue_byshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+5
                    self.blue_toy_counters += 1
            self.update_points()
            self.position_state_blue["back_yard"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_byshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-10
                    self.blue_toy_counters -= 1
                else:
                    self.blue_points = self.blue_points-5
            else:
                self.btn_blue_byshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["back_yard"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-5
                    self.blue_toy_counters -= 1
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
                else:
                    self.blue_points = self.blue_points+5
            else:
                self.btn_blue_sashelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["sales_floor"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+15
                    self.blue_toy_counters += 1
            self.update_points()
            self.position_state_blue["sales_floor"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_sashelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["sales_floor"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-20
                    self.blue_toy_counters -= 1
                else:
                    self.blue_points = self.blue_points-5
            else:
                self.btn_blue_sashelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["sales_floor"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-15
                    self.blue_toy_counters -= 1
            self.update_points()
            self.position_state_blue["sales_floor"]["shelves"][type][id] = False

    def btn_red_shshelves_act(self, type, id):
        if self.position_state_red["showcase"]["shelves"][type][id] == False:
            if type == "hat":
                self.btn_red_shshelves_hat[id]['bg'] = "#00FF00"
                if self.position_state_red["showcase"]["shelves"]["sword"][id] == False:
                    self.red_points = self.red_points+35
                    self.red_toy_counters += 1
                    self.writeToLog("赤チーム：ショーケース\tハット　配置\t+35点")
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
                    self.blue_points = self.blue_points+35
                    self.blue_toy_counters += 1
                else:
                    self.blue_points = self.blue_points+5
            else:
                self.btn_blue_shshelves_sword[id]['bg'] = "#00FF00"
                if self.position_state_blue["showcase"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points+25
                    self.blue_toy_counters += 1
            self.update_points()
            self.position_state_blue["showcase"]["shelves"][type][id] = True
        else:
            if type == "hat":
                self.btn_blue_shshelves_hat[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["showcase"]["shelves"]["sword"][id] == False:
                    self.blue_points = self.blue_points-30
                    self.blue_toy_counters -= 1
                else:
                    self.blue_points = self.blue_points-5
            else:
                self.btn_blue_shshelves_sword[id]['bg'] = "#FFFFFF"
                if self.position_state_blue["showcase"]["shelves"]["hat"][id] == False:
                    self.blue_points = self.blue_points-25
                    self.blue_toy_counters -= 1
            self.update_points()
            self.position_state_blue["showcase"]["shelves"][type][id] = False

    def btn_test(self):
        self.red_points = self.red_points+1
        self.update_points()
        print(self.red_points)

    def btn_reset(self):
        self.red_points = 0
        self.blue_points = 0
        self.red_toy_counters = 0
        self.blue_toy_counters = 0

        # TODO:ワーク取得時のリセットをつける
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
