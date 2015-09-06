#!/usr/bin/python
# -*- coding: utf-8 -*-


from   odf.opendocument import OpenDocumentText
from   odf.style import FontFace, ListLevelProperties, ParagraphProperties, Style, TextProperties
from   odf.text import List, ListItem, ListLevelStyleBullet, ListStyle, P, Span
from   pprint import pprint
import sys
from   BaseWriter import BaseWriter
import ResumeWriter.Util.Lookup as Lkp



class ResumeWriter(BaseWriter):
	
	"""
	Open Document Format writer
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer name
		if filename == None:
			print "(E) Can't output ODF file to STDOUT, exiting ..."
			sys.exit(2)
		else:
			self.doc = OpenDocumentText()
		self.filename = filename
		self.jobDivide = 2


	def __del__(self):
		# File name must be in Unicode format
		self.doc.save( u"" + self.filename, True )


	def write(self, model=None, lang='en_GB', withPhoto=False, personalData=False, experience=False):
		if model == None:
			self.wrln( "Empty resume model." )
			return
		self.lang = lang
		self.withPhoto = withPhoto
		self.personalData = personalData
		self.experience = experience
		p = P(text="Hello World!")
		self.doc.text.addElement(p)
		#self.writeHeader(model)
		#self.writeAddress(model)
		#self.writeSummary(model)
		#self.writeSkills(model)
		#self.writeEmployment(model)
		#self.writeCertifications(model)
		#self.writeEducation(model)
		#self.writeLanguages(model)
		#self.writeHobbies(model)
		#self.writeReferences(model)
