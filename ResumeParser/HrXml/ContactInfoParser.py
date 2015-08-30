#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser
from lxml.etree import Comment


class ContactInfoParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	def __init__(self):
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


	def personNameParse(self, nameList):
		if nameList == []:
			return
		name = ''
		surname = ''
		altName = ''
		altSurname = ''
		for personName in nameList:
			for elem in personName.iter():
				if elem.tag is Comment:
					continue
				tag = self.removeNS(elem.tag)
				if tag == 'FormattedName':
					if self.altScript == '':
						self.personName = elem.text
					else:
						self.alternateName = elem.text
				elif tag == 'GivenName':
					if self.altScript == '':
						name = elem.text
					else:
						altName = elem.text
				elif tag == 'FamilyName':
					primary = elem.attrib.get("primary")
					if str(primary) == 'true':
						if self.altScript == '':
							surname = elem.text
						else:
							altSurname = elem.text
				elif tag == 'AlternateScript':
					self.altScript = elem.attrib.get("script")
				#print "%s: %s" % (tag, elem.text)
		if self.personName == '':
			self.personName = "%s %s" % (name, surname)
			self.personName = self.personName.strip()
		if self.alternateName == '':
			self.alternateName = "%s %s" % (altName, altSurname)
			self.alternateName = self.alternateName.strip()
	### personNameParse ###


	def contactMethodParse(self, methodList):
		if methodList == []:
			return
		contMethUse = ''
		streetName = ''
		buildingNumber = ''
		isTelephone = False
		isMobile = False
		
		for contactMethod in methodList:
			for elem in contactMethod.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'Use':
					contMethUse = elem.text
				elif tag == 'InternetEmailAddress':
					if contMethUse == 'personal':
						self.privateEmailAddress = elem.text
					elif contMethUse == 'business':
						self.businessEmailAddress = elem.text
				elif tag == 'CountryCode' and contMethUse == 'personal':
					self.countryCode = elem.text
				elif tag == 'PostalCode' and contMethUse == 'personal':
					self.postalCode = elem.text
				elif tag == 'Region' and contMethUse == 'personal':
					self.region = elem.text
				elif tag == 'Municipality' and contMethUse == 'personal':
					self.municipality = elem.text
				elif tag == 'StreetName' and contMethUse == 'personal':
					streetName = elem.text
				elif tag == 'BuildingNumber' and contMethUse == 'personal':
					buildingNumber = elem.text
				elif tag == 'Telephone' and contMethUse == 'personal':
					isTelephone = True
					isMobile = False
				elif tag == 'Mobile':
					isMobile = True
					isTelephone = False
				elif tag == 'FormattedNumber' and isTelephone:
					self.privatePhone = elem.text
					isTelephone = False
				elif tag == 'FormattedNumber' and isMobile:
					self.mobilePhone = elem.text
					isMobile = False
				#print "%s: %s" % (elem.tag, elem.text)
			### for
		### for
		self.streetAddress = "%s %s" % (streetName, buildingNumber)
		# TODO: Implement feature for formatting street address and number
		# based on some configuration setting
		self.streetAddress = self.streetAddress.strip()
	### contactMethodParse ###


	def __repr__(self):
		retstr = u"<ContactInfoParser: personName='%s', alternateScript='%s', alternateName='%s', privateEmailAddress='%s', businessEmailAddress='%s', streetAddress='%s', countryCode='%s', postalCode='%s', region='%s', municipality='%s', privatePhone='%s', mobilePhone='%s'>" % \
			(self.personName, self.altScript, self.alternateName, self.privateEmailAddress, \
			self.businessEmailAddress, self.streetAddress, self.countryCode, self.postalCode, \
			self.region, self.municipality, self.privatePhone, self.mobilePhone)
		return retstr.encode( 'utf-8' )
	### __repr__ ###
	

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testPersonXml = u"""
	<PersonName>
		<FormattedName>Bilbo Bagins</FormattedName>
		<GivenName>Bilbo</GivenName>
		<FamilyName primary="true">Bagins</FamilyName>
		<AlternateScript script="Cyrl">
			<FormattedName>Билбо Багинс</FormattedName>
			<GivenName>Билбо</GivenName>
			<FamilyName primary="true">Багинс</FamilyName>
		</AlternateScript>
	</PersonName>
	"""
	parser = ContactInfoParser()
	root = etree.fromstring(testPersonXml)
	parser.personNameParse(root)
	testContactXml = """
	<ContactInfo>
		<ContactMethod>
			<Use>personal</Use>
			<Location>home</Location>
			<WhenAvailable>evenings</WhenAvailable>
			<Telephone>
				<FormattedNumber>+41 (0)43 123 4567</FormattedNumber>
			</Telephone>
			<InternetEmailAddress>bbagins@gmail.com</InternetEmailAddress>
			<PostalAddress type="streetAddress">
				<CountryCode>CH</CountryCode>
				<PostalCode>8123</PostalCode>
				<Region>Zürich</Region>
				<Municipality>Oerlikon</Municipality>
				<DeliveryAddress>
					<StreetName>Akaciastrasse</StreetName>
					<BuildingNumber>3</BuildingNumber>
				</DeliveryAddress>
				<Recipient>
					<PersonName>
						<FormattedName>Bilbo Bagins</FormattedName>
					</PersonName>
					<AdditionalText/>
					<OrganizationName/>
				</Recipient>
			</PostalAddress>
		</ContactMethod>
		
		<ContactMethod>
			<Use>business</Use>
			<Location>onPerson</Location>
			<WhenAvailable>weekdays</WhenAvailable>
			<Mobile smsEnabled="true">
				<FormattedNumber>+41 (0)76 456 7890</FormattedNumber>
			</Mobile>
		</ContactMethod>
	</ContactInfo>
	"""
	root = etree.fromstring(testContactXml)
	parser.contactMethodParse(root)
	print parser
