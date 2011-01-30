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
import pdb

class UserInteract:
	"""
	
	Interact with user
	
	"""
	def __init__(self, db_path, user=""):
		""" """
		self.user = user
		self.db_path = db_path

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
			print(" {} : 	{}".format((int(t[0]) + 1), t[1]))

	def choosetablegroup(self, message=""):
		"""
		after displaying to user tables groups known, ast to user to pick one.
		return userchoice
		"""
		dbinteract = TableGroupHandlerInteract(self.db_path)
		tablegrouplist = dbinteract.gettablegroups()
		if message:
			print(message)
		if tablegrouplist:
			self.printtablelist(tablegrouplist)
		userchoice = self.askuser("Pick a table group please : ")
		##TODO test if userchoice is valid
		return userchoice

	def choosetable(self, tablegroup="", message=""):
		"""
		after displaying to user tables known, ask to user to pick one.
	    returns the user's choice.
		"""
		dbinteract = TableGroupHandlerInteract(self.db_path)
		print("tablegroup = {}".format(tablegroup))
		tablelist = dbinteract.gettablelist(tablegroup)
		if message:
			print(message)
		if tablelist:
			self.printtablelist(tablelist)
		userchoice = self.askuser("Table number, or new table name, please : ")
		tablename = dbinteract._testtablename(userchoice, tablelist)
		return tablename

class TableGroupHandlerInteract:
	""" 
	
	Interact avec model.py

	"""
	def __init__(self, db_path):
		self.db_path = db_path
		self.tablegrouphandler = model.TableGroupHandler(db_path)

	def _testtablename(self, userchoice, tablelist):
		""" 
		the userchoice the user decided may be :
			* a number   : means that user wants to use a already known table
			* a name : without spaces, exotic characters (...) ; 
		function test that, and return the tablename chosen.
		"""
		if not userchoice:
			addprovider(self.db_path)
		elif userchoice.isdigit():
			i = int(userchoice) - 1
			try:
				tablename = tablelist[i][1]
				return tablename
			except IndexError:
				message = "Please use alpha numeric for table name"
				print(message)
				addprovider(self.db_path)
		elif userchoice.isalnum():
			return userchoice
		else:
			message = "Please use alpha numeric for table name"
			print(message)
			addprovider(self.db_path)

	def gettablegroups(self):
		""" 
		Print all kind of table group we can find in the database
		"""
		tablegrouplist = self.tablegrouphandler.gettablegrouplist()
		return tablegrouplist

	def gettablelist(self, tablegroup):
		""" 
		after displaying to user tables known, ask to user to pick one.
		returns the user's choice.
		"""
		print("searching in metatable for tablegroup {}".format(tablegroup))
		tablelist = self.tablegrouphandler.gettablelist(tablegroup)
		return tablelist

class DbNavigate():
	pass

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
			preformat = usrint.askuser("url part introducing queryformat	: ")
			presymbol = usrint.askuser("url part introducing symbol		: ")
			providerinfo = ( name, baseurl, preformat, presymbol )
			providerinfos.append(providerinfo)
			addprvd = usrint.askuser("add an other provider ? y/n :	")
			if addprvd == "y":
				print("\n")
				interactuser()
			return providerinfos

		providerinfos = interactuser()
		return providerinfos

	print("adding new PROVIDER\n")
	print("select PROVIDER's table")
	message = "Which provider table do you want to use ?\n\
Most people will only need one provider's table. If you want to create a new \
table, just write its name please."
	providertable = usrint.choosetable(db_path, "provider", message)
	providerinfos = getproviderinfos()
	print("select SYMBOL's table")
	message = "Which SYMBOL table do you want to use ?\n\
Most people will only need one symbol's table. If you want to create a new \
table, just write its name please."
	symboltable = usrint.choosetable(db_path, "symbol")
	providerhandler = model.ProviderHandler(db_path, providertable, message)
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

def selectstuff(db_path):
	""" 
	select table from metatable

	"""
	usrint = UserInteract(db_path)

	message = ("Please select what kind of tables you want to navigate \
into")
	usrint.choosetablegroup(message)
	
#	usrint.choosetable(db_path, "", message)


def quit():
	""" """
	sys.exit(0)



