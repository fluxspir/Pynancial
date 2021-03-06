#!/usr/bin/python3
# (c) Franck LABADILLE
# LICENCE BSD
# 20110127
# Pynancial.db
#

"""


"""
import sqlite3
import pdb

class DbHandler:
	"""

	

	"""
	def __init__(self, db_path):
		self.db_path = db_path
		self.conn = sqlite3.connect(db_path)
		

		cur = self.conn.cursor()
		cur.execute('''select name from sqlite_master
									where name="metatable" ''')
		metatableresult = cur.fetchall()
		if not metatableresult:
			cur = self.conn.cursor()
			cur.execute('''create table metatable (
						tablename text unique not null,
						tablegroup text not null) ''')
			print("metatable created")
			self.conn.commit()
			cur.close()

	def _testtableexists(self, table):
		cur = self.conn.cursor()
		cur.execute('''select name from sqlite_master where name="{}"
				'''.format(table))
		tableexistresult = cur.fetchall()
		cur.close()
		if not tableexistresult:
			print("about to create table {}".format(table))
			self._createtable()

	def _addmetatable(self, metadata):
		cur = self.conn.cursor()
		try:
			cur.execute('''insert into metatable ("tablename", "tablegroup")
					values (?,?) ''', metadata)
			self.conn.commit()
			cur.close()
			return 
		except sqlite3.IntegrityError:
			message = "Error while adding new table values {} in metatable\n\
					".format(metadata)
			return message

	def gettablegrouplist(self):
		"""
		return tablegrouplist : list of group availables :
			[ "provider", "stock", "symbol", ]
		"""
		cur = self.conn.cursor()
		cur.execute('''select tablegroup from metatable''')
		tablegrouplist = cur.fetchall()
		cur.close()
		return tablegrouplist

	def gettableslist(self, tablegroup=""):
		""" 
		tablegroup = ( "grp1", "grp2" )
		return tablelist : list of tablenames  [ name1, name2, ]
		"""
		cur = self.conn.cursor()
		if not tablegroup:
			cur.execute('''select tablename from metatable''')
			tablelist = cur.fetchall()
			cur.close()
			return tablelist
		try:
			cur.execute('''select tablename from metatable
						where tablegroup="{}" '''.format(tablegroup))
			tablelist = cur.fetchall()
			cur.close()
			return tablelist
		except sqlite3.OperationalError:
			tablelist = []
			return tablelist

	def gettablename(self, name):
		"""
		return tablename if table is recognize by metatable
		False otherwise
		"""
		cur = self.conn.cursor()
		cur.execute('''select tablegroup from metatable
							where tablename="{}" '''.format(tablename))
		tablename = cur.fetchall()
		cur.close()
		return tablename

	def getsomething(self, columns="", where="" , pattern=""):
		"""
		columns = ( column1, column2, )
		where = column
		pattern = ( 
		return response = [ ( , ,), ] 
		"""
		col = ""
		cur = self.conn.cursor()
		if not columns:
			col = "*"
		else:
			if len(columns) > 1:
				for c in columns:
					if not col:
						col = str(c)
					else:
						col = col + ", " + str(c)
			else:
				col = columns[0]
		
		if not where:
			cur.execute('''select {} from {}'''.format(col, self.table))
			response = cur.fetchall()
			cur.close()
		else:
			##TODO not sure about this synthax
			cur.execute('''select {} from {} where {}="{}" '''
						.format(col, self.table, where, pattern))
			response = cur.fetchall()
			cur.close()
		return response

