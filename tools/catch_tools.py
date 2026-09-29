import ctypes
import time
import tkinter as tk
from tkinter import filedialog
from pynput import mouse
from PIL import ImageGrab

# ========== 全局状态 ==========
current_x = 0
current_y = 0
records = {
    "F1": None,
    "F2": None,
    "F3": None,
    "F4": None,
}
target_hwnd = None
target_title = ""
picking_hwnd = False
pick_listener = None

scale = 1.0

# ========== DPI ==========
def update_scale_from_hwnd(hwnd):
    global scale
    try:
        dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
        if dpi == 0:
            dpi = ctypes.windll.user32.GetDpiForSystem()
    except Exception:
        dpi = ctypes.windll.user32.GetDpiForSystem()
    scale = dpi / 96.0
    return dpi

# ========== 常驻鼠标移动监听 ==========
def on_move(x, y):
    global current_x, current_y
    current_x = x
    current_y = y


def start_mouse_listener():
    """只启动一次，永远不关"""
    listener = mouse.Listener(on_move=on_move)
    listener.start()

# ========== 取窗体监听 ==========
def on_pick_click(x, y, button, pressed):
    global target_hwnd, target_title, picking_hwnd, pick_listener

    if not picking_hwnd:
        return True

    if pressed and button == mouse.Button.left:
        picking_hwnd = False

        hwnd = ctypes.windll.user32.WindowFromPoint(
            ctypes.wintypes.POINT(int(x), int(y))
        )

        if hwnd:
            dpi = update_scale_from_hwnd(hwnd)
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)

            target_hwnd = hwnd
            target_title = buff.value
            print(f"✅ 获取到窗口: hwnd={hwnd}, 标题='{buff.value}', DPI={dpi}, scale={scale:.2f}")
        else:
            target_hwnd = None
            target_title = ""
            print("❌ 未获取到窗口")

        root.after(0, update_hwnd_display)
        root.after(0, update_scale_display)

        if pick_listener:
            pick_listener.stop()
            pick_listener = None

    return False

# ========== UI 更新 ==========
def update_ui():
    live_label.config(text=f"当前鼠标坐标：({current_x}, {current_y})")
    update_scale_display()
    root.after(50, update_ui)

def update_scale_display():
    scale_label.config(text=f"DPI Scale: {scale:.2f}")

def update_hwnd_display():
    if target_hwnd:
        hwnd_label.config(
            text=f"目标窗口: {target_title}\nHWND: {target_hwnd}",
            fg="green"
        )
    else:
        hwnd_label.config(text="目标窗口: 未选择", fg="gray")


def update_scale_display():
    scale_label.config(text=f"DPI Scale: {scale:.2f}")


def update_hwnd_display():
    if target_hwnd:
        hwnd_label.config(
            text=f"目标窗口: {target_title}\nHWND: {target_hwnd}",
            fg="green"
        )
    else:
        hwnd_label.config(text="目标窗口: 未选择", fg="gray")


def update_record_display():
    texts = []
    for k in records:
        v = records[k]
        texts.append(f"{k}: {v}" if v else f"{k}: 未记录")
    record_label.config(text="\n".join(texts))

# ========== 记录坐标 ==========
def make_record(key):
    def _(event):
        records[key] = (int(current_x / scale), int(current_y / scale))
        update_record_display()
    return _


# ========== 取窗体 ==========
def start_pick_hwnd(event=None):
    global picking_hwnd, pick_listener

    if picking_hwnd:
        return

    picking_hwnd = True
    hwnd_label.config(text="🔴 请点击目标窗口...", fg="red")

    pick_listener = mouse.Listener(on_move=on_move, on_click=on_pick_click)
    pick_listener.start()

def cancel_pick_hwnd(event=None):
    global picking_hwnd, pick_listener

    if not picking_hwnd:
        return

    picking_hwnd = False
    if pick_listener:
        pick_listener.stop()
        pick_listener = None

    update_hwnd_display()

# ========== F5 截图（核心：不用 pynput）==========
def capture_by_size(event=None):
    """F5：用主界面宽高 + 当前鼠标位置截图"""
    try:
        w = int(width_var.get())
        h = int(height_var.get())
    except ValueError:
        print("⚠️ 请输入有效的宽高数值")
        return

    if w <= 0 or h <= 0:
        print("⚠️ 宽高必须大于 0")
        return

    # pynput 已经是物理像素（因为设置了 DPI Awareness），直接用
    x1 = int(current_x)
    y1 = int(current_y)
    x2 = int(current_x + w)
    y2 = int(current_y + h)

    print(f"📸 截图区域（物理像素）: ({x1}, {y1}) -> ({x2}, {y2})")
    make_record("F1")(event)  # 顺便记录点击点
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)

    file_path = filedialog.asksaveasfilename(
        parent=root,
        title="保存截图",
        defaultextension=".png",
        initialfile=f"screenshot_{int(time.time())}.png",
        filetypes=[("PNG 图片", "*.png")]
    )

    if file_path:
        img.save(file_path, "PNG")
        print(f"✅ 截图已保存: {file_path}")
    else:
        print("🚫 取消保存")

# ========== 主界面 ==========
root = tk.Tk()
root.title("鼠标坐标采集工具")
root.geometry("400x420")
root.resizable(False, False)

live_label = tk.Label(root, text="当前鼠标坐标：(0, 0)", font=("Consolas", 12), fg="blue")
live_label.pack(pady=10)

tip_label = tk.Label(
    root,
    text="F1~F4 记录坐标 | F5 尺寸截图 | F6 取窗体 | ESC 取消",
    font=("Microsoft YaHei", 9)
)
tip_label.pack(pady=3)

scale_label = tk.Label(root, text=f"DPI Scale: {scale:.2f}", font=("Consolas", 10), fg="purple")
scale_label.pack(pady=2)

hwnd_label = tk.Label(root, text="目标窗口: 未选择", font=("Consolas", 10), fg="gray", justify="left")
hwnd_label.pack(pady=5)

# 截图尺寸
size_frame = tk.Frame(root)
size_frame.pack(pady=8)

tk.Label(size_frame, text="截图宽度:", font=("Microsoft YaHei", 9)).grid(row=0, column=0, padx=5)
width_var = tk.StringVar(value="400")
tk.Entry(size_frame, textvariable=width_var, width=8).grid(row=0, column=1, padx=5)

tk.Label(size_frame, text="截图高度:", font=("Microsoft YaHei", 9)).grid(row=0, column=2, padx=5)
height_var = tk.StringVar(value="300")
tk.Entry(size_frame, textvariable=height_var, width=8).grid(row=0, column=3, padx=5)

record_label = tk.Label(
    root,
    text="F1: 未记录\nF2: 未记录\nF3: 未记录\nF4: 未记录",
    font=("Consolas", 11), justify="left"
)
record_label.pack(pady=10)

# 快捷键
root.bind("<F1>", make_record("F1"))
root.bind("<F2>", make_record("F2"))
root.bind("<F3>", make_record("F3"))
root.bind("<F4>", make_record("F4"))
root.bind("<F5>", capture_by_size)
root.bind("<F6>", start_pick_hwnd)
root.bind("<Escape>", cancel_pick_hwnd)

# 启动
start_mouse_listener()
update_ui()
root.mainloop()
