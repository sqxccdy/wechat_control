import logging

import win32gui
import win32api
import win32con
import ctypes
from ctypes import wintypes


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class INPUT_union(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_union),
    ]

move_cursor = lambda x, y : ctypes.windll.user32.SetCursorPos(x, y)

def mouse_click():
    extra = ctypes.c_ulong(0)
    inp = INPUT()
    inp.type = win32con.INPUT_MOUSE
    inp.union.mi = MOUSEINPUT(
        dx=0, dy=0, mouseData=0,
        dwFlags=win32con.MOUSEEVENTF_LEFTDOWN,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    # 鼠标左键抬起
    inp2 = INPUT()
    inp2.type = win32con.INPUT_MOUSE
    inp2.union.mi = MOUSEINPUT(
        dx=0, dy=0, mouseData=0,
        dwFlags=win32con.MOUSEEVENTF_LEFTUP,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(inp2))


def click_screen(hwnd, x, y):
    from screen_tools import get_pos_by_hwnd
    left, top, width, height = get_pos_by_hwnd(hwnd)
    if 0<= x <= width and 0<=y <= height:
        logging.debug(f'hwnd: {hwnd}, left: {left}, top: {top}')
        logging.debug(f'move cursor to: {left + x}, {top + y}')
        move_cursor(left + x, top + y)
        mouse_click()
    else:
        raise RuntimeError('位置下标越界。检查脚本逻辑')