try:
    import sys
    sys.path.append("/home/pi/.local/lib/python3.5/site-packages")
except:
    pass

from keyboard import wait,hook
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from .keyboardmodule import key_pressed,key_released

def on_action(event):
    if event.event_type == KEY_DOWN:
        on_press(event.name)

    elif event.event_type == KEY_UP:
        on_release(event.name)

def on_press(key):
    key_pressed(key)

def on_release(key):
    key_released(key)

def readkeyboardthrd():
    hook(lambda e: on_action(e))
    wait('alt gr')