#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser


class QualificationsParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.skil = []


	def parse(self, skilList):
		if skilList == []:
			return
		tmpList = []
		
		for skil in skilList:
			for elem in skil.iter():
				tag = self.removeNS(elem.tag)
				if tag == 'Competency':
					name = elem.attrib.get( 'name' )
					if len(elem) > 0 and tmpList != []:
						self.skil.append( tmpList )
						tmpList = []
					tmpList.append( name )
				#print "%s (%d): %s" % (tag, len(elem), name)
		### for
		self.skil.append( tmpList )

	def __repr__(self):
		retstr = "<QualificationsParser: %s>" % self.skil
		return retstr.encode( 'utf-8' )
		

if __name__ == "__main__":
	# Run test if invoked as a program
	from lxml import etree
	from pprint import pprint
	testXml = """
	<Qualifications>
		<Competency name="Operating systems">
			<Competency name="UNIX (Solaris)" />
			<Competency name="Linux" />
			<Competency name="Microsoft Windows 7" />
		</Competency>
		<Competency name="Java">
			<Competency name="J2EE" />
			<Competency name="JavaScript" />
			<Competency name="JPA" />
			<Competency name="JMS" />
			<Competency name="JDBC" />
			<Competency name="JUnit" />
			<Competency name="Weblogic 12.1" />
			<Competency name="Spring" />
		</Competency>
		<Competency name="Markup languages">
			<Competency name="XML (SAX and DOM API)" />
			<Competency name="XSLT" />
			<Competency name="HTML" />
			<Competency name="CSS" />
		</Competency>
		<Competency name="Databases">
			<Competency name="Oracle 11g" />
			<Competency name="PL/SQL" />
			<Competency name="MySQL 5.x" />
		</Competency>
		<Competency name="Other languages">
			<Competency name="C" />
			<Competency name="C++" />
			<Competency name="PHP 5.x" />
			<Competency name="Perl 5.x" />
			<Competency name="Python 2.x" />
			<Competency name="Groovy" />
			<Competency name="UML" />
		</Competency>
		<Competency name="Libraries">
			<Competency name="Google Protocol Buffer" />
		</Competency>
		<Competency name="Source control" >
			<Competency name="Subversion" />
		</Competency>
		<Competency name="Collaboration">
			<Competency name="Confluence"/>
			<Competency name="JIRA"/>
		</Competency>
		<Competency name="Tools">
			<Competency name="Ant" />
			<Competency name="Maven" />
		</Competency>
	</Qualifications>
	"""
	parser = QualificationsParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	pprint (parser.skil)
