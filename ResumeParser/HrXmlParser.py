#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from lxml import etree

from HrXml import AddtlItemsParser, CertificationParser, ContactInfoParser, EducationHistoryParser
from HrXml import EmploymentHistoryParser, ExecutiveSummaryParser, LanguageParser, QualificationsParser
from HrXml import ReferenceParser
from ResumeModel import HrXml
from Util.Namespace import NAMESPACEMAP


class ResumeParser():
	
	def __init__(self, inputFile):
		# File existence checked previously
		self.input = codecs.open( inputFile, 'rb', 'utf-8' )
		self.root = etree.parse(inputFile).getroot()
		self.model = HrXml.HrXml()
		self.certXPath = '/ns:Resume/ns:StructuredXMLResume/ns:LicensesAndCertifications/ns:LicenseOrCertification'
		self.certParser = CertificationParser.CertificationParser()
		self.contMethXPath = '/ns:Resume/ns:StructuredXMLResume/ns:ContactInfo/ns:ContactMethod'
		self.persNameXpath = '/ns:Resume/ns:StructuredXMLResume/ns:ContactInfo/ns:PersonName'
		self.contParser = ContactInfoParser.ContactInfoParser()
		self.execSumXPath = '/ns:Resume/ns:StructuredXMLResume/ns:ExecutiveSummary'
		self.execSumParser = ExecutiveSummaryParser.ExecutiveSummaryParser()
		self.employmentXPath = '/ns:Resume/ns:StructuredXMLResume/ns:EmploymentHistory/ns:EmployerOrg'
		self.emplParser = EmploymentHistoryParser.EmploymentHistoryParser()
		self.eduXPath = '/ns:Resume/ns:StructuredXMLResume/ns:EducationHistory/ns:SchoolOrInstitution'
		self.eduParser = EducationHistoryParser.EducationHistoryParser()
		self.langXPAth = '/ns:Resume/ns:StructuredXMLResume/ns:Languages/ns:Language'
		self.langParser = LanguageParser.LanguageParser()
		self.skilXPath = '/ns:Resume/ns:StructuredXMLResume/ns:Qualifications/ns:Competency'
		self.skilParser = QualificationsParser.QualificationsParser()
		self.refXPath = '/ns:Resume/ns:StructuredXMLResume/ns:References/ns:Reference'
		self.refParser  = ReferenceParser.ReferenceParser()
		self.addtlXPath = '/ns:Resume/ns:StructuredXMLResume/ns:ResumeAdditionalItems/ns:ResumeAdditionalItem'
		self.addtlParser = AddtlItemsParser.AddtlItemsParser()
		

	def __del__(self):
		self.input.close()


	def parse(self):
		# Personal name
		nameList = self.root.xpath(self.persNameXpath, namespaces = NAMESPACEMAP)
		self.contParser.personNameParse( nameList )
		# Contact methods
		methodList = self.root.xpath(self.contMethXPath, namespaces = NAMESPACEMAP)
		self.contParser.contactMethodParse( methodList )
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
		return self.model
###   HrXmlResumeParser end ###


if __name__ == "__main__":
	print "Testing HrXmlResumeParser ..."
	print
	parser = HrXmlResumeParser('example2.xml')
	parser.parse()
