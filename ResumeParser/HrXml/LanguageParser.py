#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class LanguageParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.lang = []


	def parse(self, langList):
		if langList == []:
			return
		langDict = {}
		
		for lang in langList:
			for elem in lang.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'Language' and langDict != {}:
					self.lang.append( langDict )
					langDict = {}
				elif tag == 'LanguageCode':
					langDict[ 'code' ] = elem.text
				elif tag == 'Read':
					langDict[ 'read' ] = elem.text
				elif tag == 'Write':
					langDict[ 'write' ] = elem.text
				elif tag == 'Speak':
					langDict[ 'speak' ] = elem.text
				elif tag == 'Comments':
					langDict[ 'comments' ] = elem.text
				#print "%s: %s" % (tag, elem.text)
		### for
		# Not to forget last language
		self.lang.append( langDict )
		

	def __repr__(self):
		retstr = "<LanguageParser: %s>" % self.lang
		return retstr.encode( 'utf-8' )
		

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testXml = """
	<Languages>
		<Language>
			<LanguageCode>SR</LanguageCode>
			<Read>true</Read>
			<Write>true</Write>
			<Speak>true</Speak>
			<Comments>Mother tongue</Comments>
		</Language>
	</Languages>
	"""
	parser = LanguageParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	print parser
