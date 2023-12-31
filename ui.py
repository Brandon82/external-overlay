import dearpygui.dearpygui as dpg
import psutil
import win32gui
import win32process

def get_window_info(target_hwnd):
    window_title = win32gui.GetWindowText(target_hwnd)
    process_id = win32process.GetWindowThreadProcessId(target_hwnd)[1]
    process_name = None
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['pid'] == process_id:
            process_name = proc.info['name']
            break
    return {
        'window_title': window_title,
        'process_id': process_id,
        'process_name': process_name,
    }

def auto_center_cb(s, d):
    viewport_w = dpg.get_viewport_width()
    win_w = dpg.get_item_width("main_win")
    dpg.set_item_pos("main_win", [(viewport_w-win_w)-10, 80])

def ui(tar_hwnd=None):
    dpg.set_viewport_resize_callback(auto_center_cb)
    window_info = get_window_info(tar_hwnd)
    with dpg.window(tag="main_win", no_background=False, no_move=False, no_resize=True, no_title_bar=True, autosize=True):
        dpg.add_text("Process Information:")
        dpg.add_text("Process Window: " + window_info['window_title'])
        dpg.add_text("Process Name: " + window_info['process_name'])
        dpg.add_text("Process ID: " + str(window_info['process_id']))