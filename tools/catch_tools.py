import ctypes
import tkinter as tk
from pynput import mouse
import threading

# ========== 全局状态 ==========
current_x = 0
current_y = 0
records = {
    "F1": None,
    "F2": None,
    "F3": None,
    "F4": None,
}

# ========== 鼠标监听回调 ==========
def on_move(x, y):
    global current_x, current_y
    current_x = x
    current_y = y

def start_mouse_listener():
    """在后台线程中启动鼠标监听"""
    listener = mouse.Listener(on_move=on_move)
    listener.start()

# ========== 更新 UI ==========
def update_ui():
    """每 50ms 刷新一次界面"""
    # 实时坐标
    live_label.config(text=f"当前鼠标坐标：({current_x}, {current_y})")

    # 记录的坐标
    f1_text = f"F1: {records['F1']}" if records['F1'] else "F1: 未记录"
    f2_text = f"F2: {records['F2']}" if records['F2'] else "F2: 未记录"
    f3_text = f"F3: {records['F3']}" if records['F3'] else "F3: 未记录"
    f4_text = f"F4: {records['F4']}" if records['F4'] else "F4: 未记录"

    record_label.config(
        text=f"{f1_text}\n{f2_text}\n{f3_text}\n{f4_text}"
    )

    root.after(50, update_ui)

dpi = ctypes.windll.user32.GetDpiForSystem()
scale = 1.5
print(scale)
# ========== 键盘绑定 ==========
def record_f1(event):
    records["F1"] = (round(current_x / scale, 2), round(current_y / scale, 2))

def record_f2(event):
    records["F2"] = (round(current_x / scale, 2), round(current_y / scale, 2))

def record_f3(event):
    records["F3"] = (round(current_x / scale, 2), round(current_y / scale, 2))
def record_f4(event):
    records["F4"] = (round(current_x / scale, 2), round(current_y / scale, 2))
# ========== 构建界面 ==========
root = tk.Tk()
root.title("鼠标坐标采集工具")
root.geometry("350x250")
root.resizable(False, False)

live_label = tk.Label(
    root,
    text="当前鼠标坐标：(0, 0)",
    font=("Consolas", 12),
    fg="blue"
)
live_label.pack(pady=15)

tip_label = tk.Label(
    root,
    text="移动鼠标，按 F1~F4 记录坐标",
    font=("Microsoft YaHei", 10)
)
tip_label.pack(pady=5)

record_label = tk.Label(
    root,
    text="F1: 未记录\nF2: 未记录\nF3: 未记录\nF4: 未记录",
    font=("Consolas", 11),
    justify="left"
)
record_label.pack(pady=15)

# 绑定 F1~F4 快捷键
root.bind("<F1>", record_f1)
root.bind("<F2>", record_f2)
root.bind("<F3>", record_f3)
root.bind("<F4>", record_f4)

# ========== 启动 ==========
start_mouse_listener()   # 后台鼠标监听
update_ui()              # 启动 UI 刷新循环
root.mainloop()