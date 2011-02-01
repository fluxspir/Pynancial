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
q : Quit\n")
# 3 Create URL\n\

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
				addformat(db_path)
			else:
				pass

		elif response == "f":
			selectstuff(db_path)

		elif response == "u":
			""" build url"""
			pass

		elif response == "q":
			quit()
		else:
			print("select a valid number please")
except KeyboardInterrupt:
	print("KeyboardInterrupt")
	quit()
