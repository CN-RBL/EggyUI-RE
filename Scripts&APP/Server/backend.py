# -*- coding: utf-8 -*-

import subprocess
import requests

url_main = ""
url_backup = "47.118.29.36"

print(f"url_main: {url_main}\nurl_backup: {url_backup}\nEggyUI-RE Server Tools\ninput \"l help\" to get help")

# main loop
while True:
    cmd = input("Server> ").split(" ")
    match cmd[0]:
        case "l":
            print("Local command")
            match cmd[1]:
                case "help":
                    print("""Help docs
Command format: [Command class] [Command name] |*Command Args|
Command class:
    | l: Local command
    | m: Sever command: Main Server
        # TIP: Most upload operations are synchronized to the Backup server.
    | b: Sever command: Backup Server
Command:
    | l
    | - help
    | - exit
    ===== ===== =====
    | m
    | - status
    | - ul_news |img path(.png)| |title| |txt path(.txt)|
    | - ul_kit |kit path(.7z)| |version| |name| |description|
    | - ul_update |update kit path(.7z)| |name| |project name|
    ===== ===== =====
    | b
    | - status""")
                case "exit":
                    print("Exit")
                    exit(0)
                case _:
                    print("Unknown command")
        case "m": pass
        case "b":
            match cmd[1]:
                case "status":
                    print(f"Backup Server status: {"OK" if not subprocess.run(f"ping {url_backup}", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).returncode else "Error"}")
        case _:
            print("Unknown command class")
