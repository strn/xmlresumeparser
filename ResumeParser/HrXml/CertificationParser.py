#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class CertificationParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.cert = []


	def parse(self, certList):
		if certList == []:
			return
		certDict = {}
		
		for cert in certList:
			for elem in cert.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'LicenseOrCertification' and certDict != {}:
					self.cert.append( certDict )
					certDict = {}
				elif tag == 'Name':
					certDict[ 'name' ] = elem.text
				elif tag == 'IssuingAuthority':
					certDict[ 'auth' ] = elem.text
				elif tag == 'Description':
					certDict[ 'desc' ] = elem.text
				elif tag in ( 'AnyDate', 'YearMonth' ):
					certDict[ 'issued' ] = self.getMonthYear(elem.text)
				elif tag == 'StringDate':
					certDict[ 'issued' ] = elem.text
				#print "%s: %s" % (tag, elem.text)
		### for
		# Not to forget last certificate
		self.cert.append( certDict )
		

	def __repr__(self):
		retstr = "<CertificationParser: %s>" % self.cert
		return retstr.encode( 'utf-8' )
		

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testXml = """
	<LicensesAndCertifications>
		<LicenseOrCertification>
			<Name>Ordinary Wizard Level</Name>
			<IssuingAuthority>Hogworts School For Witchcraft And Wizardry</IssuingAuthority>
			<Description>Ordinary Wizard Level</Description>
			<EffectiveDate>
				<FirstIssuedDate>
					<YearMonth>2011-07</YearMonth>
				</FirstIssuedDate>
			</EffectiveDate>
		</LicenseOrCertification>
	</LicensesAndCertifications>
	"""
	parser = CertificationParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	print parser
