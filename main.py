import tkinter as tk
import tkinter.font as tk_font
from PIL import ImageTk

red_points = 0
blue_points = 0


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.title("画像の表示")       # ウィンドウタイトル
        self.master.geometry("720x520")     # ウィンドウサイズ(幅x高さ)
        self.master.attributes('-fullscreen', True)

        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        # Canvasを配置
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
        self.photo_image = ImageTk.PhotoImage(file="field.png")

        # キャンバスのサイズを取得
        self.update()  # Canvasのサイズを取得するため更新しておく
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像の描画
        self.canvas.create_image(
            canvas_width / 2,       # 画像表示位置(Canvasの中心)
            canvas_height * 0.6,
            image=self.photo_image,  # 表示画像データ
        )

        self.canvas.create_rectangle(
            canvas_width/4, 0, canvas_width/2, canvas_height/7, fill='red')
        self.canvas.create_rectangle(
            canvas_width/2, 0, canvas_width/2+canvas_width/4, canvas_height/7, fill='blue')

        # ボタン作成
        btn_rst_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=15, weight="bold")
        btn_rst = tk.Button(self.master, text='リセット', command=btn_reset, height=int(
            canvas_height/1000), width=int(canvas_width/148), font=btn_rst_font, relief=tk.RAISED, bd=5)
        btn_rst.place(x=canvas_width*0.905, y=canvas_height*0.8)

        btn_close_font = tk_font.Font(
            self.master, family="HGPゴシックE", size=20, weight="bold")
        btn_close = tk.Button(self.master, text='閉じる', command=self.btn_close, height=int(
            canvas_height/1000), width=int(canvas_width/200), bg='#FF0000', fg='#FFFFFF', font=btn_close_font)
        btn_close.place(x=canvas_width*0.905, y=canvas_height*0.9)

        chk = tk.Checkbutton(self.master, text='Pythonを使用する')
        chk.place(x=50, y=70)

    def btn_close(self):
        self.master.destroy()

# ボタンのクリックイベント


def btn_reset():
    print('リセット')


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
