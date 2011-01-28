#!/usr/bin/python3
#
# (c) Franck Labadille franck@kernlog.net 2011
# LICENCE BSD
#

from pynancial.ui import *

if len(sys.argv) < 2:
    message = """

    NOM
        pyFinancial.py

    SYNOPSIS
        pyFinancial.py file.db

    """
    print(message)
    quit()

db_path = sys.argv[1]

while True:
	addprovider()
	print("new try to add")

while True:
    response = userinteract.raw_input("What do you want to do ?\n\
        1 Extend database\n")
#        2 Find in database\n\
#        3 Create URL\n\
#        9 Quit\n")

    userinteract = code.InteractiveConsole()
    if int(response) == 1:
        response = userinteract.raw_input("What do you want to add ?\n\
            1 provider\n")
#            2 stock\n\
#            3 index\n\
#            4 format\n")

        if int(response) == 1:
            addprovider()
        elif int(response) == 2:
            addstock()
        elif int(response) == 3:
            addindex()
        elif int(response) == 4:
            addformat()
        else:
            pass
    elif int(response) == 2:
        pass
    elif int(response) == 3:
        pass
    elif int(response) == 9:
        quit()
    else:
        print("select a valid number please")

