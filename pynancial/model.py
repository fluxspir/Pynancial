#!/usr/bin/python3
# (c) Franck LABADILLE
# LICENCE BSD
# 20110127
# Pynancial.model
#

"""


"""
import pynancial.db as db
import pdb

class TableGroupHandler:
	"""
	
	We have several group of tables in the database : 
		* The "format" ones		:(usually : only one)
		* The "provider" ones	:(usually : only one)
		* The "symbol" ones	:(usually : only one)
		* The "stock" ones : (may be several)
		* The "index" ones : (may be several)
	
	One unique table, the metatable, will connect table-name with table-group
	
	"""
	def __init__(self, db_path):
		self.db_path = db_path

	def gettablegrouplist(self):
		""" 
		return tablegrouplist : list tuples which assignate
		tablegrouplist = [ (number , tablegroup), ]
		"""
		def checkalreadyknowngroup(tablegroup, tablegrouplist):
			for tgp in tablegrouplist:
				if t[0] in tgp[1]:
					return
			return True
		
		tablegrouplist = []
		dbhandler = db.DbHandler(self.db_path)
		groupsavailable = dbhandler.gettablegrouplist()
		if groupsavailable:
			i = 0 
			for t in groupsavailable:
				if not tablegrouplist:
					tablegrouplist.append((i, t[0]))
					i += 1
				else:
					check = checkalreadyknowngroup(t, tablegrouplist)
					if check:
						tablegrouplist.append((i, t[0]))
						i += 1
		return tablegrouplist

	def gettablelist(self, tablegroup=""):
		""" 
		return tablelist : a list of tuples to assignate 
			[	(number  ,  tablename) , ]
		
		"""
		tablelist = []
		dbhandler = db.DbHandler(self.db_path)
		tablesindb = dbhandler.gettableslist(tablegroup)
		if tablesindb:
			i = 0
			for t in tablesindb:
				tablelist.append((i, t[0]))
				i += 1
		return tablelist

	

class ProviderHandler(TableGroupHandler):
	"""

	METHODS
		checkmetatable()

	provider database :
		* baseurl
		* presymbol
		* symbols
		* pre_format
		
	"""
	def __init__(self, db_path, table):
		self.db_path = db_path
		self.table = table
		self.dbprovider = db.ProviderDbHandler(self.db_path, self.table)

	def addnewprovider(self, providerinfos, symboltable):
		""" """
		prvdmessage = self.dbprovider.addprovider(providerinfos, symboltable)
		print(prvdmessage)

	def addsymbol(self, providername, symboltable, symbolsfortokens):
		"""
		add provider_symbols for tokens
		symbolsfortokens = [ ( " tokencode ", "providersymbol" ),
							( "FRxxxxxxxx" , "BNP.PA" ) , ]
		insert into symboltable ( "tokencode" ) value (providersymbol) \
		where providername = 'providername'
		"""

	def addnewproviderformat(self, providername, formats):
		"""
		add to provider "providername" the format
		formats = [ ( "formatname" , "formatprovidercode" ) ,
					( "lname" , "l" ) ,		]
		insert into providertable (formatname) value formatprovidercode\
		where providername = 'providername'
		"""

	def addformattype(self, formattable, formatinfos):
		"""
		alter providertable with formatcolums ;
		insert into formattable [ ( "formatname" , "explicit format name"), ]
		return 
		"""
		response  = self.dbprovider.addformat(formattable, formatinfos)
		return response

	def updateformat(self, formattable, urlformats):
		""" 
			urlformats = ( ("providername", "shortname", "urlformatstring" ) )
		insert/replace into PROVIDERTABLE values ("providername","shortname",\
															"urlformatstring" )
		return = if False : everything want well
				true = urlformatreject  = [ ( urlformats[x]), ]
		"""
		response = self.dbprovider.updateformat(formattable, urlformats)
		return response

	def getsomething(self, columns="", where="", name=""):
		""" """
		response = self.dbprovider.getsomething(columns, where, name)
		return response

class StockHandler(TableGroupHandler):
	"""
	
	"FR", "US" , "mystocks"
	database stock
		* tokencode "internationnal normalized code (FRxxxxxxx)" primary key
		* common name
		* location
	
	METHOD:
		addstock(stockinfos)
			stockinfos = [ ( stock int code, name, location ),
							( "USxxxxxxx", general motor", "NYSE" ) ]

		getstockcode(pattern)
		
	"""

	def __init__(self, db_path, table):
		self.db_path = db_path
		self.table = table
		self.dbstock = db.StockDbHandler(self.db_path, self.table)
		
	def addstock(self, stockinfos, symboltable):
		addmessage = self.dbstock.addnewstock(stockinfos, symboltable)
		print(addmessage)

	def getsomething(self, columns="", where="", name=""):
		""" """
		response = self.dbstock.getsomething(columns, where, name)
		return response

	def getstocklist(self):
		"""
		return : ( ( code, name ) )
		"""
		


class IndexHandler(TableGroupHandler):
	"""
	
	"dj30", "nasdaq100", "cac40" 
	database indexes
		* "INCode (FRxxxxxxxx)" primary key
		* common name
		* location
		* alter with provider_codes

	"""
	def __init__(self, db_path, table):
		self.db_path = db_path
		self.table = table
		self.dbindex = IndexDbHandler(self.db_path, self.table)

	def addindex(self, indexinfos, symboltable):
		addmessage = self.dbindex.addnewindex(indexinfos, symboltable)
		print(addmessage)

	def getsomething(self, columns="", where="", name=""):
		""" """
		response = self.dbindex.getsomething(columns, where, name)
		return response

class SymbolHandler(TableGroupHandler):
	def __init__(self, db_path, table):
		self.db_path = db_path
		self.table = table
		self.dbsymbol = db.SymbolDbHandler(self.db_path, self.table)

	def addsymbol(self, newsymbols):
		""" 
		newsymbols = [ ( prvd , value, symbol), ]
		insert into symboltable (codecolumn,) values ( symbol, )
		where "provider" = (name,)
		if everything ok, return false
		otherwise, return list of symbols refused
		"""
		verifyadd = self.dbsymbol.addsymbol(newsymbols)
		return verifyadd

	def getsomething(self, columns="", where="", name=""):
		""" """
		response = self.dbsymbol.getsomething(columns, where, name)
		return response
	
class FormatHandler:
	""" 
	The format adding passed throught ProviderHandler, as providertable is
	altered by this process.

	"""
	def __init__(self, db_path, table):
		self.db_path = db_path
		self.table = table
		self.dbformat = db.FormatDbHandler(self.db_path, self.table)
	
	def getsomething(self, columns="", where="", name=""):
		""" """
		response = self.dbformat.getsomething(columns, where, name)
		return response

