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


