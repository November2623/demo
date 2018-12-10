#!/usr/bin/env python3
import os

def handle_cd(command):
    """
    BUILTIN - CD - CHANGE DIRECTORY
    cd ~ go HOME
    cd / go root
    cd - go previous directory
    """
    # got to HOME
    if len(command) == 1 or command[1] == "~":
        # "HOME" in environment variable
        if "HOME" in os.environ.keys():
            os.environ.update({"OLDPWD": os.getcwd()})
            os.chdir(os.environ["HOME"])
        # "HOME" is unseted
        else:
            print("intek-sh: cd: HOME not set")

    # go to previous PATH
    elif command[1] == "-":
        os.environ.update({"OLDPWD": os.getcwd()})
        os.chdir(os.environ["OLDPWD"])

    # raise error PATH is file
    elif os.path.isfile(command[1]) is True:
        print("bash: cd: %s: Not a directory" % command[1])

    # raise error when PATH don't exist
    elif os.path.isdir(command[1]) is False:
        print("bash: cd: %s: No such file or directory" % command[1])

    # PATH is valid => change dir
    else:
        # save the previous PATH before changing dir
        os.environ.update({"OLDPWD": os.getcwd()})
        # change dir
        os.chdir(command[1])

    # save current PATH into environment variable
    os.environ.update({"PWD": os.getcwd()})


def handle_export(command):
    """
    BUILTIN - EXPORT - save environment variables

    """
    list_export = command[1:]
    for item in list_export:
        if "=" in item:
            if item.startswith("=") is True:
                print("-bash: export: `%s': not a valid identifier" %item)
            else:
                parse = item.split("=")
                key = parse[0]
                # some case more "=" in argument
                value = '='.join(parse[1:])
                # check ending "=" should valid when only one "=" in argument
                if item.endswith("=") is True and item.count("=") == 1:
                    os.environ.update({item: ''})
                else:
                    os.environ.update({key: value})


def handle_unset(command):
    """
    BUILTIN - UNSET VARIABLE environment
    """
    list_unset = command[1:]
    for key in list_unset:
        if key in os.environ.keys():
            del os.environ[key]


def handle_exit_status(command): ## need to rebuilt
    print("NOT THING")
