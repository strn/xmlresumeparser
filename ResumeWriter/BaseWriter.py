#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import locale


class BaseWriter:
	
	"""
	BaseWriter
	
	Implements base methods for writing parsed HR-XML resumes
	"""
	
	def __init__(self, filename=None):
		if filename == None:
			self.outFile = sys.stdout
		else:
			try:
				self.outFile = open( filename, 'wb' )
			except IOError:
				print "Unable to open file '%s' for output, exiting ..." % filename
				sys.exit(2)


	def __del__(self):
		if self.outFile != sys.stdout:
			self.outFile.close()
			

	def wr(self, s):
		self.outFile.write(s.encode('utf-8'))


	def wrln(self, s):
		self.wr(s + '\n')


	def lookup(self, lang, *arg):
		"""
		Helper method that looks up value for given key in specific language
		"""
		if len(arg) == 1:
			aDict = arg[0]
			if aDict.has_key( lang ):
				retVal = aDict[ lang ]
			else:
				retVal = '### (not found for lang %s) ###' % lang
		elif len(arg) == 2:
			aDict = arg[0]
			key = arg[1]
			if aDict.has_key( lang ):
				langValues = aDict[ lang ]
				if langValues.has_key( key ):
					retVal = langValues[ key ]
				else:
					retVal = key
			else:
				retVal = key
		else:
			print "Unsuported parameters:",arg
			sys.exit(3)
		return retVal
	

	def getNLDate(self, aDate, aLang):
		locale.setlocale(locale.LC_TIME, aLang)
		format_ = datetime.datetime.strptime(aDate, '%Y-%m-%d').strftime('%x')
		return format_


	def getNLYear(self, aLang, aDate):
		if len(aDate) < 4:
			return '0000'
		else:
			return aDate[:4]
