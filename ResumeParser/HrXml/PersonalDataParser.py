#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser
from lxml.etree import Comment


class PersonalDataParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	def __init__(self):
		self.dateOfBirth = ''
		self.nationality = ''
		self.maritalStatus = ''
	
	
	def parse(self, persDataList):
		for item in persDataList:
			for elem in item.iter():
				if elem.tag is Comment:
					continue
				tag = self.removeNS(elem.tag)
				if tag == 'Nationality':
					self.nationality = elem.text.strip()
				elif tag == 'DateOfBirth':
					self.dateOfBirth = elem.text.strip()
				elif tag == 'MaritalStatus':
					self.maritalStatus = elem.text.strip()


	def __repr__(self):
		retstr = u"<PersonalDataParser: dateOfBirth='%s', nationality='%s', maritalStatus='%s'>" % \
			(self.dateOfBirth, self.nationality, self.maritalStatus)
		return retstr.encode( 'utf-8' )


if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testPersonXml = u"""
	<PersonalData>
		<PersonDescriptors>
			<LegalIdentifiers>
				<PersonLegalId validFrom="1928-01-01" countryCode="CA">
					<IdValue name="SIN">123456789</IdValue>
				</PersonLegalId>
				<MilitaryStatus>Retired</MilitaryStatus>
				<VisaStatus countryCode="CH" validFrom="2000-01-01" validTo="2005-01-01">Active</VisaStatus>
				<Citizenship>RU</Citizenship>
				<Residency>US</Residency>
			</LegalIdentifiers>
			
			<DemographicDescriptors>
				<Race>White</Race>
				<Ethnicity>Russian</Ethnicity>
				<Nationality>CA</Nationality>
				<PrimaryLanguage>UZ</PrimaryLanguage>
				<BirthPlace>Moscow, CCCP</BirthPlace>
				<Religion>Orthodox</Religion>
				<MaritalStatus>Unmarried</MaritalStatus>
				<ChildrenInfo>
					<NumberOfChildren>3</NumberOfChildren>
				</ChildrenInfo>
			</DemographicDescriptors>
			<BiologicalDescriptors>
				<DateOfBirth>1968-05-28</DateOfBirth>
				<GenderCode>1</GenderCode>
				<EyeColor>Brown</EyeColor>
				<HairColor>Brown</HairColor>
				<Height unitOfMeasure="centimetres">180</Height>
			</BiologicalDescriptors>
		</PersonDescriptors>
	</PersonalData>
	"""
	parser = PersonalDataParser()
	root = etree.fromstring(testPersonXml)
	parser.parse(root)
	print parser
