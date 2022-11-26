import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk

root = tk.Tk()
root.title("Timer")
text_sec = tk.StringVar()
text_sec.set("0")
my_font = font.Font(size=20)

text_min = tk.StringVar()
text_min.set("30")

buff_min = tk.StringVar()
buff_min.set("0")

buff_sec = tk.StringVar()
buff_sec.set("0")

text_start_stop = tk.StringVar()
text_start_stop.set("START")

progressbar = ttk.Progressbar(
    root, orient="horizontal", length=230, mode="determinate")
progressbar.grid(row=2, column=0, columnspan=7)

start = True
check = True
stop = False


def start():
    global start, check, text_min, text_sec, start, check, stop, value_time
    start = False
    if check == True and stop == True:
        start = True
        text_start_stop.set("STOP")
        timer()

    elif check == False and stop == True:
        count_min = int(buff_min.get())
        count_sec = int(buff_sec.get())
        buff_min.set("0")
        buff_sec.set("0")
        buff_min.set(count_min)
        buff_sec.set(count_sec)
        check = True
        text_start_stop.set("START")

    else:
        start = True
        stop = True
        text_start_stop.set("STOP")
        buff_min.set(int(text_min.get()))
        buff_sec.set(int(text_sec.get()))
        maximum_time = int(buff_min.get())*60+int(buff_sec.get())
        # print(maximum_time)
        value_time = 0
        div_time = 1
        progressbar.configure(maximum=maximum_time, value=value_time)
        timer()


def timer():
    global start, buff_min, buff_sec, text_min, text_sec, check, value_time, div_time
    if start == True:
        if int(buff_min.get()) == 0 and int(buff_sec.get()) == 0:
            pass
        else:
            check = False
            time_min = int(buff_min.get())
            time_sec = int(buff_sec.get())
            if time_min >= 0:
                time_sec -= 1
                buff_sec.set(str(time_sec))
                value_time += 1
                progressbar.configure(value=value_time)
                root.after(1000, timer)
                if time_sec == -1:
                    time_min -= 1
                    buff_min.set(str(time_min))
                    buff_sec.set("59")
            if int(buff_min.get()) == 0 and int(buff_sec.get()) == 0:
                start = False
                time_min = 0
                time_sec = 0
                buff_sec.set(str(time_sec))
                buff_min.set(str(time_min))


def stop():
    global start, check, stop
    start = True
    check = True
    stop = False
    time_min = 0
    time_sec = 0
    buff_sec.set(str(time_sec))
    buff_min.set(str(time_min))


labbel = tk.Label(root, text="設定")
labbel.grid(row=0, column=0, columnspan=1)

entry = tk.Entry(root, width=2, font=my_font, textvariable=text_min)
entry.grid(row=0, column=1)

label_min = tk.Label(root, text=u"分")
label_min.grid(row=0, column=2)

entry1 = tk.Entry(root, width=2, font=my_font, textvariable=text_sec)
entry1.grid(row=0, column=3)

label_sec = tk.Label(root, text=u"秒")
label_sec.grid(row=0, column=4)

button = tk.Button(root, textvariable=text_start_stop, command=start)
button.grid(row=0, column=5)

button = tk.Button(root, text=u"RESET", command=stop)
button.grid(row=0, column=6)

labbel = tk.Label(root, text="タイマー")
labbel.grid(row=1, column=0, columnspan=1)

labbel = tk.Label(root, font=my_font, textvariable=buff_min)
labbel.grid(row=1, column=1, columnspan=1)

labbel = tk.Label(root, text="分")
labbel.grid(row=1, column=2, columnspan=1)

labbel = tk.Label(root, font=my_font, textvariable=buff_sec)
labbel.grid(row=1, column=3, columnspan=1)

labbel = tk.Label(root, text="秒")
labbel.grid(row=1, column=4, columnspan=1)

root.mainloop()
