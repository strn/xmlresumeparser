#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser
from lxml.etree import Comment


class NonXmlResumeParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	def __init__(self):
		self.personPhoto = ''
		self.personPhotoType = ''
		self.personPhotoDesc = ''


	def parse(self, contDataList):
		if contDataList == []:
			return
		photoDesc = ''
		
		for item in contDataList:
			for elem in item.iter():
				if elem.tag is Comment:
					continue
				tag = self.removeNS(elem.tag)
				if tag == 'AttachmentReference':
					context = elem.attrib.get("context")
					if context == 'CandidatePhoto':
						self.personPhotoType = elem.attrib.get("mimeType")
						self.personPhoto = elem.text.strip()
				elif tag == 'Description':
					photoDesc = elem.text.strip()
			if self.personPhoto != '':
				self.personPhotoDesc = photoDesc
	### parse ###


	def __repr__(self):
		retstr = u"<NonXmlResumeParser: personPhoto='%s', personPhotoType='%s', personPhotoDesc='%s'>" % \
			(self.personPhoto, self.personPhotoType, self.personPhotoDesc)
		return retstr.encode( 'utf-8' )
	### __repr__ ###
	

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testPersonNonXmlResumeXml = u"""
		<SupportingMaterials>
			<!-- URI of the photo -->
			<Description>My Picture Description</Description>
			<AttachmentReference context="CandidatePhoto" mimeType="image/jpeg">file:///path/to/MyPicture.jpg</AttachmentReference>
		</SupportingMaterials>
	"""
	parser = NonXmlResumeParser()
	root = etree.fromstring(testPersonNonXmlResumeXml)
	parser.parse(root)
	print parser
