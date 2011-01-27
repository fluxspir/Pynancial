#!/usr/bin/python3
# (c) Franck LABADILLE
# LICENCE BSD
# 20110127
# Pynancial.model
#

"""


"""
import pynancial.db as db

class TableGroupHandler():
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

	def gettablelist(self, tablegroup=""):
		""" 
		return a tuple with name of each known table in the 
		"""
		tablelist = []
		dbhandler = db.DBHandler(db_path)
		tablesindb = dbhandler.gettablelist(tablegroup)
		i = 1
		for t in tablesindb:
			tablelist.append((i, t))
			i++
		return tablelist

	def verifytableexists(self, tablename):
		""" 
		apparently never called :/
		"""
		dbhandler = db.DBHandler(db_path)
		tableindb = dbhandler.gettablename(tablename)
		if tableindb:
			return tableindb
		else:
			return


class ProviderHandler:
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
		alter providertable with formatcollums ;
		insert into formattable [ ( "formatname" , "explicit format name"), ]
		"""
		self.formattable = formattable
		self.addformattype = db.DBProvider(self.db_path, self.table)
		addformattypemessage  = self.addformattype.addformat(self.formattable,\
													formatinfos)
		return addformattypemessage


class StockHandler():
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
		db_path = self.db_path
		self.table = table
		self.dbstock = DBStock(self.db, self.table)
		
	def addstock(self, stockinfos, symboltable):
		addmessage = self.dbstock.addnewstock(stockinfos, symboltable)
		print(addmessage)

	def getstockcode(self, pattern):
		pass

class IndexHandler():
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
		self.dbindex = IndexDbHandler(self.db, self.table)

	def addindex(self, indexinfos, symboltable):
		addmessage = self.dbindex.addnewindex(indexinfos, symboltable)
		print(addmessage)

	def getindexcode(self, pattern):
		pass

