plugin = {
    'author': 'YanZihan',
    'version': '0.1',
    'export': [
        'open_pptx'
    ]
}

from pptx import Presentation
from datetime import date
from os import system
from time import sleep
import os
import datetime
import pyautogui
import win32gui
import win32process
import win32api
import subprocess
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def get_pptx_page(pptx_path):
    try:
        p = Presentation(pptx_path)
        page = len(p.slides)
    except KeyError:
        page = 0
    return page

def get_window_handle_by_process_name(process_name):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                p = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, found_pid)
                exe_name = win32process.GetModuleFileNameEx(p, 0)
                if process_name.lower() in exe_name.lower():
                    hwnds.append(hwnd)
            except Exception as e:
                print(f"Error: {e}")

        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def open_pptx():
    pygame.init()
    today = date.today()
    ppt_name = today.strftime('%#m月%#d日早读任务.pptx')
    os.chdir("V:\\团队库\\2023级语文组\\早读课件")
    page=get_pptx_page("V:\\团队库\\2023级语文组\\早读课件\\" + ppt_name)
    proc = subprocess.Popen("V:\\团队库\\2023级语文组\\早读课件\\" + ppt_name, shell=True)
    if proc.returncode != 0:
        exit()
    process_name = "wps.exe"
    hwnds = get_window_handle_by_process_name(process_name) 
    sleep(10)
    pyautogui.press('F5')
    print("Pressed F5")