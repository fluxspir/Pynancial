
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
import re

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
	    returns the table the user chose.
		"""
		dbinteract = TableGroupHandlerInteract(self.db_path)
		print("tablegroup = {}".format(tablegroup))
		tablelist = dbinteract.gettablelist(tablegroup)
		if message:
			print(message)
		if tablelist:
			self.printtuple(tablelist)
		userchoice = self.askuser("Table number, or new table name, please : ")
		if not userchoice:
			self.choosetable(tablegroup, message)
		tablename = dbinteract._testtablename(userchoice, tablelist)
		if not tablename:
			self.choosetable(tablegroup, message)
		return tablename

	def parseresponse(self, userinput, tupplechoices):
		"""
		userinput : string of numbers and words. 
			at least,   space separated (can add "commas, or anything else")

		tupplechoices = ( ( int_1, "name" , "code"), ( 2, "name2", "code"), ]

		le but de la fonction :
			creer une liste de values (result);


		userinput : * si c'est un nombre : 
				result = la "value finale" = tupplechoice[userinput - 1][1]
						: on veut le "name" correspondant au numéro rentré.
					* si c'est alphanum:
				result.append(recupération des "noms" contenant cette string)

				result évite les résultats redondants

		return result
		"""
		userlist = []
		i = 0
		splittedlist = re.split(r"[\s,;]+", userinput)
		for elem in splittedlist:
			elem = elem.strip()
			def testalreadyknownentries(newentry, oldentries):
				""" 
				newentry : string to test
				oldentries : list of user choices already validated
				"""
				if newentry not in oldentries:
					oldentries.append(newentry)
				return oldentries
					
			if elem.isdigit():
				try:
					elem = tupplechoices[int(elem) - 1][2]
					userlist = testalreadyknownentries(elem, userlist)
				except IndexError:
					print("number entry {} erroneus ; ignoring".format(elem))

			elif elem.isprintable():
				## aller attraper dans la tupplechoices[*][1]
				## tous les "names" qui contiennent la string elem
				lowelem = elem.lower()
				if lowelem.startswith("^"):
					lowelem = "".join(lowelem.split("^"))
					for possibility in tupplechoices:
						if possibility[1].lower().startswith(str(lowelem)):
							userlist = testalreadyknownentries(possibility[2],\
																userlist)
				elif lowelem.endswith("$"):
					lowelem = "".join(lowelem.split("$"))
					for possibility in tupplechoices:
						if possibility[1].lower().endswith(str(lowelem)):
							userlist = testalreadyknownentries(possibility[2],\
																	userlist)
				else:
					for possibility in tupplechoices:
						if not possibility[1].lower().find(lowelem) == -1:
							userlist = testalreadyknownentries(possibility[2],\
																	userlist)
			else:
				print("wrong value ; ignoring")
		return userlist

	def multchoicesvalues(self, tablegroup="", burnstate=""):
		"""
		SHOULDN'T BE USED WITH "ADD_SOMETHING() functions BECAUSE OF THE STEPS 
		SKIPPING WHEN ONLY A SINGLE TABLEGROUP CHOICE

		multiple choices values
		navigate throught selections

		if burnstate == "y"
		drops ways without propositions and don't ask when only one choice 
		possible.
		tablegroup = ( "", "",)

		return list of codes 
		"""
		
		tablegrouphandler = TableGroupHandlerInteract(self.db_path)
		handler = model.TableGroupHandler(self.db_path)
		## get the tablegroup
		if not tablegroup:
			tablegroup = self.choosetablegroup()
		else:
			listgroup = []
			if len(tablegroup) > 1:
				i = 0
				for g in tablegroup:
					listgroup.append((i, g))
					i += 1
				self.printtuple(listgroup)
				userchoice = self.askuser("Pick a table group please : ")
				tablegroup = tablegrouphandler._testtablename(userchoice, \
																	listgroup)
			else:
				## BE CAREFUL WITH ADD MODE
				tablegroup = tablegroup[0]

		try:
			tablelist = handler.gettablelist(tablegroup)
		except :
			print("no such tablegroup {}.".format(tablegroup))
			self.multchoicesvalues("", burnstate)

		self.printtuple(tablelist)
		response = self.askuser("Which table	: ")
		pdb.set_trace()
		if response.isdigit():
			table = tablelist[int(response) - 1][1]
		else:
			self.multchoicevalues(tablegroup, burnstate)

		if tablegroup == "stock":
			tablehandler = model.StockHandler(self.db_path, table)
		elif tablegroup == "index":
			tablehandler = model.StockHandler(self.db_path, table)
	
		entries = tablehandler.getsomething(("code", "name"))
		entrieslist = []
		i = 0
		for entry in entries:
			entrieslist.append((i, entry[1], entry[0]))
			i += 1
		self.printtuple(entrieslist)
		userchoice = self.askuser("Which values, comma separated, do you want \
to use ?\n\
you can pick number, \n\
use  ^lal   to select all values beginning by 'lal'\n\
use lal$	to select all values finishing by 'lal'\n\
use   lal	to select all values contening 'lal'\n")
		userlist = self.parseresponse(userchoice, entrieslist)
		return userlist

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
			return False
		elif userchoice.isdigit():
			i = int(userchoice) - 1
			try:
				tablename = tablelist[i][1]
				return tablename
			except IndexError:
				message = "Please use alpha numeric for table name"
				print(message)
				return False
		elif userchoice.isalnum():       # or userchoice.isspace():(not needed)
			return userchoice
		else:
			message = "Please use alpha numeric for table name"
			print(message)
			return False

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
		unorderedlist = [ ("x"), ("y"), ]
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

	def multiplevaluesselector(self, column="", message="", where="", 
															pattern=""):
		""" 
		display to user a list of  : num - name
		user pick numbers from list
		verify if only digits where chosen
		return a list of value.code 
		"""
		def makelist(self, unordered):
			""" 
			unordered = ( ( , ) , ( , ) )
			"""
			orderedlist = []
			i = 0
			for t in unordered:
				orderedlist.append((i, t[1]))
			return orderedlist

		if not column:
			column = (code, name)
		if not message:
			message = "pick numbers, comma separated\n"
		columnresponse = self.getsomething(column)

	def getsomething(self, columns="", where="", pattern=""):
		"""
		select columns from self.table where where=pattern
		columns = ( "col1", "col2", )
		where = "string"
		pattern = (maybe string now) should be : ( pat1, pat2, )
		response = [ (), (), ]
		"""
		response = self.tablehandler.getsomething(columns, where, pattern)
		return response

	def addformat(self, formattable, formatinfos):
		"""
		should be (at first ?) only usable by Provider()
		Provider() is the only class with method formatable(self)

		insert into formattable formatinfos
		and alter providertable with "colname" (formatinfos[n][0])
		formatinfos = [ ( "colname", "explicit name") , ]
		"""
		response = self.tablehandler.addformattype(formattable, formatinfos)
		return response

	def getformat(self, formattable):
		"""
		formatteble = "formattable"
		return ( ("shortname","long name"), )
		"""
		tablehandler = model.FormatHandler(self.db_path, formattable)
		response = tablehandler.getsomething( ("columnname", "explicitname") )
		return response

	def chooseformat(self, formattable, formatknown):
		""" 
		column = [("shortname", "long name"),]
		will use shortname for dbinteract
		will use "long name" for user interact

		like choosefromcolumn, except for formattable
		"""
		formattablehandler = model.FormatHandler(self.db_path, formattable)
		column = []
		uiname = []
		for c in formatknown:
			column.append((c[0],))
			uiname.append((c[1],))			
		orderedname = self._orderresponse(uiname)
		orderedcol = self._orderresponse(column)
		if orderedname:
			self.ui.printtuple(orderedname)
		message = "choose format name please	: "
		userchoice = self.ui.askuser(message)
		pdb.set_trace()
		testchoice = self._testuserchoice(userchoice, orderedcol)
		if not testchoice:
			self.chooseformat(formattable, columns, message)
		else:
			choice = testchoice
		return choice

	def updateformat(self, formattable, urlformats):
		"""
		formattable = "formattable"
		urlformats = ( ("providername", "shortname", "urlformatstring" , ) )
			verify in (urlformat) if urlformat[1]
		insert/replace into PROVIDERTABLE values ("providername","shortname",\
															"urlformatstring" )
		return : response false : ok
				else : response = [ (urlformat[x]), ]
		"""
		response = self.tablehandler.updateformat(formattable, urlformats)
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
#		if not name:
#			name = self.name()
#		self.name = name

	def table(self):
		message = "Please select the table you want to navigate into	: "
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename

	def name(self):
		""" select name from providertable"""
		message = "Please select the provider you want to use	: "
		name = self.choosefromcolumn(("providername",), message)
		return name
		
	def baseurl(self, name=""):
		if not name:
			name = self.name()
		baseurl = self.tablehandler.getsomething(("baseurl",), "providername",\
																		name)
		return baseurl[0][0]

	def presymbol(self, name=""):
		if not name:
			name = self.name()
		presymbol = self.tablehandler.getsomething(("presymbol",), \
													"providername", name)
		return presymbol[0][0]

	def preformat(self, name=""):
		if not name:
			name = self.name()
		preformat = self.tablehandler.getsomething(("preformat",) ,\
													"providername", name)
		return preformat[0][0]

	def getinfos(self, name=""):
		""" 
		return = ( ( "name", self.name ),
					("baseurl", url  ),
					("presymbol", presymbol ),
					(preformat , preformat), )
		"""
		if not name:
			name = self.name()
		url = self.baseurl(name)
		preformat = self.preformat(name)
		presymbol = self.presymbol(name)
		selectedstuff = (("providername", name),("baseurl", url), \
					("presymbol", presymbol), ("preformat", preformat ))
		return selectedstuff

	def formattable(self):
		message = " Please select the format table	: "
		formattable = self.ui.choosetable("format", message)
		return formattable
		
	def formatinfos(self, formattable=""):
		"""
		return = ( ( "shortname", "long name" ), )
		"""
		if not formattable:
			formattable = self.formattable()
		selectedstuff = self.getformat(formattable)
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
		valuename = value.name(valuecode)
		codename = ( valuecode, valuename)
		return codename
	
	def provider(self):
		""" Provider.name() """
		prvd = Provider(self.db_path)
		providername = prvd.name()
		return providername
		
	def getsymbol(self, provider="", code=""):
		"""
		select _code() from tokentable 
			where "providername"=(_provider)
		return : symbol = ""
		"""
		if not code:
			codename = self.codename()
			code = codename[0]
		if not provider:
			provider = self.provider()
		symbols = self.getsomething((code,), "provider", provider)
		symbol = symbols[0][0]
		return symbol

	def getinfos(self):
		provider = self.provider()
		codename = self.codename()
		name = codename[1]
		code = codename[0]
		symbol = self.getsymbol(provider, code)
		infos = (("name", name), ("code", code), ("symbol", symbol))
		return infos

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
		if self.tablegroup == "stock":
			self.tablehandler = model.StockHandler(self.db_path, self.table)
		elif self.tablegroup == "index":
			self.tablehandler = model.IndexHandler(self.db_path, self.table)
		else:
			print("No tablegroup ; expect errors because no tablehandler \
could be set.")

	def table(self):
		message = "Please select the table you want to navigate into"
		tablename = self.ui.choosetable(self.tablegroup, message)
		return tablename


	def code(self, name="", message=""):
		""" select code from the stock/index/... table"""
		if not name:
			name = self.choosefromcolumn(("name", "code" ), message)
			code = self.code(name)
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
				("locate", self.location(self.code)) )
		return infos 

class Index(Value):
	""" """
	def __init__(self, db_path, table="", code="", name=""):
		self.db_puth = db_path
		self.tablegroup = "index"
		Value.__init__(self, db_path, self.tablegroup, table)
		self.ui = UserInteract(self.db_path)
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
		needs a databas
		e
		"""
		#TODO
		pass