class StockDbHandler(DbHandler):
	"""
	DATABASE NAME
		Stock
		
	DATABASE STRUCTURE
		* (rowid)
		* code  : text, unique, not null
		* name	: text, unique, not null
		* location : text, unique, not null
	
	DATABASE semi_public METHODS:
		* DBStock.addstock(table, stockinfos)

	"""
	def __init__(self, db_path, table):
		""" """
		DbHandler.__init__(self, db_path)
		self.db_path = db_path
		self.table = table
		self.tablegroup = "stock"
		self.metadata = (self.table, self.tablegroup)

	def _createtable(self):
		cur = self.conn.cursor()
		try:
			cur.execute('''create table {} (
						code text unique not null,
						name text unique not null,
						location text )
						'''.format(self.table))
			self.conn.commit()
			cur.close()
			self._addmetatable(self.metadata)
		except sqlite3.OperationalError:
			print("Table {} already exists".format(self.table))

	def _inserttable(self):
		"""
		stockinfos = [ ( "USxxxxxxxx", "google inc" , "NYSE" )
					  ( "FRxxxxxxxx", "BNP Paribas", "Paris"), ]
		insert into stocktable values ( "code"(stockinfo[0]) ,\
											"name"(stockinfo[1] ) 
		"""
		stockinforefused= []
		cur = self.conn.cursor()
		for stockinfo in self.stockinfos:
			try:
				cur.execute('''insert into {} ("code", "name", "location")
						values(?,?,?) '''.format(self.table), stockinfo)
				self.conn.commit()
				cur.close()
			except sqlite3.OperationalError:
				self._createtable()
			except sqlite3.IntegrityError:
				stockinforefused.append(stockinfo)
		return stockinforefused

	def addnewstock(self, stockinfos, symboltable):
		"""
		insert into stocktable values (tokencode, real_name, location)
		stockinfos = [ ( tokencode, real_name, stockexchangelocation )
						( "USxxxxxxxx", "google inc" , "NYSE" )
					  	( "FRxxxxxxxx", "BNP Paribas", "Paris"), ]

		symboltable = DBSymbol.__tablename__
		"""
		self.stockinfos = stockinfos
		self.symboltable = symboltable
		self.dbsymbol = SymbolDbHandler(self.db_path, self.symboltable)
		symbolexist = self.dbsymbol._testsymboltableexists()

		if not symbolexist:
			message = "Please add at least one  provider before trying to add\
			a stock\n"
			return message

		def test_input(test):
			tokencodes = []
			for chunk in stockinfos:
				for token in chunk:
					if not token:
						print(" 3 values mandatory in {}\n".format(chunk))
						return 
					if not token.isprintable():
						print("values must be alpha-numeric in {}\n\
							".format(chunk))
						return
				tokencodes.append(chunk[0])
			return tokencodes

		tokencodes = test_input(self.stockinfos)
		if not tokencodes:
			message = "Please correct wrongly_written  values\n"
			return message

		self._testtableexists(self.table)
		## insert into stock table the stockinfos.
		stocktabledoubles = self._inserttable()
		if stocktabledoubles:
			message = "Tokens {} where already in table {}\n\
			".format(stocktabledoubles, self.table)
			return message

		symboltabledoubles = self.dbsymbol._altertable(tokencodes)
		if symboltabledoubles:
			message = "Tokens {} where already in table {}\n\
			".format(tokenrefused, self.symboltable)
			return message
		message = "OK"
		return message

class IndexDbHandler(DbHandler):
	"""

	Index database
		* (rowid)
		* code unique not null
		* name unique not null
		* location not null

		altered with stockcode int (1/0) 

	"""
	def __init__(self, db_path, table):
		DbHandler.__init__(self, db_path)
		self.db_path = db_path
		self.table = table
		self.tablegroup = "index"
		self.metadata = (self.table, self.tablegroup)

	def _createtable(self):
		cur = self.conn.cursor()
		try:
			cur.execute('''create table {} (
					code text unique not null,
					name text unique not null,
					location text unique not null)
					'''.format(self.table))
			self.conn.commit()
			cur.close()
			self._addmetatable(self.metadata)
		except sqlite3.OperationalError:
			print("table {} already exists".format(self.table))

	def _inserttable(self):
		""" """
		cur = self.conn.cursor()
		tokenrefused = []
		for indexinfo in self.indexinfos:
			try:
				cur.execute("""insert into {} ("code", "name", "location") \
				values (?,?,?)""".format(self.table), indexinfo)
				self.conn.commit()
				cur.close()
			except sqlite3.IntegrityError:
				tokenrefused.append(indexinfo)
		return tokenrefused
	
	def addnewindex(self, indexinfos, symboltable):
		""" """
		self.indexinfos = indexinfos
		self.dbsymbol = SymbolDbHandler(self.db, symboltable)
		symbolexists = self.dbsymbol._testtable()

		def testinput(self, indexinfos):
			tokencodes = []
			for chunk in indexinfos:
				for token in chunk:
					if not token:
						print("3 values mandatory in {}\n".format(chunk))
						return
					elif token.isalnum:
						pass
					else:
						print("Values must be alpha-numeric in {}\n\
						".format(chunk))
						return
				tokencodes.append(chunk[0])
			return tokencodes

		tokencodes = self.testinput(self.indexinfos)
		if not tokencodes:
			message = "Please correct wrongly-written values\n"
			return message

		self._testtableexists(self.table)
		indextabledoubles = self._inserttable()
		if indextabledoubles:
			message = "Token {} were already in table {}\n\
			".format(indextabledoubles, self.table)
			return message

		symboltabledoubles = self.dbsymbol._altertable(tokencodes)
		if symboltabledoubles:
			message = "Tokens {} were already in table {}\n\
			".format(symboltabledoubles, symboltable)
			return message
		message = "OK"
		return message

