plugin = {
    'author': 'YanZihan',
    'version': '0.1',
    'export': [
        'play_sounds'
    ]
}

import pyautogui
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def play_sounds(FILE_NAME,volume=0.7):
    actully_volume=100*volume
    for i in range(50):
        pyautogui.press('volumedown')
    for i in range(int(actully_volume/2)):
        pyautogui.press('volumeup')
    
    pygame.init()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    pygame.mixer.music.load(FILE_NAME)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()