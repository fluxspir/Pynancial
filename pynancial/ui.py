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
		""" response = str("userinput") """
		userinteract = code.InteractiveConsole()
		response = userinteract.raw_input(message)
		return response

	def printtuple(self, tupletoprint):
		""" 
		print the table list :
				1   table_1
				2   table_2
		from tablelist [ ( 1, table_1 ), ... ]
		be careful : 1 = tablelist[0]
		"""
		for t in tupletoprint:
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
			self.printtuple(tablegrouplist)
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
			self.printtuple(tablelist)
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
		elif userchoice.isalnum() or userchoice.isspace():
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
		self.db_path = db_path
		self.ui = UserInteract(self.db_path)

	def _orderresponse(self, unorderedlist):
		""" 
		response = [ ("x"), ("y"), ]
		assign num to each tuple;
		return = ( ( 1: "x"),(2:"y"), ]
		"""
		response = []
		i = 0
		for t in unorderedlist:
			response.append((i, t[0]))
			i += 1
		return tuple(response)

	def _testuserchoice(self, userchoice, possibilities):
		""" 
		look if userchoice is valid
		"""
		if not userchoice:
			message =  "error : user didn't pick nothing"
			print(message)
			return
		elif userchoice.isdigit():
			i = int(userchoice) - 1
			try:
				definitivechoice = possibilities[i][1]
				return definitivechoice
			except IndexError:
				message = "Please pick a number that exist"
				return
		elif userchoice.isprintable():
			for choice in possibilities[1]:
				if userchoice == choice:
					return choice
				else:
					return

	def dataavailable(self):
		""" 
		list of colums from tables, for user to choose whatever he needs
		"""
		pass

	def choosefromcolumn(self, column="", message="", where="", pattern=""):
		"""
		after displaying to user 
		return "string"
		"""
		if not column:
			column = "*"
		columnresponse = self.getsomething(column)
		orderedcol = self._orderresponse(columnresponse)
		if orderedcol:
			self.ui.printtuple(orderedcol)
		userchoice = self.ui.askuser(message)
		testchoice = self._testuserchoice(userchoice, orderedcol)
		if not testchoice:
			self.choosefromcolumn(column, message)
		else:
			choice = testchoice
		return choice

	def getsomething(self, columns="", where="", pattern=""):
		""" 
		response = [ ( ), (), ]
		"""
		response = self.tablehandler.getsomething(columns, where, pattern)
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
		##TODO test if given name OK
		self.name = name

	def table(self):
		message = "Please select the table you want to navigate into"
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename

	def name(self):
		""" select name from providertable"""
		message = "Please select the provider you want to use	: "
		name = self.choosefromcolumn(("name",), message)
		return name
		
	def baseurl(self):
		baseurl = self.tablehandler.getsomething(("baseurl",), "name", \
												self.name)
		return baseurl[0][0]

	def presymbol(self):
		presymbol = self.tablehandler.getsomething(("presymbol",) , \
														"name", self.name)
		return presymbol[0][0]

	def preformat(self):
		preformat = self.tablehandler.getsomething(("preformat",) ,\
														"name", self.name )
		return preformat[0][0]

	def formattable(self):
		pass

	def getinfos(self, something=""):
		""" """
		url = self.baseurl()
		preformat = self.preformat()
		presymbol = self.presymbol()
		selectedstuff = (("name", self.name),("baseurl", url), ("presymbol", \
										presymbol), ("preformat", preformat ))
		return selectedstuff
		

class Symbol(TableHandlerInteract):
	def __init__(self, db_path, table="", provider="", valuecode=""):
		self.db_path = db_path
		self.tablegroup = "symbol"
		self.ui = UserInteract(self.db_path)
		if not table:
			table = self.table()
		self.table = table
		self.tablehandler = model.SymbolHandler(self.db_path, self.table)
			

	def table(self):
		message = "Please select the table you want to navigate into"
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename

	def codename(self):
		""" Value.code() and .name()  ;  return (code , name)"""
		value = Value(self.db_path)
		valuecode = value.code()
		valuename = value.name()
		codename = ( valuecode, valuename)
		return codename
	
	def provider(self):
		""" Provider.name() """
		prvd = Provider(self.db_path)
		providername = prvd.name()
		return providername
		
	def getsymbol(self):
		"""
		select _code() from tokentable 
			where "name"=(_provider)
		return : symbol = (
		"""
		codename = self.codename()
		provider = self.provider()
		symbols = self.getsomething(codename[0], "name", self.provider)
		symbol = symbols[0][0]
		return (symbol)

	def getinfos(self):
		provider = self.provider
		name = self.codename[1]
		code = self.codename[0]
		symbol = self.getsymbol()
		pass