class ProviderDbHandler(DbHandler):

	"""
	DATABASE NAME
		ProviderTable ("providertable_1",...
			(most people use only one)

	DATABASE STRUCTURE
		(rowid)
		providername : "my_name" text MANDATORY, UNIQUE
		baseurl : "http://finance.$$$.com/cvsdownload/" text
		preformat : "&formatquery="text
		presymbol : "&symbolquery=%" text"

		altered with format text foreign DBFormat name

	DATABASE semi_public METHOD
		DBProvider.addprovider()
		DBProvider.addformat()

	"""

	def __init__(self, db_path, table):
		DbHandler.__init__(self, db_path)
		self.db_path = db_path
		self.table = table
		self.tablegroup = "provider"
		self.metadata = (self.table, self.tablegroup)

	def _createtable(self):
		cur = self.conn.cursor()
		try:
			cur.execute('''create table {} (
					providername text unique not null,
					baseurl text not null,
					preformat text,
					presymbol text )'''.format(self.table))
			self.conn.commit()
			cur.close()
			self._addmetatable(self.metadata)
		except sqlite3.OperationalError:
			raise
			print("table {} already exists".format(self.table))
	
	def _alterwithnewformat(self, formatnames):
		""" formatnames = ( name1, name2, names3, )"""
		cur = self.conn.cursor()
		alreadyknownformat = []
		for formatname in formatnames:
			try:
				cur.execute('''alter table {} add {} text
						'''.format(self.table, formatname))
				self.conn.commit()
				cur.close
			except sqlite3.OperationalError:
				alreadyknownformat.append(formatname)
		return alreadyknownformat

	def _insertnewprovider(self):
		""" """
		cur = self.conn.cursor()
		providerrefused = []
		for providerinfo in self.providerinfos:
			try:
				cur.execute('''insert into {} ("providername", "baseurl", 
				"preformat", "presymbol") values (?,?,?,?)
						'''.format(self.table), providerinfo)
				self.conn.commit()
				cur.close()
			except sqlite3.OperationalError:
				self._createtable()
				self._insertnewprovider()
			except sqlite3.IntegrityError:
				providerrefused.append(providerinfo)
		return providerrefused

	def addprovider(self, providerinfos, symboltable):
		"""
		When you add, a provider, you'll have some information to give.
			* Provider's infos : a list of tuples that each contain :
			  providerinfos = [(provider_name, base_url, preformat, presymbol),
						("yahoo", "http://download.finance.yahoo.com/d/quotes\
						.csvr?e=.csv ", "&f=", "&s=" ) ]
			* Symbol table name : there will be kept the "provider_name" to 
				match with the token(stock, indice...)_name.
				symboltable = DBSymbol.__tablename__
			* Format table name : where 
			formattable = DBFormat.__tablename__
		"""
		self.providerinfos = providerinfos
		self.symboltable = symboltable

		providernames = []
		def testproviderinfos():
			""" """
			for chunk in providerinfos:
				if not chunk[0].isalnum():
					print("provider name {} must be alphanumeric please\n\
					".format(chunk[0]))
					return
				if not chunk[1].isprintable():    ##TODO regex to verify url 
					print("baseurl {} must be a valid base url for query\n\
					".format(chunk[1]))
					return
				if not chunk[2].isprintable():
					print("enter preformat {} valid please\n\
					".format(chunk[2]))
					return
				if not chunk[3].isprintable():
					print("Enter presymbol {} valid please\n\
					".format(chunk[3]))
					return
				providernames.append(chunk[0])
			return providernames
		
		providernames = testproviderinfos()
		if not providernames:
			message = "Please correct wrongly_written values\n"
			return message
		# see if table exists, otherwise, create it.
		self._testtableexists(self.table)
		# add providerinfos in providertable
		providerrefused = self._insertnewprovider()
		if providerrefused:
			message = "providers {} where already in {}\n\
			".format(providerrefused, self.table)
			return message

		# add providername into Symbol database
		self.dbsymbol = SymbolDbHandler(self.db_path, self.symboltable, \
										self.table)
		symboladd = self.dbsymbol.insertnewprovider(tuple(providernames))
		if symboladd:
			message = "provider(s) {} where already in symboldatabase {}\n\
			".format(providernames, self.symboltable)
			return message
		message = "OK"
		return message

	def addformat(self, formattable, formatinfos):
		"""
		to add a format, we need to know ther providertable \
								(self.table at instanciation)
		formatinfos = [ ( "sname", "explicit_name" ), ]
		DbProvider._altertable(self.db, self.table)
		DbFormat(self.db, formattable)._inserttable(formatinfos)
		return formatnames = [ "name1", "name2", ]
		"""
		formatinfos = formatinfos

		def _testinput(formatinfos):
			formatnames = []
			for formatinfo in formatinfos:
				for c in formatinfo[0]:
					if c.isalnum():
						pass
					else:
						print("format {} mustn't contain whitespaces. Please\
change it.\n".format(formatinfo[0]))
						return
				formatnames.append(formatinfo[0])
				for c in formatinfo[1]:
					if c.isprintable:
						pass
					else:
						print("format description {} must be alphanumeric, \
please\n".format(formatinfo[1]))
						return
			return formatnames

		formatnames = _testinput(formatinfos)
		if not formatnames:
			message = "Please correct wrongly written values\n"
			return message
		# alter providertable with new format
		formatrefused = self._alterwithnewformat(tuple(formatnames))
		if formatrefused:
			message = "format {} were already in {}\n\
			".format(formatrefused, self.table)
			print(message)
			return message

		# insert formatinfos in formattable
		dbformat = FormatDbHandler(self.db_path, formattable)
		formatadd = dbformat._insertnewformat(formatinfos)
		if formatadd:
			message = "formats {} where already in {} database\n\
			".format(formatadd, formattable)
			print(message)
			return message
		message = "OK"
		return message

	def updateformat(self, formattable, urlformats):
		""" 
		urlformats = ( ("providername", "shortname", "urlformatstring" , ) )
		 insert/replace into PROVIDERTABLE values ("providername","shortname",\
		 												"urlformatstring" )
		return
		"""
		cur = self.conn.cursor()
		urlformatreject = []
		for urlformat in urlformats:
			# test if "shortname"(provider's columnname) exists in format table
			# if not, insert format
			#TODO should test values
			formatvalues = (urlformat[2],)
			try:
				cur.execute('''update or replace {} set "{}"="{}" 
								where "providername"="{}" '''\
								.format(self.table, urlformat[1], \
								urlformat[2], urlformat[0]))
				self.conn.commit()
				cur.close()
			except sqlite3.IntegrityError:
				urlformatreject.append(urlformat)
		return urlformatreject

