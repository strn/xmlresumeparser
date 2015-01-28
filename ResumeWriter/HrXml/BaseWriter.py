#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


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
		self.outFile.write(s)


	def wrln(self, s):
		self.outFile.write(s + '\n')


	def lookup(self, lang, *arg):
		"""
		Helper method that looks up value for given key in specific language
		"""
		if len(arg) == 1:
			aDict = arg[0]
			if aDict.has_key( lang ):
				retVal = aDict[ lang ]
			else:
				retVal = '###'
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
	
