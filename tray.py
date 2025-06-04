from pystray import Icon, MenuItem, Menu
from PIL import Image
import sys, subprocess
import os
import threading
import json
import threads
import main
import winreg

APP_NAME = "Game Time Calculator"
EXE_PATH = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)

def run_tray():
    img = Image.open(resource_path('assets/icon.ico'))
    icon = Icon("Game Time Calculator", img, menu=Menu(
        MenuItem("Start at Boot", toggle_startup, checked=lambda item: is_startup_enabled()),
        MenuItem("Open Console", lambda: threading.Thread(target=open_console, daemon=True).start()),
        MenuItem("Exit", lambda icon: icon.stop())
    ))
    icon.run()

def open_console():
    if sys.platform == "win32":
        l = sys.executable.split("\\")
        l[-1] = "cli_runner.exe"
        path = ""
        for i in range(len(l)):
            if i != len(l)-1:
                path += l[i] + "\\"
            else:
                path += l[i]
        proc = subprocess.Popen(path)
        proc.wait()
        with open(main.pure_path("system/games.json"), "r") as f:
            data = json.load(f)
        games = data["games"]
        for game in games:
            if game["active_status"]:
                gm = main.getGame(game["gameName"])[0]
                threads.Threads.monitor_game(main.getGame(gm.gameName)[0].exe_name, gm.gameName)
            else:
                threads.Threads.deactivate_game(game["gameName"])

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def is_startup_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, "Game Time Calculator")
        return value == sys.executable
    except FileNotFoundError:
        return False

def enable_startup():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, "Game Time Calculator", 0, winreg.REG_SZ, sys.executable)

def disable_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "Game Time Calculator")
    except FileNotFoundError:
        pass

def toggle_startup(icon, item):
    if item.checked:
        disable_startup()
    else:
        enable_startup()
    icon.update_menu()