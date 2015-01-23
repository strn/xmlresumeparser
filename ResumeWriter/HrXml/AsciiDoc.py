#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from BaseWriter import BaseWriter


class ResumeWriter(BaseWriter):
	
	"""
	AsciiDoc
	"""

	def write(self, model=None):
		if model == None:
			self.wrln( "Empty resume model." )
			return
		print
		print model
		print
		self.wrln( "= Curriculum Vitae - %s =" % model.personName )
		self.wrln( ":data-uri:" )
		self.wrln( ":doctype: article" )
		self.wrln( ":encoding: UTF-8" )
		self.wrln( ":lang: en" )
		self.wrln( ":quirks:" )
		self.wrln( ":theme: cv" )
		self.wrln( ":toclevels: 2")
		self.wrln( "" )
		self.wrln( "== Personalia ==" )
