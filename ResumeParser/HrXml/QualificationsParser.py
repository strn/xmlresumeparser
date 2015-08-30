#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseParser import BaseParser
from lxml.etree import Comment


class QualificationsParser(BaseParser):

	"""
	Placeholder for documentation
	"""
	
	def __init__(self):
		self.skil = {}
		self.skilGroup = []


	def parse(self, skilList):
		if skilList == []:
			return
		skillDict = {}
		
		for skil in skilList:
			for elem in skil.iter():
				if elem.tag is Comment:
					continue
				tag = self.removeNS(elem.tag)
				if tag == 'Competency':
					name = elem.attrib.get( 'name' )
				elif tag == 'TaxonomyId':
					taxIdOwner = elem.attrib.get( 'idOwner' )
					if taxIdOwner == 'SkillGroup':
						# Create new key in skill map
						skillGroup = name
						taxGroupId = int(elem.attrib.get( 'id' ))
						if not self.skil.has_key( taxGroupId ):
							self.skil[ taxGroupId ] = {}
							self.skil[ taxGroupId ][ 'skillGroup' ] = skillGroup
							self.skil[ taxGroupId ][ 'skills' ] = {}
					elif taxIdOwner == 'Skill':
						skill = name
						# Append to skill dictionary
						self.skil[ taxGroupId ][ 'skills' ][ skill ] = {}
				elif tag == 'CompetencyEvidence':
					lastUsed = elem.attrib.get( 'lastUsed' )
					started = elem.attrib.get( 'dateOfIncident' )
					self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'started' ] = started
					self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'lastUsed' ] = lastUsed
				#print "%s (%d): %s" % (tag, len(elem), name)
		### for
		#self.skil.append( tmpList )


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
			<TaxonomyId idOwner="SkillGroup" id="1" />
			<Competency name="UNIX (Solaris)">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="Linux">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="Microsoft Windows 7">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
		</Competency>
		<Competency name="Architecture" >
			<TaxonomyId idOwner="SkillGroup" id="2" />
			<Competency name="OOD">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="REST">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
		</Competency>
		<Competency name="Java Core">
			<TaxonomyId idOwner="SkillGroup" id="3" />
			<Competency name="JSE 1.4">
				<TaxonomyId idOwner="Skill" id="" />
				<CompetencyEvidence dateOfIncident="2001-08-23" name="Years of Experience" typeDescription="Years of Experience" typeId="7" lastUsed="2001-08-23">
					<EvidenceId description="Years of Experience in Competency" id="7" idOwner="Self"/>
					<NumericValue description="Range in years for experience">4</NumericValue>
				</CompetencyEvidence>
				<CompetencyWeight type="skillLevel">
					<NumericValue description="1" maxValue="10" minValue="0">90</NumericValue>
		       </CompetencyWeight>
			</Competency>
			<Competency name="JEE">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="JavaScript">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="JSP">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
			<Competency name="JDBC">
				<TaxonomyId idOwner="Skill" id="" />
			</Competency>
		</Competency>
	</Qualifications>
	"""
	parser = QualificationsParser()
	root = etree.fromstring(testXml)
	parser.parse(root)
	pprint (parser.skil)