class Value(TableHandlerInteract):
	""" 
	
	Common informations that share chattels, as code, name, location.
	Value may be "stock", "index", "futures", "...???"
	
	"""
	def __init__(self, db_path, tablegroup ="", table=""):
		self.db_path = db_path
		self.ui = UserInteract(self.db_path)
		if not tablegroup:
			groupsavailable = ( (0, "stock"), (1, "index") )
			message = "What kind of values you want to see symbols ?"
			self.ui.printtuple(groupsavailable)
			userchoice = self.ui.askuser(message)
			dbinteract = TableGroupHandlerInteract(self.db_path)
			tablegroup = dbinteract._testtablename(userchoice, groupsavailable)
		self.tablegroup = tablegroup
		if not table:
			table = self.table()
		self.table = table


	def table(self):
		message = "Please select the table you want to navigate into"
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename


	def code(self, name="", message=""):
		""" select code from the stock/index/... table"""
		if not name:
			name = self.choosefromcolumn(("name", "code" ), message)
			self.code(name)
		else:
			getcode = self.tablehandler.getsomething(("code",),"name", name)
			code = getcode[0][0]
		return code
		
	def name(self, code="", message=""):
		""" 
		select name from value table 
		name = [ ( "name" ), ]
		"""
		if not code:
			name = self.choosefromcolumn(("name",), message)
		else:
			getname = self.tablehandler.getsomething(("name",), "code", code)
			name = getname[0][0]
		return name

	def codename(self, message=""):
		code = self.code()
		name = self.name()
		codename (self.code, self.name)
		return codename

	def location(self, code="", message=""):
		"""select location where "code" = code"""
		if not code:
			location = self.choosefromcolumn(("location",), message)
		else:
			getlocation = self.getsomething(("location",), "code", code)
			location = getlocation[0][0]
		return location

class Stock(Value):
	""" 

	A stock belongs to the database.
	It has a stock international code : FRxxxxxxxxxx (10 "x")
	The stock name is at first choosen by the user.
		An implementation could be to take the name of yahoo-format long_name
	The stock location is the market place (stock exchange) where you may find
		this stock (exemple : NYSE, NASDAQ, PARIS...)
	
	"""
	def __init__(self, db_path, table="", code="", name=""):
		self.db_path = db_path
		self.tablegroup = "stock"
		Value.__init__(self, db_path, self.tablegroup, table)
		self.tablehandler = model.StockHandler(self.db_path, self.table)
		if not code:
			if not name:
				message = "Please select the stock you want to use : "
				name = self.name( "" , message)
				code = self.code(name)
			code = self.code(name)
		self.code = code

	def getinfos(self):
		"""
		infos =( ("db_path", self.db_path), ("table", self.table ),("code",\
			self.code), ("name" self.name), ("location", self.location) )
		"""
		infos =( ("db_path", self.db_path), ("table", self.table ), ("code",\
				self.code), ("name", self.name(self.code)), \
				("location", self.location(self.code)) )
		return infos 

class Index(Value):
	""" """
	def __init__(self, db_path, table="", code="", name=""):
		self.db_puth = db_path
		self.tablegroup = "index"
		Value.__init__(self, db_path, self.tablegroup, table)
		self.ui = UserInteract(self.db_path)
		self.tablehandler = model.IndexHandler(self.db_path, self.table)
		if not code:
			if not name:
				message = "Please select the index you want to use : "
				name = self.name( "" , message)
				code = self.code(name)
			code = self.code(name)
		self.code = code

	def valuesindexed(self):
		""" 
		return ( "stock1", "stock2", "stock3", ) 
		needs a database
		"""
		#TODO
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
	providertable = usrint.choosetable("provider", message)
	providerinfos = getproviderinfos()
	print("select SYMBOL's table")
	message = "Which SYMBOL table do you want to use ?\n\
Most people will only need one symbol's table. If you want to create a new \
table, just write its name please."
	symboltable = usrint.choosetable("symbol", message)
	providerhandler = model.ProviderHandler(db_path, providertable)
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

def addsymbol(db_path, newsymbols=[]):
	""" 
	[ ( provider, value, symbol ), ]
	"""
	ursint = UserInteract(db_path)
	if newsymbols:
		pass

	provider = Provider(db_path)
	message = "To which kind of value will you add the symbol ? "
	groups ("stock", "index")
	tablegroup = usrint.choosetablegroup(message, groups)
	if tablegroup == "stock":
		value = Stock(db_path)
	elif tablegroup == "index":
		value = Index(db_path)
	providername = provider.name()
	valuecode = value.code()
	valuename = value.name()
	symbol = usrint.askuser("What is the {}' symbol for the value \
{}	: ".format(providername, valuename))
	##TODO
##	symbolhandler = model.Symbol

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

	def userprint(stufftoprint):
		""" 
		print format of tuples ("name"  :  "value")
		"""
		for r in stufftoprint:
			print("{}	:	{}".format(r[0], r[1]))
		print("\n")

	if tablegroup == "provider":
		provider = Provider(db_path)
		stuffselected = provider.getinfos()
		userprint(stuffselected)
		return stuffselected

	elif tablegroup == "symbol":
		symbol = Symbol(db_path)
		stuffselected = symbol.getsymbol()
		userprint(stuffselected)
		return stuffselected

	elif tablegroup == "stock":
		stock = Stock(db_path)
		stuffselected = stock.getinfos()
		userprint(stuffselected)
		return stuffselected

	elif tablegroup == "index":
		index = Index(db_path)
		stuffselected = index.selectvalue()
		userprint(stuffselected)
		return stuffselected
	else:
		return
	return stuffselected
	
def quit():
	""" """
	sys.exit(0)



