import os
import sys
import shutil
from game_setup import GameSetup
import json
import datetime
import threads

class Game:
    def __init__(self, gameName, exe_path, active_status=False, register_new=False):
        self.gameName = gameName
        self.exe_path = exe_path
        self.exe_name = exe_path.split("\\")[-1]
        self.active_status = active_status
        if register_new:
            GameSetup(gameName, exe_path)
            self.__register()
        with open(f"games/{gameName}/game_config.json", "r") as file:
            data = json.load(file)
        self.time = data["play_time"]

    def __register(self):
        with open("system/games.json", "r") as f:
            data = json.load(f)
        game = {
            "gameName": self.gameName,
            "executable_path": self.exe_path,
            "active_status": self.active_status,
        }
        data["games"].append(game)
        with open("system/games.json", "w") as fi:
            json.dump(data, fi, indent=4)
        system_log(f"{self.gameName} is added successfully!")

    def remove(self):
        with open("system/games.json", "r") as f:
            data = json.load(f)
        for i in range(len(data["games"])):
            if data["games"][i]["gameName"] == self.gameName:
                data["games"].pop(i)
        with open("system/games.json", "w") as fi:
            json.dump(data, fi, indent=4)
        shutil.rmtree(f"games/{self.gameName}")
        system_log(f"{self.gameName} is removed successfully!")

    def activate(self):
        if is_game(self):
            with open("system/games.json", "r") as f:
                data = json.load(f)
            if data["games"][getGame(self.gameName)[1]]["active_status"] is False:
                data["games"][getGame(self.gameName)[1]]["active_status"] = True
                system_log(f"{self.gameName} is activated!")
            with open("system/games.json", "w") as f:
                json.dump(data, f, indent=4)
            if not sys.executable.endswith("cli_runner.exe"):
                threads.Threads.monitor_game(self.exe_name, self.gameName)

    def disable(self):
        if is_game(self):
            with open("system/games.json", "r") as f:
                data = json.load(f)
            if data["games"][getGame(self.gameName)[1]]["active_status"] is True:
                data["games"][getGame(self.gameName)[1]]["active_status"] = False
                system_log(f"{self.gameName} is disabled!")
            with open("system/games.json", "w") as f:
                json.dump(data, f, indent=4)
            if not sys.executable.endswith("cli_runner.exe"):
                threads.Threads.deactivate_game(self.gameName)

class Main:
    def __init__(self):
        threads.Threads()
        if not os.path.isdir("games"):
            os.mkdir("games")
        if not os.path.isdir("system"):
            os.mkdir("system")
            with open("system/log.txt", "w") as _:
                pass
            with open("system/games.json", "w") as f:
                json.dump({"games": []}, f, indent=4)
        for game in getGames():
            if game.active_status:
                game.activate()

    @staticmethod
    def onClose():
        print("Closing...")
        for game in getGames():
            calculate_time(game.gameName)

def getGames() -> list[Game]:
    games = []
    with open("system/games.json", "r") as f:
        data = json.load(f)
    for game in data["games"]:
        games.append(Game(game["gameName"], game["executable_path"], game["active_status"]))
    return games

def getGame(gameName) -> (Game, int):
    for i in range(len(getGames())):
        if getGames()[i].gameName == gameName:
            return getGames()[i], i
    return None

def calculate_time(gameName):
    with open(f"games/{gameName}/game_config.json", "r") as f:
        data = json.load(f)
    with open (f"games/{gameName}/logs.txt", "r") as f:
        log = f.readlines()
    enters = removeAll([(datetime.datetime.strptime(i.removesuffix("\n").split("]")[0][1::], "%d-%m-%Y %H:%M:%S") if i.removesuffix("\n").endswith("The game is running!") else 0) for i in log], 0)
    outs = removeAll([(datetime.datetime.strptime(i.removesuffix("\n").split("]")[0][1::], "%d-%m-%Y %H:%M:%S") if i.removesuffix("\n").endswith("The game is stopped!") else 0) for i in log], 0)
    if outs < enters:
        outs.append(datetime.datetime.now())
    time = 0
    for i in range(len(enters)):
        time += (outs[i] - enters[i]).total_seconds() / 60
    time = int(time)
    data["play_time"] = time
    with open(f"games/{gameName}/game_config.json", "w") as f:
        json.dump(data, f)

def compare_games(game1:Game, game2:Game) -> bool:
    if game1.gameName == game2.gameName and game1.exe_path == game2.exe_path and game1.active_status == game2.active_status:
        return True
    return False

def is_game(game:Game) -> bool:
    for gm in getGames():
        if compare_games(game, getGame(gm.gameName)[0]):
            return True
    return False

def removeAll(lst, value) -> list:
    a = []
    for i in lst:
        if i != value:
            a.append(i)
    return a

def system_log(message):
    with open("system/log.txt", "a") as log:
        log.write(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]: {message}\n")