class UrlBuilder():
	""" """
	def __init__(self, db_path):
		self.db_path = db_path
		self.ui = UserInteract(self.db_path)

	def _possessions(self, table=""):
		"""
		code = ( code1, code2,)
		return symbols = 
		"""
		codes = []
		codelist = self.ui.multchoicesvalues(("stock","index"), "")
		return codelist

	def _providerinfos(self, table="", name=""):
		"""
		return infos = ("name", "baseurl" , "preformat", "presymbol")
		"""
		providertable = self.ui.choosetable("provider")
		provider = Provider(self.db_path, providertable)
		providerinfos = provider.getinfos(name)
		providername = providerinfos[0][1]
		baseurl = providerinfos[1][1]
		presymbol = providerinfos[2][1]
		preformat = providerinfos[3][1]
		formatinfos = provider.formatinfos()
		queryformat = self.ui.multchoicesvalues(("format",), "yes")
		infos = (providername, baseurl, preformat, presymbol, queryformat)
		pdb.set_trace()
		return infos
	
	def _providerformat(self, table="", name=""):
		""" 
		return = ( 
		"""
#		formathandler = Provider, self.db_path, 

	def geturl(self, valuetable="", valuecodes="", providertable="", 
														providername=""):
		"""
		valuecode = list of codes
		"""
		def multiple(outlist=""):
			if not outlist:
				outlist = []
			##get the list of codes the user wants.
			codelist = self._possessions(valuetable)
			for code in codelist:
				outlist.append(code)

			addother = self.ui.askuser("Add others ?	y/n	")
			if addother == "y":
				multiple(outlist)
			return outlist
		
		## codelist
		if not valuecodes:
			codes = multiple()
		else:
			codes = valuecodes

		## provider
		(providername, baseurl, preformat, presymbol, queryformat) = \
							self._providerinfos(providertable, providername)

		## get symbols for codes
		symbol = Symbol(self.db_path)
		symbolinfos = symbol.getsymbol(providername, codes[0])

		## get the queryformats the user needs
		## URL to return
		url = baseurl + preformat + queryformat + presymbol + symbols
		print(url)
		quit()
		return url

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
	if not providertable:
		addprovider(db_path)
	providerinfos = getproviderinfos()
	print("select SYMBOL's table")
	message = "Which SYMBOL table do you want to use ?\n\
Most people will only need one symbol's table. If you want to create a new \
table, just write its name please."
	symboltable = usrint.choosetable("symbol", message)
	if not symboltable:
		addprovider(db_path)
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
	if not stocktable:
		addstock(db_path)
	stockinfos = getstockinfos()
	stockhandler = model.StockHandler(db_path, stocktable)
	message = "Which SYMBOL table do you want to use for table {} ?"\
	.format(stocktable)
	symboltable = usrint.choosetable("symbol", message)
	if not symboltable:
		addstock(db_path)
	stockhandler.addstock(stockinfos, symboltable)

