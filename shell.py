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
	1 Extend database\n\
	2 Find in database\n\
	9 Quit\n")
	#        3 Create URL\n\

		if int(response) == 1:
			response = userinteract.raw_input("What do you want to add ?\n\
	1 provider\n\
	2 stock\n\
	3 index\n\
	4 format\n")

			if int(response) == 1:
				addprovider(db_path)
			elif int(response) == 2:
				addstock(db_path)
			elif int(response) == 3:
				addindex()
			elif int(response) == 4:
				addformat()
			else:
				pass
		elif int(response) == 2:
			selectstuff(db_path)

		elif int(response) == 3:
			pass
		elif int(response) == 9:
			quit()
		else:
			print("select a valid number please")
except KeyboardInterrupt:
	print("KeyboardInterrupt")
	quit()
