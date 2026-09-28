"""
    不开启DPI感知，直接计算的版本
"""
import logging
import pathlib
import time

from discern_tools import same_pos_picture
from mouse_tools import click_screen, scroll_up, move_screen
from screen_tools import find_wechat_hwnd, set_foreground_window, set_window_size_ex, screenshot_by_hwnd, \
    get_window_scale
from wechat_control.find_tools import find_template_bottom_up
from wechat_control.identify_tools import anchor_identify
from wechat_control.keyword_tools import send_ctrl_v, set_clipboard_text, delay, send_enter, get_clipboard_text, \
    send_ctrl_w

logging.basicConfig(level=logging.DEBUG)
catch_mode = False
anchor_point_root = pathlib.Path('anchor_point')
if not anchor_point_root.exists():
    anchor_point_root.mkdir()

# 按键延迟
keyword_delay_seconds = 1.5
# 微信窗口 宽，高，x，y
wechat_init_pos = 1024, 800, 0, 0
hwnd = find_wechat_hwnd()
scale = get_window_scale(hwnd=hwnd)
set_foreground_window(hwnd)
set_window_size_ex(hwnd, *wechat_init_pos)

def click_screen_with_check_pos(click_pos, check_pos, try_img, trys=0):
    if same_pos_picture(screenshot_by_hwnd(hwnd),
                        check_pos,
                        anchor_point_root / try_img,
                        catch_mode=catch_mode):
        return True
    click_screen(hwnd, *click_pos)
    time.sleep(1)
    if same_pos_picture(screenshot_by_hwnd(hwnd),
                        check_pos,
                        anchor_point_root / try_img,
                        catch_mode=catch_mode):
        return True
    elif trys < 3:
        # 重试逻辑
        time.sleep(1)
        return click_screen_with_check_pos(click_pos, check_pos, try_img, trys+1)
    raise RuntimeError('定位失败')

def click_link_package(horizontal_x):
    """封装点击连接的脚本"""
    set_window_size_ex(hwnd, *wechat_init_pos)
    same_pos_picture(screenshot_by_hwnd(hwnd),
                     (horizontal_x, 590, 40, 40),
                            anchor_point_root / 'avatar.png',
                            catch_mode=False)

    same_pos_picture(screenshot_by_hwnd(hwnd),
                     (horizontal_x, 0, 40, 640),
                            anchor_point_root / 'large.png',
                            catch_mode=True)
    avatar_pos, confidence = find_template_bottom_up(
        anchor_point_root / 'large.png',
        anchor_point_root / 'avatar.png',
    )
    if not avatar_pos:
        raise RuntimeError('avatar不存在')
    logging.debug(f'avatar_pos: {avatar_pos}, confidence: {confidence}')
    delay(keyword_delay_seconds)(click_screen)(hwnd,
        horizontal_x-50,
        int((avatar_pos[1] + 20 )/ scale))


click_screen_with_check_pos((130, 120), (238, 40, 120, 40), anchor_identify())
click_screen_with_check_pos((530, 700), (270, 740, 200, 40), anchor_identify())
set_clipboard_text("https://mp.weixin.qq.com/s/ldCed8VImYDtEohu5GuSZg")
delay(keyword_delay_seconds)(send_ctrl_v)()
delay(keyword_delay_seconds)(send_enter)()
try:
    click_link_package(945)
except RuntimeError:
    click_link_package(582)

delay(keyword_delay_seconds)(set_window_size_ex)(hwnd, *wechat_init_pos)
# 打开公众号
click_screen(hwnd, 740, 757)

#滚轮到顶部
move_screen(hwnd, 821, 405)
delay(keyword_delay_seconds)(scroll_up)(100)

#点击第一篇 TODO: 定位不准导致不稳定
click_screen(hwnd, 866, 593)

delay(keyword_delay_seconds)(click_screen)(hwnd, 916, 45)
delay(keyword_delay_seconds)(click_screen)(hwnd, 873, 158)
print('newlink', delay(keyword_delay_seconds)(get_clipboard_text)())