class SymbolDbHandler(DbHandler):
	"""

	DATABASE NAME
		Symbol_XX

	DATABASE STRUCTURE

		* (rowid)
		* providername : foreign rowid DBProvider (text, MANDATORY, unique)
	
		Be altered with
			foreign locationname from databases (type : Stock, \
													Index, Trackers...)

	DATABASE without public access.
		accesses via DBProvider(), DBStock(), DBIndex(),...
		will be created after an access from DBProvider.
		Need to add a Provider before all.

	"""
	def __init__(self, db_path, table, providertable=""):
		DbHandler.__init__(self, db_path)
		self.db_path = db_path
		self.table = table
		self.tablegroup = "symbol"
		self.metadata = (self.table, self.tablegroup)

		self.providertable = providertable
		symboltableexists = self._testsymboltableexists()
		if not symboltableexists:
			if providertable:
				self._createtable(self.providertable)
			else:
				print("Please give the providertable name you want \
new symboltables {} be reliated.\n".format(self.table))

	def _testsymboltableexists(self):
		cur = self.conn.cursor()
		cur.execute('''select name from sqlite_master where name="{}"
				'''.format(self.table))
		testinmetatable = cur.fetchall()
		cur.close()
		for r in testinmetatable:
			return r

	def _createtable(self, providertable):
		cur = self.conn.cursor()
		try:
			cur.execute('''create table {} (
						provider text unique not null,
						foreign key(provider) references {}(name))
					'''.format(self.table, providertable))
			self.conn.commit()
			cur.close()
			self._addmetatable(self.metadata)
		except sqlite3.OperationalError:
			print("Table of symbols {} already exists".format(self.table))

	def insertnewprovider(self, providernames):
		""" 
			providernames = ( "provider1", "provider2", )
		"""
		cur = self.conn.cursor()
		providerrefused = []
		for providername in providernames:
			try:
				cur.execute('''insert into {} ("provider") values (?)
					  '''.format(self.table), (providername,) )
				self.conn.commit()
				cur.close()
			except sqlite3.OperationalError:
				self._createtable(providername)
				self.insertnewprovider(providernames)
			except sqlite3.IntegrityError:
				providerrefused.append(providername)
		return providerrefused

	def _altertable(self, tokencodes):
		"""
			locationtable = ( location1, "NYSE", Paris, )
			tokentable = DBStock or DBIndex, or DBTrackers...
			return False ,  
			otherwise, list of token that could not alter the table
		"""
		cur = self.conn.cursor()
		tokenrefused = []
		for tokencode in tokencodes:
			try:
				cur.execute('''alter table {} add {} text
					  '''.format(self.table, tokencode))
				self.conn.commit()
				cur.close()
			except sqlite3.OperationalError:
				tokenrefused.append(tokencode)
		return tokenrefused

	def addsymbol(self, newsymbols):
		"""
		newsymbols = [( provider, value(token), symbol), ]
		insert into self.table value
		return symbolsrefused 
		symbolrefused = [ ( providerrefused, valuerefused, symbolrefused),]
		"""
		cur = self.conn.cursor()
		symbolrefused = []
		for symbol in newsymbols:    # symbol = ( provider, value, symbol )
			try:
				insertvalues = (symbol[0], symbol[2])
				cur.execute('''update or replace {} set "{}"="{}"
							where "provider"="{}" '''.format(self.table, \
							symbol[1], symbol[2], symbol[0]))
