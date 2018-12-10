#!/usr/bin/env python3
from shell import handle_rough_command, handle_execute_command
from identify_command import  identify_command
import os
dict_history = {}
dic_var = {}


def main():
    """
    THOSE STEP PROCESSING:
    1. loop input command
    2. handle main processing
    3. handle the rough/hard command
    4. handle identification/expansion/parse command (argumuents/path)
            =>  features are here
    5. handle execute command

    """
    global dict_history
    global dic_var
    run_minish = 'YES'
    rough_commands = ''
    while run_minish:
        # 1. loop input command
        path = "\x1B[34m" + os.getcwd() + "$ "
        print("\033[1;32mintek-sh:" + path, end='')
        try:
            rough_commands = input('\033[1;37m')
        except (EOFError, KeyboardInterrupt):
            break
        # 2. handle main processing
        command = handle_rough_command(rough_commands) # 3
        if command != '' and command != []:
            dict_history.update({len(dict_history) + 1 : rough_commands})
            if command[0] == "exit":
                return
            else:
                handled_command = identify_command(command, dict_history, dic_var) # 4
                # print(handled_command, "****return", type(handled_command))
                handle_execute_command(handled_command[0], handled_command[1]) # 5



main()
