from typing import Callable
import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo
import threading
import time
import win32gui
import win32con
import ctypes
from ctypes import c_int

dwm = ctypes.windll.dwmapi
user32 = ctypes.windll.user32

class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int), ("cxRightWidth", c_int), ("cyTopHeight", c_int), ("cyBottomHeight", c_int)]

class ExternalOverlay:
    def __init__(self, target_window: str, ui_to_run: Callable, overlay_name: str = "Overlay"):
        self.target_window = target_window
        self.overlay_name = overlay_name
        self.ui_to_run = ui_to_run
        self.target_hwnd = None
        self.overlay_hwnd = None
    
    def start(self, overlay_delay: float = 0.05):
        ui_thread = threading.Thread(target=self._init_ui)
        ui_thread.start()
        time.sleep(0.5)
        if(self.target_hwnd == None or self.overlay_hwnd == None):
            raise Exception("Creating handles failed.")
        hook_thread = threading.Thread(target=self._hook_to_target(overlay_delay))
        hook_thread.start()

    def _set_handles(self):
        self.target_hwnd = win32gui.FindWindow(None, self.target_window)
        if not self.target_hwnd:
            raise Exception("Target Window not found.")
        self.overlay_hwnd = win32gui.FindWindow(None, self.overlay_name)
        if not self.overlay_hwnd:
            raise Exception("Overlay Window not found.")

    def _set_dpg_win_transparent(self):
        # DPG does not support transparent window/viewport, so it has to be done manually
        margins = MARGINS(-1, -1,-1, -1)
        dwm.DwmExtendFrameIntoClientArea(self.overlay_hwnd, margins) 
        # Making the overlay click-through
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT )

    def _hook_to_target(self, overlay_delay: float):
        tar_rect = win32gui.GetWindowRect(self.target_hwnd)
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, tar_rect[0], tar_rect[1], tar_rect[2]-tar_rect[0], tar_rect[3]-tar_rect[1], win32con.SWP_NOZORDER)
        while True:
            tar_rect = win32gui.GetWindowRect(self.target_hwnd)
            win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, tar_rect[0], tar_rect[1], tar_rect[2]-tar_rect[0], tar_rect[3]-tar_rect[1], win32con.SWP_NOZORDER)
            time.sleep(overlay_delay)
        
    def _init_ui(self):
        dpg.create_context()
        dpg.create_viewport(title=self.overlay_name, width=300, height=300, decorated=False, always_on_top=True, clear_color=[0.0,0.0,0.0,0.0]),
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self._set_handles()
        self._set_dpg_win_transparent()
        self.ui_to_run(self.target_hwnd)
        dpg.start_dearpygui()
        dpg.destroy_context()