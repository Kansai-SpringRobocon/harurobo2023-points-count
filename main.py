import tkinter as tk
import tkinter.font as tk_font
from PIL import ImageTk
import json


class Application(tk.Frame):
    red_points = 0
    blue_points = 0

    state_red_toy_acquisition = False
    state_blue_toy_acquisition = False
    state_red_sword_byshelves_1 = False
#    shelves = {"back_yard", "sales_floor", "showcase"}
#    shelves["back_yard"] = {}
    position_state_red = {}
    position_state_blue = {}
    with open("setting_red.json", mode="r") as f_red:
        position_state_red = json.load(f_red)
    with open("setting_red.json", mode="r") as f_blue:
        position_state_blue = json.load(f_blue)

    def __init__(self):
        self.master = tk.Tk()

        self.master.title("画像の表示")       # ウィンドウタイトル
        self.master.geometry("1920x1080")     # ウィンドウサイズ(幅x高さ)
        self.master.attributes('-fullscreen', True)

        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        # Canvasを配置
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        self.photo_image = ImageTk.PhotoImage(file="field.png")

        # キャンバスのサイズを取得
        self.master.update()  # Canvasのサイズを取得するため更新しておく
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像の描画
        self.canvas.create_image(
            canvas_width / 2,       # 画像表示位置(Canvasの中心)
            canvas_height * 0.6,
            image=self.photo_image,  # 表示画像データ
        )

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

        btn_toy_acquisition_pos = 70
        btn_toy_acquisition_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=14, weight="bold")
        self.btn_red_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_red_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_red_toy_acquisition.place(
            x=canvas_width/2-btn_toy_acquisition_pos, y=canvas_height*0.68, anchor=tk.CENTER)
        self.btn_blue_toy_acquisition = tk.Button(
            self.master, text='ワーク\n取得', command=self.btn_blue_toy_acquisition_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_blue_toy_acquisition.place(
            x=canvas_width/2+btn_toy_acquisition_pos, y=canvas_height*0.68, anchor=tk.CENTER)

        btn_byshelves_0_pos = 40
        self.btn_red_byshelves_hat_0 = tk.Button(
            self.master, text='ハット', command=lambda: self.btn_red_byshelves_hat_act("hat", 0), bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_red_byshelves_hat_0.place(
            x=canvas_width/2-btn_byshelves_0_pos, y=canvas_height*0.9, anchor=tk.CENTER)

        self.btn_red_byshelves_sword_0 = tk.Button(
            self.master, text='剣', command=self.btn_red_sword_byshelves_1_act, bg="#FFFFFF", font=btn_toy_acquisition_font)
        self.btn_red_byshelves_sword_0.place(
            x=canvas_width/2-btn_byshelves_0_pos, y=canvas_height*0.95, anchor=tk.CENTER)


#  print(len(self.btn_red_hat_byshelves))

        self.master.mainloop()

    # 得点更新
    def update_points(self):
        self.red_points_text.set(str(self.red_points))
        self.blue_points_text.set(str(self.blue_points))

    # ウィンドウクローズ
    def btn_close(self):
        self.master.destroy()

    def btn_red_toy_acquisition_act(self):
        if self.state_red_toy_acquisition == False:
            self.red_points = self.red_points+5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#00FF00"
            self.state_red_toy_acquisition = True
        else:
            self.red_points = self.red_points-5
            self.update_points()
            self.btn_red_toy_acquisition['bg'] = "#FFFFFF"
            self.state_red_toy_acquisition = False

    def btn_blue_toy_acquisition_act(self):
        if self.state_blue_toy_acquisition == False:
            self.blue_points = self.blue_points+5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#00FF00"
            self.state_blue_toy_acquisition = True
        else:
            self.blue_points = self.blue_points-5
            self.update_points()
            self.btn_blue_toy_acquisition['bg'] = "#FFFFFF"
            self.state_blue_toy_acquisition = False

    def btn_red_byshelves_hat_act(self, type, id):
        if self.position_state_red["back_yard"]["shelves"][type][id] == False:
            self.red_points = self.red_points+10
            self.update_points()
            self.btn_red_byshelves_hat_0['bg'] = "#00FF00"
            self.position_state_red["back_yard"]["shelves"][type][id] = True
        else:
            self.red_points = self.red_points-10
            self.update_points()
            self.btn_red_byshelves_hat_0['bg'] = "#FFFFFF"
            self.position_state_red["back_yard"]["shelves"][type][id] = False

    def btn_red_sword_byshelves_1_act(self):
        if self.state_red_sword_byshelves_1 == False:
            self.red_points = self.red_points+10
            self.update_points()
            self.btn_red_sword_byshelves_1['bg'] = "#00FF00"
            self.state_red_sword_byshelves_1 = True
        else:
            self.red_points = self.red_points-10
            self.update_points()
            self.btn_red_sword_byshelves_1['bg'] = "#FFFFFF"
            self.state_red_sword_byshelves_1 = False

    def btn_test(self):
        self.red_points = self.red_points+1
        self.update_points()
        print(self.red_points)

    def btn_reset(self):
        self.red_points = 0
        self.blue_points = 0
        for i in range(len(self.position_state_red["back_yard"]["shelves"]["hat"])):
            self.position_state_red["back_yard"]["shelves"]["hat"][i] = False
        self.update_points()


if __name__ == "__main__":
    app = Application()
