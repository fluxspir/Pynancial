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
import pynancial.model as model

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
	response = userinteract.raw_input(message)
	return response

def printtablelist(tablelist):
	""" """
	for t in tablelist:
		print(" {} : {}".format(t[0], t[1]))

def testtablename(tablename):
	""" 
	the tablename the user decided may be :
		* a number   : means that user wants to use a already known table
		* a name : without spaces, exotic characters (...) ; 
	function test that, and return the tablename chosen.
	"""
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

def addprovider():
	""" """
	providerhandler = db.ProviderHandler(db_path, providertable)

#	def gethandlerfromtables():
#		""" """
#		providertable = choosetable("provider")
#		providerhandler = db.ProviderHandler(db_path, providertable)
#		return providerhandler
#
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
	
	print("adding new provider")
	print("select symbols table")
	symboltable = model.choosetable("symbol")
	providerhandler.gethandlerfromtables()
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

