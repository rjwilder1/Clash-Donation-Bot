import ctypes
import win32api
import win32con
import win32gui
from ctypes import wintypes, Structure, windll, POINTER, pointer

LONG = wintypes.LONG
DWORD = wintypes.DWORD
ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(Structure):
    _fields_ = (
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    )

class INPUT(Structure):
    _fields_ = (
        ("type", DWORD),
        ("mi", MOUSEINPUT)
    )

def click_at(x, y):
    # Convert screen coordinates to normalized coordinates
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    normalized_x = 65536 * x // screen_width + 1
    normalized_y = 65536 * y // screen_height + 1

    # Create the INPUT structures
    input_structures = (INPUT * 2)()
    
    # Mouse press event
    input_structures[0].type = win32con.INPUT_MOUSE
    input_structures[0].mi.dx = normalized_x
    input_structures[0].mi.dy = normalized_y
    input_structures[0].mi.mouseData = 0
    input_structures[0].mi.dwFlags = win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTDOWN

    # Mouse release event
    input_structures[1].type = win32con.INPUT_MOUSE
    input_structures[1].mi.dx = normalized_x
    input_structures[1].mi.dy = normalized_y
    input_structures[1].mi.mouseData = 0
    input_structures[1].mi.dwFlags = win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTUP

    # Send the INPUT structures to the system
    windll.user32.SendInput(2, pointer(input_structures[0]), ctypes.sizeof(input_structures[0]))

click_at(1920, 0)