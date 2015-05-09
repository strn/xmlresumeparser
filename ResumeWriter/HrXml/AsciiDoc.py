#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from BaseWriter import BaseWriter
from ResumeWriter.Util.Lookup import countryMap, langMap, presMap
from pprint import pprint


class ResumeWriter(BaseWriter):
	
	"""
	AsciiDoc
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer
		# name
		BaseWriter.__init__(self, filename)
		self.jobDivide = 2


	def write(self, model=None, lang='en'):
		if model == None:
			self.wrln( "Empty resume model." )
			return
		self.lang = lang
		self.writeHeader(model)
		self.writeAddress(model)
		self.writeSummary(model)
		self.writeSkills(model)
		self.writeEmployment(model)
		self.writeCertifications(model)
		self.writeEducation(model)
		self.writeLanguages(model)
		self.writeHobbies(model)
		self.writeReferences(model)
		self.writeFooter(model)
		

	def writeHeader(self, model):
		self.wrln( "= %s =" % model.personName )
		self.wrln( ":lang: %s" % self.lang )
		self.wrln( ":data-uri:" )
		self.wrln( ":doctype: article" )
		self.wrln( ":encoding: UTF-8" )
		self.wrln( ":stylesdir: ResumeStyle" )
		self.wrln( ":stylesheet: BaseAsciiDoc-print.css" )
		self.wrln( ":disable-javascript:" ) # Javascript is in most cases NOT required in CV
		self.wrln( ":linkcss:" )
		self.wrln( ":last-update-label!:" )
		keyLine = ""
		for skilLine in model.skil:
			keyLine += ", ".join(skilLine[1:]) + ", "
		self.wrln( ":keywords: CV, HR-XML, " + keyLine[:-2] )
		self.wrln( "" )


	def writeFooter(self, model):
		#self.wrln( "include::ResumeStyle/AsciiDoc-footer.html[]" )
		pass


	def writeAddress(self, model):
		# Table for contact data
		self.wrln( '[width="100%", cols="<,>", grid="none", frame="none"]' )
		self.wrln( '|=============' )
		self.wrln( '|%s | mobile tel. number: *%s*' % (model.streetAddress, model.mobilePhone,) )
		self.wrln( '|%s %s, %s | email address: %s' % (model.postalCode, model.municipality, model.region, model.privateEmailAddress,) )
		# Look up country based on country code
		country = self.lookup( self.lang, countryMap, model.countryCode )
		self.wrln( '|%s | ' % (country,) )
		self.wrln( '|=============' )
		self.wrln( "" )


	def writeSummary(self, model):
		if model.execS != []:
			self.wrln( '== Summary ==' )
			for line in model.execS:
				self.wrln( line )
			self.wrln( "" )
		if model.objct != []:
			self.wrln( '== Objective ==' )
			for line in model.objct:
				self.wrln( line )
			self.wrln( "" )
		
		
	def writeSkills(self, model):
		self.wrln( '== Skills ==' )
		self.wrln( '[width="100%",cols="25s,75", grid="none", frame="none"]' )
		self.wrln( '|=============' )
		for skilLine in model.skil:
			self.wrln( "|%s:|%s" % (skilLine[0], ", ".join(skilLine[1:])) )
		self.wrln( '| | ' )
		self.wrln( '|=============' )
		self.wrln( "" )


	def writeEmployment(self, model):
		self.wrln( '== Employment ==' )
		numJobs = len(model.empl)
		# Print details of only most recent jobs (0 to jobDivide-1)
		# for other jobs list only employer, start and end dates
		self.wrln( '[width="100%",cols="70%,30%", grid="none", frame="none"]' )
		self.wrln( '|=======================================================' )
		for i in range(0, self.jobDivide):
			job = model.empl[i]
			country = self.lookup( self.lang, countryMap, job['cntr'] )
			#pprint( job )
			self.wrln( '2+<|[companyname]*%s*, %s, %s' % (job['name'], job['city'], country) )
			#self.wrln( "|" )
			for pos in job['job']:
				#self.wrln( str(pos) )
				if pos.has_key( 'end' ):
					endDate = pos[ 'end' ]
				else:
					endDate = self.lookup( self.lang, presMap )
				if pos[ 'dept' ] == None:
					dept = '' 
				else:
					dept = ' (%s)' % pos[ 'dept' ]
				self.wrln( '<|%s%s >|_%s - %s_' % (pos['title'], dept, pos['start'], endDate) )
				self.wrln( "2+a|" )
				for line in pos[ 'desc' ]:
					self.wrln( "  " + line )
				#self.wrln( "|" )
		#self.wrln( "|" )
		for i in range(self.jobDivide, numJobs):
			job = model.empl[i]
			country = self.lookup( self.lang, countryMap, job['cntr'] )
			self.wrln( '2+<|[companyname]*%s*, %s, %s' % (job['name'], job['city'], country) )
			self.wrln( '<|%s >|_%s - %s_' % (job['job'][0]['title'], job['job'][0]['start'], job['job'][0]['end']) )
			self.wrln( "| | " )
			self.wrln( "| | " )
			self.wrln( "| | " )
		self.wrln( '|=======================================================' )
		self.wrln( "" )
		

	def writeCertifications(self, model):
		self.wrln( '== Certifications ==' )
		for cert in model.cert:
			self.wrln( "* %s _(%s)_" % (cert[ 'name' ], cert[ 'issued' ]) )
		self.wrln( "" )
		self.wrln( "" )
		
		
	def writeEducation(self, model):
		self.wrln( '== Education ==' )
		self.wrln( '[width="100%",cols="<70%,>30%", grid="none", frame="none"]' )
		self.wrln( '|=============' )
		for edu in model.edu:
			country = self.lookup( self.lang, countryMap, edu[ 'cntr' ] )
			self.wrln( '|*%s*, %s, %s, %s |_(%s - %s)_' % \
				(edu[ 'school' ], edu[ 'orgunit' ], edu[ 'city' ], country, edu[ 'start' ], edu[ 'end' ]) )
		self.wrln( '|=============' )
		self.wrln( "" )
		
		
	def writeLanguages(self, model):
		self.wrln( '== Languages ==' )
		langLine = ''
		for lang in model.lang:
			# Look up name of that language
			langName = self.lookup(self.lang, langMap, lang[ 'code' ])
			langLine += langName
			if len(lang[ 'comments' ]) > 2:
				langLine += " (%s)" % lang[ 'comments' ]
			langLine += ", "
		self.wrln( langLine[:-2] + "." )
		self.wrln( "" )
		
		
	def writeHobbies(self, model):
		self.wrln( '== Hobbies ==' )
		hobbies = []
		for values in model.addt.values():
			hobbies += values
		self.wrln( ", ".join(hobbies) + "." )
		self.wrln( "" )
		
		
	def writeReferences(self, model):
		self.wrln( '== References ==' )
		self.wrln( 'References are available upon request.' )
		self.wrln( "" )
		
