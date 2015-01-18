#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class ExecutiveSummaryParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.execS = []
		self.objct = []


	def parse(self, execSumList):
		if execSumList == []:
			return
		for execSum in execSumList:
			for elem in execSum.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'ExecutiveSummary':
					self.execS = self.text2lines(elem.text)
				elif tag == 'Objective':
					self.objct = self.text2lines(elem.text)
				#print "%s: %s" % (tag, elem.text)


	def __repr__(self):
		retstr = "<ExecutiveSummaryParser: execSumm='%s', objective='%s'>" % (self.execS, self.objct)
		return retstr.encode( 'utf-8' )


if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	testXml = u"""
	<StructuredXMLResume>
		<ExecutiveSummary>
			This is an executive summary
			in multiple lines.
		</ExecutiveSummary>
		<Objective>
			This is multi-line objective
			than can also come handy
		</Objective>
	</StructuredXMLResume>
	"""
	parser = ExecutiveSummaryParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	print parser
