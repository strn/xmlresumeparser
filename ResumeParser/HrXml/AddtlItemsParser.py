#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class AddtlItemsParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.addt = {}


	def parse(self, addtList):
		if addtList == []:
			return
		itemType = ''
		
		for item in addtList:
			for elem in item.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'ResumeAdditionalItem':
					itemType = elem.attrib.get( 'type' )
					if not self.addt.has_key( itemType ):
						self.addt[ itemType ] = []
				elif tag == 'Description':
					self.addt[ itemType ].append( elem.text )
				#print "%s (%d): %s" % (tag, len(elem), name)
		### for


	def __repr__(self):
		retstr = "<AddtlItemsParser: %s>" % self.addt
		return retstr.encode( 'utf-8' )
		

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	from pprint import pprint
	testXml = """
	<ResumeAdditionalItems>
		<ResumeAdditionalItem type="Interests">
			<EffectiveDate>
				<StartDate>
					<Year>2013</Year>
				</StartDate>
			</EffectiveDate>
	        <Description>Typewriter collecting</Description>
	    </ResumeAdditionalItem>
		<ResumeAdditionalItem type="Hobbies">
	        <Description>Traveling</Description>
	    </ResumeAdditionalItem>
	    <ResumeAdditionalItem type="Hobbies">
	        <Description>Cycling</Description>
	    </ResumeAdditionalItem>
	    <ResumeAdditionalItem type="Hobbies">
	        <Description>Mountain hiking</Description>
	    </ResumeAdditionalItem>
	</ResumeAdditionalItems>
	"""
	parser = AddtlItemsParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	pprint (parser.addt)
