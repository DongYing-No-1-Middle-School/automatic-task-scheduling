plugin = {
    'author': 'YanZihan',
    'version': '0.1',
    'export': [
        'play_sounds'
    ]
}

import win32api
import win32con
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def set_volume(volume):
    win32api.SendMessage(
        win32con.HWND_BROADCAST, win32con.WM_APPCOMMAND, 0x30292, volume * 0xFFFF // 100)

def play_sounds(FILE_NAME,volume=0.7):
    pygame.init()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    nowdate = time.strftime('%m%d', time.localtime(time.time()))
    FILE_NAME = FILE_NAME.replace('{date}', nowdate)
    pygame.mixer.music.load(FILE_NAME)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()
