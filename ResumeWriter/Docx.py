#!/usr/bin/python
# -*- coding: utf-8 -*-


from   docx import Document, enum
from   pprint import pprint
import sys
from   BaseWriter import BaseWriter
import ResumeWriter.Util.Lookup as Lkp



class ResumeWriter(BaseWriter):
	
	"""
	MS Word document writer
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer name
		if filename == None:
			print "(E) Can't output ODF file to STDOUT, exiting ..."
			sys.exit(2)
		else:
			self.doc = Document()
		self.filename = filename
		self.jobDivide = 2


	def write(self, model=None, lang='en_GB', withPhoto=False, personalData=False, experience=False):
		if model == None:
			print "(E) Empty resume model."
			return
		self.lang = lang
		self.withPhoto = withPhoto
		self.personalData = personalData
		self.experience = experience
		self.writeHeader(model)
		#self.writeAddress(model)
		#self.writeSummary(model)
		#self.writeSkills(model)
		#self.writeEmployment(model)
		#self.writeCertifications(model)
		#self.writeEducation(model)
		#self.writeLanguages(model)
		#self.writeHobbies(model)
		#self.writeReferences(model)
		self.doc.save( self.filename + ".docx" )


	def writeHeader(self, model):
		self.doc.add_heading( model.personName, 0 )
