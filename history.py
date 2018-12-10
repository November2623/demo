#!/usr/bin/env python3


def handle_history(command, dict_history):
    if len(command) == 1:
        for key in range(1, len(dict_history) + 1):
            line = '   ' + str(key) + '  ' + str(dict_history[key])
            print(line)
    else:
        if command[1] == '-c': # cleaar history
            dict_history = {}
        elif command[1][0] == "+" and command[1][1:].isdigit() is True:
            show_short_history(int(command[1][1:]), dict_history)
        elif command[1].isdigit() is True:
            show_short_history(int(command[1]), dict_history)
        else:
            print("bash: history: %s: numeric argument required" %command[1])
    return [' ']


def show_short_history(num_line, dict_history):
    for i in range(num_line -1 , -1, -1):
        line = '   ' + str(len(dict_history) - i) + '  ' + str(dict_history[len(dict_history) - i])
        print(line)


def handle_exclamation_mark_history(command, dict_history, dic_var):
    if len(command[0]) == 1:
        return [' ']
    else:
        if command[0][1:].isdigit() is True:
            print(dict_history[int(command[0][1:])])
            return dict_history[int(command[0][1:])].split()
        else:
            if command[0][1] == "!":
                print(dict_history[len(dict_history)-1])
                return dict_history[len(dict_history)-1].split()
            else:
                print("bash: %s: event not found" %command[0])
                return [' ']
