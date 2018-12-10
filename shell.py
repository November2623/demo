#!/usr/bin/env python3
import os, subprocess


def handle_rough_command(rough_commands):
    """
    1. plit program-name and argument by " " in command
    """
    if rough_commands.startswith('`') and rough_commands.endswith('`'):
        return [rough_commands]
    else:
        command = rough_commands.split() # 2
        return command





def handle_execute_command(command, bool):
    if bool is True or len(command) == 1:
        if len(command) == 1 and command[0] == ".":
            print("bash: .: filename argument required\n.: usage: . filename [arguments]")

        # 2 PATH
        elif "/" in command[0] or command[0].startswith("."):
            path = handle_path(command)
            check_path(path, command)

        # 3 bultin-name or external-file or script
        else:
            if check_exists_command(command[0]) == "non_PATH":
                print("intek-sh: " + command[0] + ": No such file or directory")
            elif check_exists_command(command[0]) == "notfound":
                if command[0] != ['history'] and command != [' ']:
                    print("%s: command not found" % command[0])
            elif check_exists_command(command[0]) == "buildin":
                process_commands(command)
            else:
                if(len(command) == 1):
                    a = subprocess.run(command[0])
                    os.environ.update({'STATUS_EXIT': str(a.returncode)})
                else:
                    for arg in command[1:]:
                        a = subprocess.run([command[0], arg])
                        os.environ.update({'STATUS_EXIT': str(a.returncode)})
    else:
        temp = pipe(command).communicate()[0]
        stdout = temp.decode("utf-8").strip()
        print(stdout)




def pipe(command):
    prev_proc = subprocess.Popen(command[0], stdout=subprocess.PIPE)
    proc = ''
    for args in command[1:]:
        if len(args) == 1 and args[0] == ".":
            print("bash: .: filename argument required\n.: usage: . filename [arguments]")

        # 2 PATH
        elif "/" in args[0] or args[0].startswith("."):
            path = handle_path(args)
            check_path(path, args)

        # 3 bultin-name or external-file or script
        else:
            if check_exists_command(args[0]) == "non_PATH":
                print("intek-sh: " + args[0] + ": No such file or directory")
            elif check_exists_command(args[0]) == "notfound":
                if args[0] != ['history'] and args != [' ']:
                    print("%s: command not found" % args[0])
            elif check_exists_command(args[0]) == "buildin":
                process_commands(args)
            else:
                proc = subprocess.Popen(args, stdin=prev_proc.stdout,stdout=subprocess.PIPE)
                print(proc)
                # prev_proc.stdout.close()
    return proc

def handle_path(command):
    if command[0] == ".":
        if not command[1].startswith("/") or not command[1].startswith("./"):
            path = os.getcwd() + "/" + command[1]
    else:
        path = command[0]
    return path


def check_path(path, command):
    name = command[0]
    # print(name, type(name), command, type(command))
    if command[0] == ".":
        if len(command) > 1:
            name = command[1]
    if os.path.exists(path) is False:
        print("bash: " + name + ": No such file or directory")
    elif os.path.isdir(path) is True:
        print("bash: " + name + ": Is a directory")
    elif os.path.isfile(path) is True:
        if os.access(path, os.X_OK) is False:
            if command[0] == ".":
                os.chmod(path, 0o755)
                a = subprocess.run(path)
                os.environ.update({'STATUS_EXIT': str(a.returncode)})
            else:
                print("bash: " + name + ": Permission denied")
        else:
            a = subprocess.run(path)
            os.environ.update({'STATUS_EXIT': str(a.returncode)})
    else:
        print("bash: %s: command not found" % name)


def check_exists_command(command):
    """
    if non-exists PATH -> False
    if non-exists command -> True
    exists command -> return where command
    """
    if command in ["cd", "unset", "export", "exit"]:
        return "buildin"
    if 'PATH' not in os.environ:
        return "non_PATH"
    PATH = os.environ['PATH'].split(':')
    for path in PATH:
        if(os.path.exists(path)):
            if command in os.listdir(path):
                return path
    return "notfound"


def process_commands(command):
    processing = {'cd': handle_cd,
                  'unset': handle_unset,
                  'export': handle_export}
    return processing[command[0]](command)


handle_execute_command([['cat', 'note.txt'],['echo']], False)