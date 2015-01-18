#!/usr/bin/python
# -*- coding: utf-8 -*-

class HrXml:
	
	def __init__(self):
		# Contact info
		self.personName = ''
		self.altScript = ''
		self.alternateName = ''
		self.privateEmailAddress = ''
		self.businessEmailAddress = ''
		self.streetAddress = ''
		self.countryCode = ''
		self.postalCode = ''
		self.region = ''
		self.municipality = ''
		self.privatePhone = ''
		self.mobilePhone = ''
		# Executive summary
		self.execS = []
		# Objective
		self.objct = []
		# Educational history
		self.edu = []
		# Employment history
		self.empl = []
		# Certifications
		self.cert = []
		# References
		self.ref = []
		# Additional items
		self.addt = {}
		# Human languages
		self.lang = []
		# Qualifications (skills)
		self.skil = []


	def __repr__(self):
		cnt = "Contact info: personName='%s', alternateScript='%s', alternateName='%s', privateEmailAddress='%s', businessEmailAddress='%s', streetAddress='%s', countryCode='%s', postalCode='%s', region='%s', municipality='%s', privatePhone='%s', mobilePhone='%s'" % (self.personName, self.altScript, self.alternateName, self.privateEmailAddress, \
			self.businessEmailAddress, self.streetAddress, self.countryCode, self.postalCode, \
			self.region, self.municipality,	self.privatePhone, self.mobilePhone)
		ex = "Executive summary: '%s', objective='%s'" % (self.execS, self.objct)
		emp = "Employment history: %s" % self.empl
		edu = "Education history: %s" % self.edu
		cert = "Licenses/certificates: %s" % self.cert
		qly = "Qualifications: %s" % self.skil
		lang = 'Languages: %s' % self.lang
		ref = 'References: %s' % self.ref
		addt = 'Additional items: %s' % self.addt
		ret = '=== HrXml model: ===\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s\r\n=== HrXml model ends ===' % \
			(cnt, ex, emp, edu, cert, qly, lang, ref, addt)
		return ret.encode( 'utf-8' )
