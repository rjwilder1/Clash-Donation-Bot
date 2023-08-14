import win32gui, win32api, win32con
import time

hwnd = win32gui.FindWindow(None, 'BlueStacks App Player')
hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
hwndChild2 = win32gui.GetWindow(hwndChild, win32con.GW_CHILD)

s = "Clash of Clans"

def PressKeys(chars):
    for i in chars:
        win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, ord(i.upper()), 0)

PressKeys(s)