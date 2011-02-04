#!/usr/bin/python3
#
# (c) Franck Labadille franck@kernlog.net 2011
# LICENCE BSD
#

from pynancial.ui import *
import code

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

try:
	while True:
		userinteract = code.InteractiveConsole()
		response = userinteract.raw_input("What do you want to do ?\n\
e : Extend database\n\
f : Find in database\n\
u : get URL\n\
q : Quit\n")

		if response == "e":
			response = userinteract.raw_input("What do you want to add ?\n\
k : stock\t\tx : index\n\
y : symbol\t\tp : provider\t\tf : format\n")

			if response == "p":
				addprovider(db_path)
			elif response == "k":
				addstock(db_path)
			elif response == "x":
				addindex(db_path)
			elif response == "y":
				addsymbol(db_path)
			elif response == "f":
				print("1 : add a new kind of format\n\
2 : insert a new format url string to an alreadyknown format")
				userchoice = userinteract.raw_input(" 1 or 2  : ")
				if userchoice == "1":
					addformat(db_path)
				elif userchoice == "2":
					updateformat(db_path)
				else:
					pass
			else:
				pass

		elif response == "f":
			selectstuff(db_path)

		elif response == "u":
			buildurl(db_path)

		elif response == "q":
			quit()
		else:
			print("select a valid number please")
except KeyboardInterrupt:
	print("KeyboardInterrupt")
	quit()
