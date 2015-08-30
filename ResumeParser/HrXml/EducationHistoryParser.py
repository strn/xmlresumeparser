#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser
from lxml.etree import Comment


class EducationHistoryParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.edu = []


	def parse(self, eduList):
		if eduList == []:
			return
		eduDict = {}
		dateType = ''

		for educ in eduList:
			for elem in educ.iter():
				if elem.tag is Comment:
					continue
				tag = self.removeNS(elem.tag)
				if tag == 'SchoolOrInstitution' and eduDict != {}:
					self.edu.append( eduDict )
					eduDict = {}
				elif tag == 'SchoolName':
					eduDict[ 'school' ] = elem.text
				elif tag == 'Municipality':
					eduDict[ 'city' ] = elem.text
				elif tag == 'CountryCode':
					eduDict[ 'cntr' ] = elem.text
				elif tag == 'Region':
					eduDict[ 'rgn' ] = elem.text
				elif tag == 'OrganizationUnit':
					eduDict[ 'orgunit' ] = elem.text
				elif tag == 'DegreeDate':
					dateType = 'dgr'
				elif tag == 'DegreeName':
					eduDict[ 'degree' ] = elem.text
				elif tag == 'StartDate':
					dateType = 'start'
				elif tag == 'EndDate':
					dateType = 'end'
				elif tag in ( 'AnyDate', 'YearMonth' ):
					eduDict[ dateType ] = self.getMonthYear(elem.text)
				elif tag == 'StringDate':
					eduDict[ dateType ] = elem.text
				#print "%s: %s" % (tag, elem.text)
		# Not to forget last education
		self.edu.append( eduDict )

	def __repr__(self):
		retstr = "<EducationHistoryParser: empl='%s'>" % self.edu
		return retstr.encode( 'utf-8' )


if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	from pprint import pprint
	testXml = u"""
	<EducationHistory>	
		<SchoolOrInstitution schoolType="">
			<School type="prior">
				<SchoolName>Massachusets Institute of Technology</SchoolName>
			</School>
			<LocationSummary>
				<Municipality>Boston</Municipality>
				<Region>Massachusets</Region>
				<CountryCode>US</CountryCode>
				<PostalCode>12345</PostalCode>
			</LocationSummary>
			<OrganizationUnit organizationType="subSchool">Faculty Of Science</OrganizationUnit>
			<Degree degreeType="bachelors" graduatingDegree="graduating">
				<DegreeName>B. Sc.</DegreeName>
				<DegreeDate>
					<YearMonth>1994-02</YearMonth>
				</DegreeDate>
				<DegreeMajor>
                    <Name>Computer Engineering</Name>
                </DegreeMajor>
                <DegreeMeasure>
		            <EducationalMeasure>
		                <MeasureSystem>GPA</MeasureSystem>
		                <MeasureValue>
		                    <NumericValue>9.06</NumericValue>
		                </MeasureValue>
						<LowestPossibleValue>
							<NumericValue>6.00</NumericValue>
			            </LowestPossibleValue>
			            <HighestPossibleValue>
							<NumericValue>10.00</NumericValue>
			            </HighestPossibleValue>
		                <GoodStudentIndicator>true</GoodStudentIndicator>
		            </EducationalMeasure>
		        </DegreeMeasure>
                <Comments>Thesis: Board Bulletin System (BBS). Advisor: Prof. Elmer Fudge</Comments>
			</Degree>
			<DatesOfAttendance currentlyEnrolled="false">
				<StartDate>
					<YearMonth>1989-10</YearMonth>
				</StartDate>
				<EndDate>
					<YearMonth>1993-10</YearMonth>
				</EndDate>
			</DatesOfAttendance>
			<ISCEDInstitutionClassification>6</ISCEDInstitutionClassification>
		</SchoolOrInstitution>
		
		<SchoolOrInstitution schoolType="">
			<School type="prior">
				<SchoolName>Beverly Hills High</SchoolName>
			</School>
			<LocationSummary>
				<Municipality>Beverly Hills</Municipality>
				<Region>California</Region>
				<CountryCode>US</CountryCode>
				<PostalCode>90210</PostalCode>
			</LocationSummary>
			<OrganizationUnit organizationType="subSchool">High School</OrganizationUnit>
			<Degree degreeType="high school or equivalent" examPassed="true" graduatingDegree="graduating">
				<DegreeName>B. Sc.</DegreeName>
				<DegreeDate>
					<StringDate>Summer 1988</StringDate>
				</DegreeDate>
			</Degree>
			<DatesOfAttendance currentlyEnrolled="false">
				<StartDate>
					<YearMonth>1986-09</YearMonth>
				</StartDate>
				<EndDate>
					<YearMonth>1988-06</YearMonth>
				</EndDate>
			</DatesOfAttendance>
			<ISCEDInstitutionClassification>3</ISCEDInstitutionClassification>
		</SchoolOrInstitution>
	</EducationHistory>
	"""
	parser = EducationHistoryParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	pprint( parser.edu )
