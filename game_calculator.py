import sys
import main, cli_runner, tray, threads, game_setup
from tray import run_tray
import atexit, PIL, subprocess, pystray, psutil, json, os, datetime, time, threading, tabulate

if __name__ == '__main__':
    atexit.register(main.Main.onClose)
    main.Main()
    run_tray()