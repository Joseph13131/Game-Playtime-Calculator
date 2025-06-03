import json
import os
import datetime

class GameSetup:
    def __init__(self, game_name, exe_path):
        if not os.path.isdir(f"games/{game_name}"):
            os.mkdir(f"games/{game_name}")
        c = {
            "game_name": game_name,
            "exe_name": exe_path.split("\\")[-1],
            "registration_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "play_time": 0
        }
        with open(f"games/{game_name}/game_config.json", "w") as f:
            json.dump(c, f, indent=4)
        with open(f"games/{game_name}/logs.txt", "a") as fa:
            fa.write(f"[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]: Game registered!\n")
        self.exe_path = exe_path
        self.game_name = game_name