#				cur.execute('''update or replace {} set ("provider","{}") \
#				values (?,?)'''.format(self.table, symbol[1]), insertvalues)
				self.conn.commit()
				cur.close()
			except sqlite3.IntegrityError:
				symbolrefused.append(symbol)
		return symbolrefused

#urlformats = ( ("providername", "shortname", "urlformatstring" , ) )
#
#				cur.execute('''update or replace {} set "{}"="{}" 
#								where "providername"="{}" '''\
#								.format(self.table, urlformat[1], \
#								urlformat[2], urlformat[0]))
#				self.conn.commit()

class FormatDbHandler(DbHandler):
	"""

	DATABASE NAME
	Format_xx

	DATABASE STRUCTURE
		* (rowid)
		* provider_alter_column_name
		* format name human readable
			
	"""
	def __init__(self, db_path, formattable):
		DbHandler.__init__(self, db_path)
		self.db_path = db_path
		self.table = formattable
		self.tablegroup = "format"
		self.metadata = (self.table, self.tablegroup)
		formattableexists = self._testtableexists(self.table)

	def _createtable(self):
		"""
		(format id: integer foreign rowid dbprovider) ?
		colname = name used to alter in DBProvider and add new provider queries
			(cf BDFormat.insertformat() )
		name = text, unique, human readable name
		"""
		cur = self.conn.cursor()
		try:
			cur.execute('''create table {} (
					columnname text unique,
					explicitname text not null)'''.format(self.table))
			self.conn.commit()
			cur.close()
			self._addmetatable(self.metadata)	
		except sqlite3.OperationalError:
			print("the table {} already exists".format(self.table))
			
	def _insertnewformat(self, newformats):
		"""
		newformats = [(the DBProvider colums names, "long name" ),
						(	"name" , "name"	),
						(	"sname", "short name"),
						(	"lname", "long name"),
						(	"nowprice", "actual price") ]
		"""
		cur = self.conn.cursor()
		formatrefused = []
		for newformat in newformats:
			try:
				cur.execute('''insert into {} ("columnname", "explicitname") \
						values(?,?)'''.format(self.table), newformat)
				self.conn.commit()
				cur.close()
			except sqlite3.IntegrityError:
				formatrefused = []
		return formatrefused

	def testformat_provider(self, formatname, providertable):
		""" """
		pass