def addindex():
	""" """
	pass

def addsymbol(db_path, newsymbols=[]):
	""" 
	[ ( provider, value, symbol ), ]
	"""
	usrint = UserInteract(db_path)
	if newsymbols:
		pass
	message = "Please choose symbol table"
	symboltable = usrint.choosetable("symbol", message)
	if not symboltable:
		return
	provider = Provider(db_path)
	message = "To which kind of value will you add the symbol \n\
1 : stock\n\
2 : index\n"
	usertablechoice = usrint.askuser(message)
	message = "Choose value please"
	if usertablechoice == "1":
		userchoice = "stock"
		value = Stock(db_path)
	elif usertablechoice == "2":
		userchoice = " index"
		value = Index(db_path)
	else:
		print("wrongly written value")
		addsymbol(db_path)
	valuename = value.name(value.code)
	providername = provider.name()
	symbol = usrint.askuser("What is the {}' symbol for the value \
{}	: ".format(providername, valuename))
	symbolhandler = model.SymbolHandler(db_path, symboltable)
	verifyadd = symbolhandler.addsymbol([(providername, value.code, symbol),])
	if not verifyadd:
		print("add symbol OK")
	else:
		print("these values weren't added :")
		for r in verifyadd:
			print("{}\t\t{}\t\t{}\n" \
				.format(verifyadd[0], verifyadd[1], verify[2]))

