#!/usr/bin/env python3
import os
#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
"""
PATH expansion:
tidle => $HOME
paramater => ${  } => PATH and $ => valuable
"""


def handle_tidle(command):
    """
    handle tidle in 4 basic case:
    ~string, ~/string,~-, ~+ => DONE
    ~{+,-}[number, string] => WILL BE develop later

    """
    path = os.environ["HOME"]

    if command[0] == "~":
        return [path]
    elif command[0] == "~+":
        return [os.environ["PWD"]]
    elif command[0] == "~-":
        if "OLDPWD" in os.environ.keys():
            return [os.environ["OLDPWD"]]
        else:
            return command
    elif command[0].startswith("~+") is True or command[0].startswith("~-") is True:
        if command[0][2:].isdigit() is False:
            print("%s: command not found" % command[0])
            return [' ']
        else:
            """
            implement pushd later => saved
            implement popd later => delete
            implement dirs later => show
            don't need to implement????????
            """
            # bash: dirs: directory stack empty
            return command# or result
    elif "/" in command[0] and command[0].startswith("~") is True:
        return [path + str(command[0][1:])]
    else:
        return [str(command[0])]


def get_variable(command, dic_var):
    """
    save variable from input of user in prompt
    "=dfgsf" => error
    "asdasa=edvwe" => run normal
    "wewe=" => value=""
    many"=" in command => oke
    """
    for cmd in command:
        if "=" not in cmd and len(command) > 1:
            print("%s: command not found" %cmd)
            return [' ']
    for cmd in command:
        if cmd.startswith("=")is False and cmd.endswith("=") is False:
            key = cmd.split("=")[0]
            value = cmd.split("=")[1]
            dic_var.update({key: value})
            print(dic_var)
    return [' ']


def return_value(paramater, dic_var):
    """
    Get the value in dic_var and environment variables if exist
    else return itself
    """
    parse_variable = []
    #split by "$"
    cmd = paramater.split('$')

    for key in cmd:

        # get key in ${.....}
        if key.startswith("{") is True and key.endswith("}") is True:
            key = key[1:-1]

        # check key in dic_var
        if key in dic_var.keys():
            parse_variable.append(dic_var[key])

        # check key in environment variables
        elif key in os.environ.keys():
            parse_variable.append(os.environ[key])

        # not identify return itself
        else:
            parse_variable.append(key)

    # combain all the values
    return "".join(parse_variable)


def handle_parameter(command, dic_var):
    """
    _parameter expansions with 2 basic cases
          + $PARAMETER
          + ${PARAMETER}
    """
    parse_variable = []
    if "$" in command[0]:
        parse_variable = return_value(command[0], dic_var)
        return [parse_variable]
    else:
        for argument in command:
            temp = argument
            if "$" in argument:
                temp = return_value(argument, dic_var)
            parse_variable.append(temp)
        return parse_variable
