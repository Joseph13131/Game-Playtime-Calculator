import sys
import main, game_calculator, tray, threads, game_setup
import atexit, PIL, subprocess, pystray, psutil, json, os, datetime, time, threading, tabulate
from pure_path import pure_path

def getInput() -> main.Game:
    games = main.getGames()
    print("\nEnter the game code: ")
    print("\n-----------------------------------")
    for i in range(len(games)):
        print("- " + games[i].gameName + f" [{i+1}]")
    print("-----------------------------------\n")
    num = int(input("===> "))
    return games[num-1]

def calculate_time(gameName):
    with open(pure_path(f"games/{gameName}/game_config.json"), "r") as f:
        data = json.load(f)
    with open(pure_path(f"games/{gameName}/logs.txt"), "r") as f:
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
    with open(pure_path(f"games/{gameName}/game_config.json"), "w") as f:
        json.dump(data, f)

def removeAll(lst, value) -> list:
    a = []
    for i in lst:
        if i != value:
            a.append(i)
    return a

if __name__ == "__main__":
    games = main.getGames()
    for game in games:
        calculate_time(game.gameName)
    os.system('')
    while True:
        inp = input("Type a command (1 = add a game, 2 = activate a game, 3 = deactivate a game, 4 = remove a game, 5 = list the games) (Press x to exit): ")
        if inp.lower() == "x":
            break
        match int(inp):
            case 1:
                gn = input("Enter the game name: ")
                ep = input("Enter the executable path: ")
                main.Game(gn, ep, register_new=True)
                print("\nSuccessfully completed!\n")
                pass
            case 2:
                i = getInput()
                gn = i.gameName
                if main.getGame(gn) is None:
                    print(f"\nGame {gn} doesn't exist\n")
                else:
                    game = main.getGame(gn)[0]
                    a = main.getGames()[0]
                    if game.active_status is True:
                        print(f"\nGame {gn} is already active!\n")
                    else:
                        game.activate()
                        print("\nSuccessfully completed!\n")
            case 3:
                i = getInput()
                gn = i.gameName
                if main.getGame(gn) is None:
                    print(f"\nGame {gn} doesn't exist\n")
                else:
                    game = main.getGame(gn)[0]
                    if game.active_status is False:
                        print(f"Game {gn} is already deactive!\n")
                    else:
                        game.disable()
                        print("\nSuccessfully completed!\n")
            case 4:
                i = getInput()
                gn = i.gameName
                if main.getGame(gn) is None:
                    print(f"\nGame {gn} doesn't exist\n")
                else:
                    game = main.getGame(gn)[0]
                    game.remove()
                    print("\nSuccessfully completed!\n")
            case 5:
                games = main.getGames()
                header_elements = ["\033[1mGame Name\033[0m", "\033[1mActive Status\033[0m", "\033[1mTime (Minutes)\033[0m"]
                list_elements = []
                for game in games:
                    list_elements.append([game.gameName, ('Active' if game.active_status else 'Deactive'), game.time])
                print("\n" + tabulate.tabulate(list_elements, header_elements, tablefmt="grid") + "\n")
            case _:
                pass

