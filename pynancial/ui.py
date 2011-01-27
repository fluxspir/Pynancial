#!/usr/bin/python3
# (c) Franck LABADILLE
# LICENCE BSD
# 20110127
# Pynancial.ui
#

"""

"""
import code
import sys
import pynancial.model 

if len(sys.argv) < 2:
	message = """

	NOM
		pyFinancial.py

	SYNOPSIS
		pyFinancial.py file.db

	"""
	print(message)
	sys.exit(1)

db_path = sys.argv[1]

def askuser(message):
	userinteract = code.InteractiveConsole()
	response = userinteract.rawinput(message)
	return response

def gettablelist(tablegroup=""):
	""" """
	tablelist = []
	dbhandler = db.DBHandler(db_path)
	tablesindb = dbhandler.gettablelist(tablegroup)
	i = 1
	for t in tablesindb:
		tablelist.append((i, t))
	return tablelist

def printtablelist(tablelist):
	""" """
	for t in tablelist:
		print(" {} : {}".format(t[0], t[1]))

def verifytableexists(tablename):
	""" """
	dbhandler = DBHandler(db_path)
	tableindb = dbhandler.gettablename(tablename)
	if tableindb:
		return tableindb
	else:
		return

def testtablename(tablename):
	""" """
	if not tablename:
		addprovider()
	elif tablename.isdigit():
		i = int(tablename)
		try:
			tablename = tablelist[i-1][1]
		except IndexError:
			message = "Please use alpha numeric for table name"
			print(message)
			addprovider()
	elif tablename.isalnum():
		pass
	else:
		message = "Please use alpha numeric for table name"
		print(message)
		addprovider()

def choosetable(tablegroup):
	""" """
	tablelist = gettablelist(tablegroup)
	message = "Which table do you want to use ?\n\
	Most people will only need one table. If the table you want to\
	use is not in the list, just write its name please.\n"
	printablelist(tablelist)
	tablename = askuser("Table number, or new table name : ")
	testtablename(tablename)
	return tablename

def addprovider():
	""" """
	def gethandlerfromtables():
		""" """
		providertable = choosetable("provider")
		providerhandler = db.ProviderHandler(db_path, providertable)
		return providerhandler

	def getproviderinfos():
		""" """
		providerinfos = []
		def interactuser():
			name = askuser("please give provider short name ; ex : yahoo")
			baseurl = askuser("give the baseurl for your provider")
			preformat = askuser("give url part that introduce queryformat")
			presymbol = askuser("give url part that introduce symbols")
			providerinfo = ( name, baseurl, preformat, presymbol )
			providerinfos.append(providerinfo)
			addprvd = askuser("do you want to add an other provider ? y/n")
			if addprvd == y:
				inderactuser()
			return providerinfos

		providerinfos = interactuser()
		return providerinfos

	symboltable = choosetable("symbol")
	providerhandler = gethandlerfromtables()
	provider.addnewprovider(providerinfos, symboltable)

def addstock():
	""" """
	pass

def addindex():
	""" """
	pass

def addformat():
	""" """
	def gethandlerfromtables():
		""" """
		formattable = choosetable("format")
		formathandler = gethandlerfromtables(db, formattable)

	def getformatinfos():
		""" """


def quit():
	""" """
	sys.exit(0)

while True:
	print("What do you want to do ?\n\
		1 Add to database\n\
		2 Find in database\n\
		3 Create URL\n\
		9 Quit\n")

	userinteract = code.InteractiveConsole()
	response = userinteract.raw_input("tell me\n")
	if int(response) == 1:
		response = userinteract.raw_input("What do you want to add ?\n\
			1 provider\n\
			2 stock\n\
			3 index\n\
			4 format\n")

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
	
