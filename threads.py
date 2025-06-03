import threading
import psutil
import datetime
import time
import json

class Threads:
    active_threads = []
    @staticmethod
    def monitor_game(exe_name, gameName):
        thread = threading.Thread(target=Threads.__monitor, args=(gameName, exe_name), name="thread-" + gameName.replace(" ", "_"))
        Threads.active_threads.append(thread.name)
        thread.start()

    @staticmethod
    def deactivate_game(gameName):
        if "thread-" + gameName in Threads.active_threads:
            Threads.active_threads.remove("thread-" + gameName)

    @staticmethod
    def __monitor(gameName, exeName):
        was_running = False
        while "thread-" + gameName.replace(" ", "_") in Threads.active_threads and threading.main_thread().is_alive():
            running = any(p.name().lower() == exeName.lower() for p in psutil.process_iter(['name']))
            if running and not was_running:
                if Threads.check_last_log(gameName) in [False, None]:
                    Threads.game_log(gameName, "The game is running!")
                was_running = True
            elif not running and was_running:
                if Threads.check_last_log(gameName):
                    Threads.game_log(gameName, "The game is stopped!")
                Threads.calculate_time(gameName)
                was_running = False
            time.sleep(1)

    @staticmethod
    def check_last_log(gameName) -> bool | None:
        with open(f"games/{gameName}/logs.txt", "r") as log:
            l = log.readlines()
            for i in range(len(l)-1, -1, -1):
                if l[i].endswith("The game is stopped!\n"):
                    return False
                elif l[i].endswith("The game is running!\n"):
                    return True
        return None

    @staticmethod
    def game_log(gameName, message):
        with open(f"games/{gameName}/logs.txt", "a") as log:
            log.write(f"[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]: {message}\n")

    @staticmethod
    def calculate_time(gameName):
        with open(f"games/{gameName}/game_config.json", "r") as f:
            data = json.load(f)
        with open(f"games/{gameName}/logs.txt", "r") as f:
            log = f.readlines()
        enters = removeAll([(datetime.datetime.strptime(i.removesuffix("\n").split("]")[0][1::],
                                                        "%d-%m-%Y %H:%M:%S") if i.removesuffix("\n").endswith(
            "The game is running!") else 0) for i in log], 0)
        outs = removeAll([(datetime.datetime.strptime(i.removesuffix("\n").split("]")[0][1::],
                                                      "%d-%m-%Y %H:%M:%S") if i.removesuffix("\n").endswith(
            "The game is stopped!") else 0) for i in log], 0)
        if outs < enters:
            outs.append(datetime.datetime.now())
        time = 0
        for i in range(len(enters)):
            time += (outs[i] - enters[i]).total_seconds() / 60
        time = int(time)
        data["play_time"] = time
        with open(f"games/{gameName}/game_config.json", "w") as f:
            json.dump(data, f)

def removeAll(lst, value) -> list:
    a = []
    for i in lst:
        if i != value:
            a.append(i)
    return a