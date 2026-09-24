"""
    不开启DPI感知，直接计算的版本
"""
import time

from mouse_tools import click_screen
from screen_tools import find_wechat_hwnd, set_foreground_window, set_window_size_ex, screenshot_pillow, \
    get_window_scale, get_pos_by_hwnd, screenshot_by_hwnd
import logging
logging.basicConfig(level=logging.DEBUG)

# 微信窗口 宽，高，x，y
wechat_init_pos = 1024, 800, 0, 0
hwnd = find_wechat_hwnd()

set_foreground_window(hwnd)
set_window_size_ex(hwnd, *wechat_init_pos)

click_screen(hwnd, 130, 120)
time.sleep(5)
wechat_img = screenshot_by_hwnd(hwnd)
