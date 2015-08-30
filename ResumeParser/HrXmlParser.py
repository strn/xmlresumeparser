#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from lxml import etree

from HrXml import AddtlItemsParser, CertificationParser, ContactInfoParser, EducationHistoryParser
from HrXml import EmploymentHistoryParser, ExecutiveSummaryParser, LanguageParser, QualificationsParser
from HrXml import ReferenceParser, NonXmlResumeParser, PersonalDataParser
from ResumeModel import HrXml
from Util.Namespace import NAMESPACEMAP


class ResumeParser():
	
	def __init__(self, inputFile):
		# File existence checked previously
		self.input = codecs.open( inputFile, 'rb', 'utf-8' )
		self.root = etree.parse(inputFile).getroot()
		self.model = HrXml.HrXml()
		self.persDataXPath = '/ns:Candidate/ns:CandidateProfile/ns:PersonalData'
		self.persDataParser = PersonalDataParser.PersonalDataParser()
		self.certXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:LicensesAndCertifications/ns:LicenseOrCertification'
		self.certParser = CertificationParser.CertificationParser()
		self.contMethXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:ContactInfo/ns:ContactMethod'
		self.persNameXpath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:ContactInfo/ns:PersonName'
		self.contParser = ContactInfoParser.ContactInfoParser()
		self.execSumXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:ExecutiveSummary'
		self.execSumParser = ExecutiveSummaryParser.ExecutiveSummaryParser()
		self.employmentXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:EmploymentHistory/ns:EmployerOrg'
		self.emplParser = EmploymentHistoryParser.EmploymentHistoryParser()
		self.eduXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:EducationHistory/ns:SchoolOrInstitution'
		self.eduParser = EducationHistoryParser.EducationHistoryParser()
		self.langXPAth = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:Languages/ns:Language'
		self.langParser = LanguageParser.LanguageParser()
		self.skilXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:Qualifications/ns:Competency'
		self.skilParser = QualificationsParser.QualificationsParser()
		self.refXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:References/ns:Reference'
		self.refParser  = ReferenceParser.ReferenceParser()
		self.addtlXPath = '/ns:Candidate/ns:Resume/ns:StructuredXMLResume/ns:ResumeAdditionalItems/ns:ResumeAdditionalItem'
		self.addtlParser = AddtlItemsParser.AddtlItemsParser()
		self.nonResXPath = '/ns:Candidate/ns:Resume/ns:NonXMLResume/ns:SupportingMaterials'
		self.nonResXmlParser = NonXmlResumeParser.NonXmlResumeParser()
		

	def __del__(self):
		self.input.close()


	def parse(self):
		# Personal data
		persDataList = self.root.xpath(self.persDataXPath, namespaces = NAMESPACEMAP)
		self.persDataParser.parse( persDataList )
		# Personal name
		nameList = self.root.xpath(self.persNameXpath, namespaces = NAMESPACEMAP)
		self.contParser.personNameParse( nameList )
		# Contact methods
		methodList = self.root.xpath(self.contMethXPath, namespaces = NAMESPACEMAP)
		self.contParser.contactMethodParse( methodList )
		# Contact data
		contDataList = self.root.xpath(self.nonResXPath, namespaces = NAMESPACEMAP)
		self.nonResXmlParser.parse( contDataList )
		# Executive summary and objective
		execSumList = self.root.xpath(self.execSumXPath, namespaces = NAMESPACEMAP)
		self.execSumParser.parse( execSumList )
		# Employment history
		emplList = self.root.xpath(self.employmentXPath, namespaces = NAMESPACEMAP)
		self.emplParser.parse( emplList )
		# Education history
		eduList = self.root.xpath(self.eduXPath, namespaces = NAMESPACEMAP)
		self.eduParser.parse( eduList )
		# Licenses and certifications
		certList = self.root.xpath(self.certXPath, namespaces = NAMESPACEMAP)
		self.certParser.parse( certList )
		# Qualifications (skills)
		skilList = self.root.xpath(self.skilXPath, namespaces = NAMESPACEMAP)
		self.skilParser.parse( skilList )
		# Languages
		langList = self.root.xpath(self.langXPAth, namespaces = NAMESPACEMAP)
		self.langParser.parse( langList )
		# References
		refList = self.root.xpath(self.refXPath, namespaces = NAMESPACEMAP)
		self.refParser.parse( refList )
		# Additional items
		addtList = self.root.xpath(self.addtlXPath, namespaces = NAMESPACEMAP)
		self.addtlParser.parse( addtList )
		

	def getModel(self):
		# Copy all fields to model
		#
		# Personal data
		self.model.dateOfBirth = self.persDataParser.dateOfBirth
		self.model.nationality = self.persDataParser.nationality
		self.model.maritalStatus = self.persDataParser.maritalStatus
		# Contact info
		self.model.personName = self.contParser.personName
		self.model.altScript = self.contParser.altScript
		self.model.alternateName = self.contParser.alternateName
		self.model.privateEmailAddress = self.contParser.privateEmailAddress
		self.model.businessEmailAddress = self.contParser.businessEmailAddress
		self.model.streetAddress = self.contParser.streetAddress
		self.model.countryCode = self.contParser.countryCode
		self.model.postalCode = self.contParser.postalCode
		self.model.region = self.contParser.region
		self.model.municipality = self.contParser.municipality
		self.model.privatePhone = self.contParser.privatePhone
		self.model.mobilePhone = self.contParser.mobilePhone
		# Person photo and description
		self.model.personPhoto = self.nonResXmlParser.personPhoto
		self.model.personPhotoType = self.nonResXmlParser.personPhotoType
		self.model.personPhotoDesc = self.nonResXmlParser.personPhotoDesc
		# Executive summary and objective
		self.model.execS = self.execSumParser.execS
		self.model.objct = self.execSumParser.objct
		# Employment history
		self.model.empl = self.emplParser.empl
		# Education history
		self.model.edu = self.eduParser.edu
		# Licenses and certifications
		self.model.cert = self.certParser.cert
		# Qualifications (skills)
		self.model.skil = self.skilParser.skil
		# Languages
		self.model.lang = self.langParser.lang
		# References
		self.model.ref = self.refParser.ref
		# Additional items
		self.model.addt = self.addtlParser.addt
		return self.model
###   HrXmlResumeParser end ###


if __name__ == "__main__":
	print "Testing HrXmlResumeParser ..."
	print
	parser = HrXmlResumeParser('example2.xml')
	parser.parse()
