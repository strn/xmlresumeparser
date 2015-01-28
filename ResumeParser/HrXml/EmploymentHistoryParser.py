#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class EmploymentHistoryParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.empl = []


	def parse(self, emplList):
		if emplList == []:
			return
		empDict = {}
		empDict[ 'job' ] = []
		jobDict = {}
		dateType = ''

		for empl in emplList:
			for elem in empl.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'EmployerOrg' and len(empDict) > 1:
					empDict[ 'job' ].append( jobDict )
					self.empl.append( empDict )
					empDict = {}
					empDict[ 'job' ] = []
					jobDict = {}
				elif tag == 'EmployerOrgName':
					empDict[ 'name' ] = elem.text
				elif tag == 'Municipality':
					empDict[ 'city' ] = elem.text
				elif tag == 'CountryCode':
					empDict[ 'cntr' ] = elem.text
				elif tag == 'PositionHistory' and jobDict != {}:
					empDict[ 'job' ].append( jobDict )
					jobDict = {}
				elif tag == 'Title':
					jobDict[ 'title' ] = elem.text
				elif tag == 'OrganizationName':
					jobDict[ 'dept' ] = elem.text
				elif tag == 'Description':
					jobDict[ 'desc' ] = self.text2lines(elem.text)
				elif tag == 'StartDate':
					dateType = 'start'
				elif tag == 'EndDate':
					dateType = 'end'
				elif tag in ( 'AnyDate', 'YearMonth' ):
					jobDict[ dateType ] = self.getMonthYear(elem.text)
				elif tag == 'StringDate':
					jobDict[ dateType ] = elem.text
				#print "%s: %s" % (tag, elem.text)
		# Not to forget last job and employer
		empDict[ 'job' ].append( jobDict )
		self.empl.append( empDict )

	def __repr__(self):
		retstr = "<EmploymentHistoryParser: empl='%s'>" % self.empl
		return retstr.encode( 'utf-8' )


if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	from pprint import pprint
	testXml = u"""
	<EmploymentHistory>
		<EmployerOrg employerOrgType="soleEmployer">
			<EmployerOrgName>ACME Ltd</EmployerOrgName>
			<EmployerContactInfo contactType="HRRep">
				<ContactMethod>
					 <InternetWebAddress>https://www.acme.com/</InternetWebAddress>
				 </ContactMethod>
				<LocationSummary>
					<Municipality>Springfield</Municipality>
					<Region>California</Region>
					<CountryCode>US</CountryCode>
				</LocationSummary>
			</EmployerContactInfo>
			
			<PositionHistory positionType="directHire" currentEmployer="true">
				<Title>Explosive Engineer</Title>
				<OrgName>
					<OrganizationName>Explosives IT</OrganizationName>
				</OrgName>
				<Description>
					- Designed explosives.
					- Tested explosives by outsourcing them to Wild E. Coyote.
				</Description>
				<StartDate>
					<AnyDate>2013-07-01</AnyDate>
				</StartDate>
			</PositionHistory>
			
			<PositionHistory positionType="directHire" currentEmployer="false">
				<Title>Senior Firecracker Developer</Title>
				<OrgName>
					<OrganizationName>Firecracker Unit</OrganizationName>
				</OrgName>
				<Description>
					- Developed and tested FireCracker Jumbo using JRocket Test framework.
					- Fired firecrackers on weddings.
				</Description>
				<StartDate>
					<AnyDate>2009-05-01</AnyDate>
				</StartDate>
				<EndDate>
					<AnyDate>2013-06-30</AnyDate>
				</EndDate>
			</PositionHistory>
			
			<PositionHistory positionType="directHire" currentEmployer="false">
				<Title>Junior Rocket Developer</Title>
				<OrgName>
					<OrganizationName>Rocket Unit</OrganizationName>
				</OrgName>
				<Description>
					- Rocket activity 1.
					- Rocket activity 2.
					- Rocket activity 3.
				</Description>
				<StartDate>
					<AnyDate>2006-07-01</AnyDate>
				</StartDate>
				<EndDate>
					<AnyDate>2009-04-30</AnyDate>
				</EndDate>
			</PositionHistory>
		</EmployerOrg>
	</EmploymentHistory>
	"""
	parser = EmploymentHistoryParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	pprint( parser.empl )
