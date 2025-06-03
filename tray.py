from pystray import Icon, Menu, MenuItem
from PIL import Image
import sys, subprocess
import os
import threading
import json
import threads
import main


def run_tray():
    img = Image.open(resource_path('assets/icon.ico'))
    icon = Icon("Game Time Calculator", img, menu=Menu(
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
        with open("system/games.json", "r") as f:
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