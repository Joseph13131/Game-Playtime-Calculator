import sys
import main, game_calculator, tray, threads, game_setup
import atexit, PIL, subprocess, pystray, psutil, json, os, datetime, time, threading, tabulate

def getInput() -> main.Game:
    games = main.getGames()
    print("\nEnter the game code: ")
    print("\n-----------------------------------")
    for i in range(len(games)):
        print("- " + games[i].gameName + f" [{i+1}]")
    print("-----------------------------------\n")
    num = int(input("===> "))
    return games[num-1]

if __name__ == "__main__":
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
