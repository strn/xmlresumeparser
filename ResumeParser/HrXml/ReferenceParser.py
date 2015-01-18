#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class ReferenceParser(BaseParser):

	"""
	Placeholder for documentation
	"""

	def __init__(self):
		self.ref = []
		

	def parse(self, refList):
		if refList == []:
			return
		refDict = {}
		addrUse = ''

		for ref in refList:
			for elem in ref.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'Reference' and refDict != {}:
					self.ref.append( refDict )
					refDict = {}
				elif tag == 'FormattedName' and not refDict.has_key( 'name' ):
					refDict[ 'name' ] = elem.text
				elif tag == 'Use':
					addrUse = elem.text
				elif tag == 'InternetEmailAddress' and addrUse == 'business':
					refDict[ 'email' ] = elem.text
				elif tag == 'PositionTitle':
					refDict[ 'title' ] = elem.text
				elif tag == 'Comments':
					refDict[ 'comments' ] = elem.text
				#print "%s: %s" % (tag, elem.text)
			### for
		### for
		# Not to forget last reference
		self.ref.append( refDict )
	### parse ###


	def __repr__(self):
		retstr = "<ReferenceParser: %s>" % self.ref
		return retstr


if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testXml = u"""
	<References>
		<Reference type="Professional">
			<PersonName>
				<FormattedName>Gandalf The Grey</FormattedName>
			</PersonName>
			<PositionTitle>Wizard-master</PositionTitle>
			<ContactMethod>
				<Use>business</Use>
				<Location>office</Location>
				<InternetEmailAddress>gandalf.grey@middle-earth.com</InternetEmailAddress>
			</ContactMethod>
			<Comments>Line manager from 2010 to 2013.</Comments>
		</Reference>
		<Reference type="Professional">
			<PersonName>
				<FormattedName>Saruman The White</FormattedName>
			</PersonName>
			<PositionTitle>Wizard-master</PositionTitle>
			<ContactMethod>
				<Use>business</Use>
				<Location>office</Location>
				<InternetEmailAddress>saruman.white@middle-earth.com</InternetEmailAddress>
			</ContactMethod>
			<ContactMethod>
				<Use>personal</Use>
				<Location>home</Location>
				<InternetEmailAddress>saruman.white@orthanc.com</InternetEmailAddress>
			</ContactMethod>
			<Comments>Direct line manager from 2006 to 2008.</Comments>
		</Reference>
		<Reference type="Personal">
			<PersonName>
				<FormattedName>Bilbo Bagins</FormattedName>
				<AlternateScript script="Cyrl">
					<FormattedName>Билбо Багинс</FormattedName>
				</AlternateScript>
			</PersonName>
			<ContactMethod>
				<Use>personal</Use>
				<Location>home</Location>
				<InternetEmailAddress>bilbo4@gmail.com</InternetEmailAddress>
			</ContactMethod>
			<ContactMethod>
				<Use>business</Use>
				<Location>office</Location>
				<InternetEmailAddress>Bilbo.Bagins@hobbiton.com</InternetEmailAddress>
			</ContactMethod>
			<Comments>Very good and close friend.</Comments>
		</Reference>
	</References>
	"""
	parser = ReferenceParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	print parser