def addformat(db_path):
	""" 
	should add   formatinfos=""  above in definition
	"""
	usrint = UserInteract(db_path)

	def getformatinfos():
		""" 
		formatinfos = [ ( "columnname" , "explicit name" ), 
					( "shortnamewithoutspace", "long name to help" ),]
		"""
		formatinfos = []
		def interactuser():
			colname = usrint.askuser("shortnamewithoutspace	: ")
			explname = usrint.askuser("long name to help	: ")
			formatinfo = (colname, explname)
			formatinfos.append(formatinfo)
			addother = usrint.askuser("add an other format ? y/n : ")
			if addother == "y":
				interactuser()
			return formatinfos
		formatinfos = interactuser()
		return formatinfos

	print("Adding new format kind\n")
	print("Select format table\n")
	message = "Which format table do you want to use ?\n\
If you want to create a new table, just write its name please."
	formattable = usrint.choosetable("format", message)
	if not formattable:
		return
	formatinfos = getformatinfos()
	provider = Provider(db_path)
	provider.addformat(formattable, formatinfos)

def updateformat(db_path, providertable="", formattable="", urlformats=""):
	"""
	newformats = [ ( "providername","columnname","format" ), ]
	insert the providerformatcode.
	"""
	usrint = UserInteract(db_path)
	provider = Provider(db_path, providertable)
	print("Inserting new formatstring")
	if not formattable:
		message = "Please choose the format table your formatsymbol \
belongs to : "
		formattable = usrint.choosetable("format", message)

	def geturlformats():
		urlformats = []
		def interactuser():
			message = "choose provider"
			providername = provider.name()
			message = "choose format name"
			formatknown = provider.getformat(formattable)
			columnname = provider.chooseformat(formattable, formatknown)
			formatstring = usrint.askuser("format string please	: ")
			urlformat = (providername, columnname, formatstring)
			urlformats.append(urlformat)
			addother = usrint.askuser("add an other formatstring ? y/n	: ")
			if addother == "y":
				interactuser()

		interactuser()
		return urlformats

	if not urlformats:
		urlformats = geturlformats()

	response = provider.updateformat(formattable, urlformats)

	if not response:
		print("OK")
		return
	else:
		print("these urlformats weren't added")
		print(response)
		return response
			
def selectstuff(db_path):
	""" 
	select anything from tables
	return the stuff selected
	"""
	usrint = UserInteract(db_path)
	message = "Please select what kind of tables you want to navigate \
into"
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
		stuffselected = symbol.getinfos()
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

	elif tablegroup == "format":
		provider = Provider(db_path)
		stuffselected = provider.formatinfos()
		userprint(stuffselected)
		return stuffselected
	else:
		return
	return stuffselected

def buildurl(db_path):
	"""
	will construct the url
	"""
	usrint = UserInteract(db_path)
	urlbuilder = UrlBuilder(db_path)
	url = urlbuilder.geturl()
	print(url)
	return url

def quit():
	""" """
	sys.exit(0)

