#!/usr/bin/python
# -*- coding: utf-8 -*-

from   pprint import pprint
import sys
from   BaseWriter import BaseWriter
import ResumeWriter.Util.Lookup as Lkp


class ResumeWriter(BaseWriter):
	
	"""
	AsciiDoc
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer name
		if filename == None:
			self.outFile = sys.stdout
		else:
			try:
				self.outFile = open( filename + ".adoc", 'wb' )
			except IOError:
				print "(E) Unable to open file '%s' for output, exiting ..." % filename
				sys.exit(2)
		self.jobDivide = 2
		self.scrSgn = '~' # Script sign: ~ for subscripts, ^ for superscript


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
		self.writeCertifications(model)
		self.writeEducation(model)
		self.writeLanguages(model)
		self.writeHobbies(model)
		self.writeReferences(model)
		

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
		for skilGroup in model.skil.values():
			keyLine += ", ".join(skilGroup[ 'skills' ].keys()) + ", "
		self.wrln( ":keywords: CV, HR-XML, " + keyLine[:-2] )
		self.wrln( "" )


	def writeAddress(self, model):
		# Table for contact data
		if self.withPhoto:
			colsFrm = '20%,16%,16%,20%,20%'
		else:
			colsFrm = '25%,25%,25%,25%'
		self.wrln( '[width="100%%", cols="%s", grid="none", frame="none"]' % colsFrm )
		self.wrln( '|=============' )
		if self.withPhoto:
			if self.personalData:
				self.wrln( '.11+|image:%s[title="%s"]' % (model.personPhoto, model.personPhotoDesc))
			else:
				self.wrln( '.5+|image:%s[title="%s"]' % (model.personPhoto, model.personPhotoDesc))
		emailAddr = self.lookup( self.lang, Lkp.emailAddrMap )
		mobileNum = self.lookup( self.lang, Lkp.mobileNumberMap )
		self.wrln( '2+|%s 2+>| %s: *%s*' % (model.streetAddress, mobileNum, model.mobilePhone,) )
		self.wrln( '2+|%s %s, %s 2+>| %s: *%s*' % \
			(model.postalCode, model.municipality, model.region, emailAddr, model.privateEmailAddress,) )
		# Look up country based on country code
		country = self.lookup( self.lang, Lkp.countryMap, model.countryCode )
		self.wrln( '2+|%s 2+| ' % (country,) )
		self.wrln( "2+|  2+|  " )
		swissPermit = self.lookup( self.lang, Lkp.swissPermitMap )
		if self.personalData:
			dobLbl = self.lookup( self.lang, Lkp.dobMap )
			self.wrln( '2+| |%s: |%s ' % (dobLbl, self.getNLDate(model.dateOfBirth, 'de_CH') ) )
			placeOfLbl = self.lookup( self.lang, Lkp.placeOfBirthMap )
			self.wrln( '2+| |%s: |%s ' % (placeOfLbl, model.birthPlace) )
			ctznLbl = self.lookup( self.lang, Lkp.nationalityMap )
			nationality = self.lookup( self.lang, Lkp.citizenshipMap, model.nationality )
			self.wrln( '2+| |%s: |%s ' % (ctznLbl, nationality) )
			maritalLbl = self.lookup( self.lang, Lkp.maritalStatusMap )
			self.wrln( '2+| |%s: |%s ' % (maritalLbl, model.maritalStatus ) )
			self.wrln( '2+| |%s: |*C*' % ( swissPermit ) )
		else:
			self.wrln( '2+| 2+>|%s: *C*' % ( swissPermit ) )
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
		# Get skills order and sort it
		skillIds = sorted(model.skil.keys())
		for skilId in skillIds:
			skilGroupName = model.skil[ skilId ][ 'skillGroup' ]
			skills = model.skil[ skilId ][ 'skills' ]
			if self.experience:
				# Write skills followed by years of experience
				self.wrln( "|%s:|%s" % (skilGroupName, ", ".join( map(self.getYearsExp, skills.items()) )) )
			else:
				self.wrln( "|%s:|%s" % (skilGroupName, ", ".join(skills.keys())) )
		self.wrln( '| | ' )
		self.wrln( '|=============' )
		self.wrln( "" )


	# Creates string representing years of experience
	def getYearsExp(self, item):
		# get skill name
		skillName = item[0]
		skillDict = item[1]
		if skillDict == {}:
			return skillName
		else:
			if skillDict.has_key( 'yrsExp' ):
				yrs = self.lookup( self.lang, Lkp.yearsMap )
				if skillDict['yrsExp'] not in ('0', '0.0'):
					return '%s %s%s%s %s%s%s' % ( skillName, self.scrSgn, skillDict['yrsExp'], self.scrSgn, self.scrSgn, yrs, self.scrSgn )
				else:
					# Use "since ..." phrase
					since = self.lookup( self.lang, Lkp.sinceMap )
					year = self.getNLYear( self.lang, skillDict[ 'started' ] )
					return '%s %s%s%s %s%s%s' % ( skillName, self.scrSgn, since, self.scrSgn, self.scrSgn, year, self.scrSgn )
			else:
				if skillDict.has_key( 'lastUsed' ):
					yearLast = self.getNLYear( self.lang, skillDict[ 'lastUsed' ] )
					if not yearLast is None:
						# Last used year is an actual value
						yearStart = self.getNLYear( self.lang, skillDict[ 'started' ] )
						if yearStart == yearLast:
							return '%s %s%s%s' % ( skillName, self.scrSgn, yearStart, self.scrSgn )
						else:
							return '%s %s%s-%s%s' % ( skillName, self.scrSgn, yearStart, yearLast, self.scrSgn )
					else:
						since = self.lookup( self.lang, Lkp.sinceMap )
						return '%s %s%s%s %s%s%s' % ( skillName, self.scrSgn, since, self.scrSgn, self.scrSgn, yearStart, self.scrSgn )
				else:
					# Use "since ..." phrase
					since = self.lookup( self.lang, Lkp.sinceMap )
					year = self.getNLYear( self.lang, skillDict[ 'started' ] )
					return '%s %s%s%s %s%s%s' % ( skillName, self.scrSgn, since, self.scrSgn, self.scrSgn, year, self.scrSgn )
		

	def writeEmployment(self, model):
		self.wrln( '== Professional Experience ==' )
		numJobs = len(model.empl)
		# Print details of only most recent jobs (0 to jobDivide-1)
		# for other jobs list only employer, start and end dates
		self.wrln( '[width="100%",cols="70%,30%", grid="none", frame="none"]' )
		self.wrln( '|=======================================================' )
		for i in range(0, self.jobDivide):
			job = model.empl[i]
			country = self.lookup( self.lang, Lkp.countryMap, job['cntr'] )
			#pprint( job )
			self.wrln( '2+<|[companyname]*%s*, %s, %s' % (job['name'], job['city'], country) )
			#self.wrln( "|" )
			for pos in job['job']:
				#self.wrln( str(pos) )
				if pos.has_key( 'end' ):
					endDate = pos[ 'end' ]
				else:
					endDate = self.lookup( self.lang, Lkp.presMap )
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
			country = self.lookup( self.lang, Lkp.countryMap, job['cntr'] )
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
			country = self.lookup( self.lang, Lkp.countryMap, edu[ 'cntr' ] )
			self.wrln( '|*%s*, %s (%s, %s) |_%s - %s_' % \
				(edu[ 'school' ], edu[ 'orgunit' ], edu[ 'city' ], country, edu[ 'start' ], edu[ 'end' ]) )
		self.wrln( '|=============' )
		self.wrln( "" )
		
		
	def writeLanguages(self, model):
		self.wrln( '== Languages ==' )
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
		self.wrln( '== Hobbies ==' )
		hobbies = []
		for values in model.addt.values():
			hobbies += values
		self.wrln( ", ".join(hobbies) + "." )
		self.wrln( "" )
		
		
	def writeReferences(self, model):
		self.wrln( '== References ==' )
		self.wrln( self.lookup(self.lang, Lkp.referenceRequestMap) )
		self.wrln( "" )


	def wr(self, s):
		self.outFile.write(s.encode('utf-8'))


	def wrln(self, s):
		self.wr(s + '\n')
