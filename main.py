"""
    不开启DPI感知，直接计算的版本
"""
import logging
import pathlib
import time

from discern_tools import same_pos_picture
from mouse_tools import click_screen
from screen_tools import find_wechat_hwnd, set_foreground_window, set_window_size_ex, screenshot_by_hwnd

logging.basicConfig(level=logging.DEBUG)
catch_mode = True

anchor_point_root = pathlib.Path('anchor_point')
# 微信窗口 宽，高，x，y
wechat_init_pos = 1024, 800, 0, 0
hwnd = find_wechat_hwnd()

set_foreground_window(hwnd)
set_window_size_ex(hwnd, *wechat_init_pos)

click_screen(hwnd, 130, 120)
time.sleep(3)
if same_pos_picture(screenshot_by_hwnd(hwnd),
                 (405, 20, 140, 30),
                     anchor_point_root / 'img_1.png',
                     catch_mode=catch_mode):
    pass
