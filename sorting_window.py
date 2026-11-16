import tkinter as tk

window = tk.Tk()
window.title("汁e泽^机器人")
window.geometry("640x520")

label = tk.Label(window, text="你好，我是小分机器人！")
label.pack()



# ---------- 1. 创建窗口 ----------
window = tk.Tk()
window.title("小分机器人 · 颜色分拣")
window.geometry("640x520")
window.resizable(False, False)

# ---------- 2. 保存任务数据 ----------
capacity = 3
total = 0
busy = False

# 字典：把每种颜色与对应信息放在一起
counts = {"红色": 0, "蓝色": 0, "黄色": 0}
boxes = {"红色": "A箱", "蓝色": "B箱", "黄色": "C箱"}
colors = {"红色": "#ef7070", "蓝色": "#67a7ef", "黄色": "#f3c95b"}
positions = {"红色": 120, "蓝色": 320, "黄色": 520}

# 保存画布上三个数量标签的编号
count_labels = {}


# ---------- 3. 定义程序功能 ----------
def refresh_counts():
    """刷新三个箱子的数量和累计成绩。"""
    for color in counts:
        text = f"{boxes[color]}：{counts[color]}/{capacity}"
        canvas.itemconfig(count_labels[color], text=text)

    total_label.config(text=f"累计成功分拣：{total} 件")


def set_buttons(state):
    """动画期间禁用按钮，防止任务互相干扰。"""
    for button in color_buttons:
        button.config(state=state)

    clear_button.config(state=state)


def start_sort(color):
    """点击颜色按钮时，开始一次分拣。"""
    global busy

    if busy:
        return

    if counts[color] >= capacity:
        status.config(text=f"[判断] {boxes[color]}已满，请先清空箱子。")
        return

    busy = True
    set_buttons("disabled")

    # 在画布上方生成一个彩色物体
    item = canvas.create_oval(
        305, 45, 335, 75,
        fill=colors[color],
        outline="#333333",
        width=2
    )

    status.config(text=f"[检测] 发现一个{color}物体。")

    # 等待600毫秒，再进行判断
    window.after(600, judge, color, item)


def judge(color, item):
    """显示判断结果，然后开始移动。"""
    status.config(text=f"[判断] {color}物体应放入{boxes[color]}。")
    window.after(600, move_item, color, item, 0)


def move_item(color, item, step):
    """每次移动一点，连续刷新形成动画。"""
    global total, busy

    if step < 30:
        status.config(text=f"[执行] 正在搬运到{boxes[color]}……")

        # 从起点到目标位置，分成30次移动
        dx = (positions[color] - 320) / 30
        dy = 190 / 30

        canvas.move(item, dx, dy)
        window.after(30, move_item, color, item, step + 1)

    else:
        # 移动完成，删除搬运中的物体
        canvas.delete(item)

        # 在箱子里画一个小圆，表示已装入的物体
        x = positions[color] - 40 + counts[color] * 40
        canvas.create_oval(
            x - 12, 240, x + 12, 264,
            fill=colors[color],
            outline="#333333",
            tags="stored"
        )

        counts[color] += 1
        total += 1
        refresh_counts()

        message = f"[完成] 已放入{boxes[color]}！可以继续添加物体。"
        if total == 5:
            message += " 今日5件目标达成！"

        status.config(text=message)

        busy = False
        set_buttons("normal")


def clear_boxes():
    """清空箱内物体，保留累计分拣成绩。"""
    if busy:
        return

    for color in counts:
        counts[color] = 0

    canvas.delete("stored")
    refresh_counts()
    status.config(text="[等待] 三个箱子已清空，请添加物体。")


# ---------- 4. 创建界面 ----------
title = tk.Label(
    window,
    text="小分机器人",
    font=("Microsoft YaHei", 20, "bold")
)
title.pack(pady=10)

tip = tk.Label(
    window,
    text="点击颜色按钮添加物体，每个箱子最多装3件。"
)
tip.pack()

# 画布：用来画物体和箱子
canvas = tk.Canvas(
    window,
    width=620,
    height=310,
    bg="#f5f7fa",
    highlightthickness=0
)
canvas.pack(pady=8)

canvas.create_text(320, 20, text="物体入口", font=("", 12))

# 画三个箱子及数量标签
for color in counts:
    x = positions[color]

    canvas.create_rectangle(
        x - 75, 210, x + 75, 280,
        fill="white",
        outline=colors[color],
        width=4
    )

    count_labels[color] = canvas.create_text(
        x, 295,
        text=f"{boxes[color]}：0/{capacity}",
        font=("", 12)
    )

# 按钮区
button_frame = tk.Frame(window)
button_frame.pack()

color_buttons = []

for color in counts:
    button = tk.Button(
        button_frame,
        text=f"添加{color}物体",
        bg=colors[color],
        width=14,
        command=lambda c=color: start_sort(c)
    )
    button.pack(side="left", padx=5)
    color_buttons.append(button)

clear_button = tk.Button(
    window,
    text="清空三个箱子",
    command=clear_boxes
)
clear_button.pack(pady=8)

total_label = tk.Label(window, text="累计成功分拣：0 件")
total_label.pack()

status = tk.Label(
    window,
    text="[等待] 请点击按钮添加物体。",
    wraplength=600
)
status.pack(pady=8)

# ---------- 5. 等待用户操作 ----------
window.mainloop()