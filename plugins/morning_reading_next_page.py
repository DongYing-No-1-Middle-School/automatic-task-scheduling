plugin = {
    'author': 'YanZihan',
    'version': '0.1',
    'export': [
        'next_page'
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

def change_directory(directory):
    system(f"cd {directory}")

def get_pptx_page(pptx_path):
    try:
        p = Presentation(pptx_path)
        page = len(p.slides)
    except KeyError:
        page = 0
    return page

def next_page():
    pygame.init()
    today = date.today()
    ppt_name = today.strftime('%#m月%#d日早读任务.pptx')
    os.chdir("V:\\团队库\\2023级语文组\\早读课件")
    page=get_pptx_page("V:\\团队库\\2023级语文组\\早读课件\\" + ppt_name)
    if page!=1:
        page-=1
        wait_time=360/page
        for i in range(page):
            pyautogui.press('enter')
