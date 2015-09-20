#!/usr/bin/python
# -*- coding: utf-8 -*-

from   pprint import pprint
import sys
from   BaseWriter import BaseWriter
import ResumeWriter.Util.Lookup as Lkp



class ResumeWriter(BaseWriter):
	
	"""
	reStructuredText writer
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer name
		if filename == None:
			self.outFile = sys.stdout
		else:
			try:
				self.outFile = open( filename + ".rst", 'wb' )
			except IOError:
				print "(E) Unable to open file '%s' for output, exiting ..." % filename
				sys.exit(2)
		self.jobDivide = 2


	def __del__(self):
		if self.outFile != sys.stdout:
			self.outFile.close()


	def write(self, model=None, lang='en_GB', withPhoto=False, personalData=False, experience=False):
		if model == None:
			self.wrln( "Empty resume model." )
			return
		self.lang = lang
		self.withPhoto = withPhoto
		self.personalData = personalData
		self.experience = experience
		self.writeHeader(model)
		self.writeAddress(model)
		self.writeSummary(model)
		self.writeSkills(model)
		self.writeEmployment(model)
		#self.writeCertifications(model)
		#self.writeEducation(model)
		self.writeLanguages(model)
		self.writeHobbies(model)
		self.writeReferences(model)


	def writeHeader(self, model):
		titleEquals = "=" * len(model.personName)
		self.wrln( titleEquals )
		self.wrln( model.personName )
		self.wrln( titleEquals )


	def writeAddress(self, model):
		emailAddr = self.lookup( self.lang, Lkp.emailAddrMap )
		mobileNum = self.lookup( self.lang, Lkp.mobileNumberMap )
		# Look up country based on country code
		country = self.lookup( self.lang, Lkp.countryMap, model.countryCode )
		# Street address
		frmtStreetAddr = " %s " % model.streetAddress
		# Postal code, municipality, region
		frmtPostCodeEtc = " %s %s, %s " % (model.postalCode, model.municipality, model.region)
		# Email address
		frmtEmail = " %s: **%s** " % (emailAddr, model.privateEmailAddress)
		# Phone number
		frmtPhone = " %s: **%s** " % (mobileNum, model.mobilePhone)
		# Country
		frmtCountry = " %s " % country
		# Swiss work permit
		swissPermit = self.lookup( self.lang, Lkp.swissPermitMap )
		frmtSwissPermit = " %s: **C** " % swissPermit
		# Determine maximum width for postal address column
		lStreetAddr = [ len( frmtStreetAddr ) ]
		lStreetAddr.append( len( frmtPostCodeEtc ) )
		lStreetAddr.append( len( frmtCountry ) )
		maxLenAddr = max(lStreetAddr)
		# Determine maximum width for email, phone etc. column
		lAddr = [ len( frmtEmail ) ]
		lAddr.append( len( frmtPhone ) )
		maxAddr = max(lAddr)
		# Table for contact data
		self.wrln( "" )
		if self.withPhoto:
			tblRow = '+%s+%s+%s+' % ( '----------', '-' * maxLenAddr, '-' * maxAddr )
			self.wrln( tblRow )
			self.wrln( '| |cndpic| |%s|%s|' % (frmtStreetAddr.ljust(maxLenAddr), frmtPhone.ljust(maxAddr),) )
			tblRow = '+%s+%s+%s+' % ( '          ', '-' * maxLenAddr, '-' * maxAddr )
			self.wrln( tblRow )
			self.wrln( '|          |%s|%s|' % (frmtPostCodeEtc.ljust(maxLenAddr), frmtEmail.ljust(maxAddr) ) )
			tblRow = '+%s+%s+%s+' % ( '          ', '-' * maxLenAddr, '-' * maxAddr )
			self.wrln( tblRow )
			self.wrln( '|          |%s|%s|' % (frmtCountry.ljust(maxLenAddr), frmtSwissPermit.ljust(maxAddr)) )
			if self.personalData:
				tblRow = '+%s+%s+%s+%s+' % ( '----------', '-' * maxLenAddr, '-' * maxAddr, '---------' )
				self.wrln( tblRow )
			else:
				tblRow = '+%s+%s+%s+' % ( '----------', '-' * maxLenAddr, '-' * maxAddr )
				self.wrln( tblRow )
		else:
			tblTop = '+%s+%s+' % ( '-' * maxLenAddr, '-' * maxAddr )
			self.wrln( tblTop )
			self.wrln( '|%s|%s|' % (frmtStreetAddr.ljust(maxLenAddr), frmtPhone.ljust(maxAddr),) )
			self.wrln( tblTop )
			self.wrln( '|%s|%s|' % (frmtPostCodeEtc.ljust(maxLenAddr), frmtEmail.ljust(maxAddr) ) )
			self.wrln( tblTop )
			self.wrln( '|%s|%s|' % (frmtCountry.ljust(maxLenAddr), frmtSwissPermit.ljust(maxAddr)) )
			self.wrln( tblTop )
		if self.withPhoto:
			self.wrln( '.. |cndpic| image:: ' + model.personPhoto )
		self.wrln( "" )


	def writeSummary(self, model):
		if model.execS != []:
			self.wrln( '-------' )
			self.wrln( 'Summary' )
			self.wrln( '-------' )
			for line in model.execS:
				self.wrln( line )
			self.wrln( "" )
		if model.objct != []:
			self.wrln( '---------' )
			self.wrln( 'Objective' )
			self.wrln( '---------' )
			for line in model.objct:
				self.wrln( line )
			self.wrln( "" )


	def writeSkills(self, model):
		self.wrln( '------' )
		self.wrln( 'Skills' )
		self.wrln( '------' )
		self.wrln( "" )
		
	def writeEmployment(self, model):
		self.wrln( '-----------------------' )
		self.wrln( 'Professional Experience' )
		self.wrln( '-----------------------' )
		self.wrln( "" )
		

	def writeLanguages(self, model):
		self.wrln( '---------' )
		self.wrln( 'Languages' )
		self.wrln( '---------' )
		langLine = ''
		for lang in model.lang:
			# Look up name of that language
			langName = self.lookup(self.lang, Lkp.langMap, lang[ 'code' ])
			langLine += langName
			if len(lang[ 'comments' ]) > 2:
				langLine += " (%s)" % lang[ 'comments' ]
			langLine += ", "
		self.wrln( langLine[:-2] + "." )
		self.wrln( "" )
		
		
	def writeHobbies(self, model):
		self.wrln( '-------' )
		self.wrln( 'Hobbies' )
		self.wrln( '-------' )
		hobbies = []
		for values in model.addt.values():
			hobbies += values
		self.wrln( ", ".join(hobbies) + "." )
		self.wrln( "" )
		
		
	def writeReferences(self, model):
		self.wrln( '----------' )
		self.wrln( 'References' )
		self.wrln( '----------' )
		self.wrln( self.lookup(self.lang, Lkp.referenceRequestMap) )
		self.wrln( "" )


	def wr(self, s):
		self.outFile.write(s.encode('utf-8'))


	def wrln(self, s):
		self.wr(s + '\n')
