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
		tablegroup = dbinteract._testtablename(userchoice, tablegrouplist)
		##TODO test if userchoice is valid
		return tablegroup

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

class TableHandlerInteract:
	""" """
	def __init__(self, db_path):
		pass

	def dataavailable(self):
		""" 
		list of collums from tables, for user to choose whatever he needs
		"""
		pass

	def choosefromcollum(self, collum="", message=""):
		"""
		after displaying to user 
		"""
		if not collum:
			collum = "*"
		if message:
			print(message)
		collumresponse = self.getsomething(collum)
		print(collumresponse)
		print("todo")
		quit()


	def getsomething(self, collumns="", where="", pattern=""):
		""" """
		response = self.tablehandler.getsomething(collumns, where, pattern)
		return response


class Provider(TableHandlerInteract):
	""" 

	the provider table is the database table where our providers are.
	the provider name is chosen by the user
	the provider baseurl is the part of the url that never changes, beginning
		with "http:// "
	the provider presymbol is the url part that will introduce the symbol that 
		represent the entity (stock...) we're looking for.
	the provider preformat is the url part that will introduce the 
		"formatquery" which tells the providers infos we want for symbol chosen

	"""
	def __init__(self, db_path, table="", name=""):
		self.db_path = db_path
		self.tablegroup = "provider"
		self.ui = UserInteract(self.db_path)
		if not table:
			table = self.table()
		self.table = table
		self.tablehandler = model.ProviderHandler(self.db_path, self.table)
		if not name:
			name = self.name()
		self.name = name

	def table(self):
		message = ("Please select the table you want to navigate into")
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename

	def name(self):
		""" select name from providertable"""
		message = ("Please select the provider you want to use")
		name = self.choosefromcollum(("name",), message)
		return name
		
	def baseurl(self):
		baseurl = self.tablehandler.getsomething(("baseurl",), "name", \
												self.name)
		return baseurl

	def presymbol(self):
		presymbol = self.providerhandler.getsomething(("presymbol",) , \
														"name", self.name)
		return presymbol

	def preformat(self):
		message = "Select format"
		print(message)
		print("TODO")
		return preformat

	def formattable(self):
		pass

	def selectfromprovider(self, something=""):
		""" """
		##TODO TOCHANGE
		url = self.baseurl()
		selectedstuff = (self.name, url)
		return selectedstuff
		

class Symbol():
	def possessioncode(self):
		pass

class Possession(Symbol):
	""" """
	def code(self):
		pass
	def name(self):
		pass
	def location(self):
		pass

class Stock(Possession):
	""" """

class Index(Possession):
	""" """
	def valuesindexed(self):
		pass

class UrlBuilder():
	""" """
	def __init__(self):
		pass
	def possession(self):
		pass
	def provider(self):
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
			preformat = usrint.askuser("url part introducing queryformat	\
: ")
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

def addstock(db_path):
	""" """
	usrint = UserInteract(db_path)

	def getstockinfos():
		"""
		tablelist = [ ( number(start at 1) , tablename ) ]
		"""
		stockinfos = []
		def interactuser():
			code = usrint.askuser("Stock International Code (USxxxxxxxxxx) : ")
			name = usrint.askuser("Compagny name	: ")
			location = usrint.askuser("Stock Exchange	: ")
			stockinfo = (code, name, location)
			stockinfos.append(stockinfo)
			addother = usrint.askuser("add an other stock ? y/n :	")
			if addother == "y":
				print("\n")
				interactuser()
			return stockinfos

		stockinfos = interactuser()
		return stockinfos

	print("adding new STOCK\n")
	print("select STOCK table")
	message = "Which stock table do you want to use ?\n\
Some people will use several stock's table. \
You could that way create stocks tables by Type (environment, healcare,...), \
locations, whateever you want.\n\
If you want to create a new table, just write its name please."
	stocktable = usrint.choosetable("stock", message)
	stockinfos = getstockinfos()
	stockhandler = model.StockHandler(db_path, stocktable)
	message = "Which SYMBOL table do you want to use for table {} ?"\
	.format(stocktable)
	symboltable = usrint.choosetable("symbol", message)
	stockhandler.addstock(stockinfos, symboltable)


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
	select anything from tables
	return the stuff selected
	"""
	usrint = UserInteract(db_path)
	message = ("Please select what kind of tables you want to navigate \
into")
	tablegroup = usrint.choosetablegroup(message)

	if tablegroup == "provider":
		provider = Provider(db_path)
		print("yo")
		stuffselected = provider.selectfromprovider()
		print("stuff selected : {}".format(stuffselected))
		return stuffselected

	elif tablegroup == "symbol":
		pass
	elif tablegroup == "stock":
		pass
	elif tablegroup == "index":
		pass
	else:
		return
	return stuffselected
	
def quit():
	""" """
	sys.exit(0)



