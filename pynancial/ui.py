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

class UserInteract:
	"""
	
	Interact with user
	
	"""
	def __init__(self, db_path, user=""):
		""" """
		self.user = user

	def askuser(self, message):
		""" """
		userinteract = code.InteractiveConsole()
		response = userinteract.raw_input(message)
		return response

	def printtablelist(self, tablelist):
		""" 
		print the table list :
				1   table_1
				2   table_2
		from tablelist [ ( 1, table_1 ), ... ]
		be careful : 1 = tablelist[0]
		"""
		for t in tablelist:
			print(" {} : {}".format(t[0], t[1]))

	def choosetable(self, db_path, tablegroup=""):
		"""
		after displaying to user tables known, ask to user to pick one.
	    returns the user's choice.
		"""
		dbinteract = TableGroupHandlerInteract(db_path)

		tablelist = dbinteract.gettablelist(tablegroup)
		message = "Which table do you want to use ?\n\
Most people will only need one table. If the table you want to\
use is not in the list, just write its name please.\n"
		print(message)
		self.printtablelist(tablelist)
		tablename = self.askuser("Table number, or new table name, please :  ")
		dbinteract._testtablename(tablename)
		return tablename

class TableGroupHandlerInteract:
	""" 
	
	Interact avec model.py

	"""
	def __init__(self, db_path):
		self.db_path = db_path
		self.tablegrouphandler = model.TableGroupHandler(db_path)

	def _testtablename(self, tablename):
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

	def gettablelist(self, tablegroup):
		""" 
		after displaying to user tables known, ask to user to pick one.
		returns the user's choice.
		"""
		print("searching in metatable for tablegroup {}".format(tablegroup))
		tablelist = self.tablegrouphandler.gettablelist(tablegroup)
		return tablelist

def addprovider(db_path):
	""" 
	
	"""
	usrint = UserInteract(db_path)
	def getproviderinfos():
		"""
		tablelist = [ ( number(start at 1) , tablename ) ]
		"""
		providerinfos = []
		def interactuser():
			name = usrint.askuser("provider short name ; ex : yahoo	: ")
			baseurl = usrint.askuser("baseurl for your provider		: ")
			preformat = usrint.askuser("url part that introduce queryformat	: ")
			presymbol = usrint.askuser("url part that introduce symbols	: ")
			providerinfo = ( name, baseurl, preformat, presymbol )
			providerinfos.append(providerinfo)
			addprvd = usrint.askuser("add an other provider ? y/n :	")
			if addprvd == "y":
				interactuser()
			return providerinfos

		providerinfos = interactuser()
		return providerinfos

	print("adding new provider\n")
	print("select provider's table")
	providertable = usrint.choosetable(db_path, "provider")
	providerinfos = getproviderinfos()
	print("select symbol's table")
	symboltable = usrint.choosetable(db_path, "symbol")
	providerhandler = model.ProviderHandler(db_path, providertable)
	providerhandler.addnewprovider(providerinfos, symboltable)

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



