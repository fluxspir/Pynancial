#!/usr/bin/python3
#
# (c) Franck Labadille franck@kernlog.net 2011
# LICENCE BSD
#

from pynancial.ui import *

while True:
    print("What do you want to do ?\n\
        1 Add to database\n")
#        2 Find in database\n\
#        3 Create URL\n\
#        9 Quit\n")

    userinteract = code.InteractiveConsole()
    response = userinteract.raw_input("tell me\n")
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

