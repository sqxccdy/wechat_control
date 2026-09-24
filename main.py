"""
    不开启DPI感知，直接计算的版本
"""
import time

from mouse_tools import click_screen
from screen_tools import find_wechat_hwnd, set_foreground_window, set_window_size_ex, screenshot_pillow, \
    get_window_scale, get_pos_by_hwnd
import logging
import win32gui
import win32con
logging.basicConfig(level=logging.DEBUG)

# 微信窗口 宽，高，x，y
wechat_init_pos = 1024, 800, 0, 0
hwnd = find_wechat_hwnd()
scale = get_window_scale(hwnd)
set_foreground_window(hwnd)
set_window_size_ex(hwnd, *wechat_init_pos)

click_screen(hwnd, 130, 120)
# time.sleep(5)

# 10个像素的相对位置是为了去掉windows自带的毛玻璃效果的边框
wechat_x, wechat_y, wechat_width, wechat_height = get_pos_by_hwnd(hwnd)
img = screenshot_pillow()
crop_x, crop_y = wechat_x + 10, wechat_y
crop_width, crop_height = wechat_width * scale - 20, wechat_height * scale
crop_box = (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
cropped = img.crop(crop_box)
cropped.show()
