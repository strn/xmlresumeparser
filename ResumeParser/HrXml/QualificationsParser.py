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
		# Arbitrary taken value that represents ID for years of experience
		# Change as you wish, to correspond to values in your XML document
		self.yearsExpTypeId = '7'


	def parse(self, skilList):
		if skilList == []:
			return
		skillDict = {}
		compEvTypeId = ''
		evidenceId = ''
		
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
					required = elem.attrib.get( 'required' )
					compEvTypeId = elem.attrib.get( 'typeId' )
					self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'started' ] = started
					self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'lastUsed' ] = lastUsed
					self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'required' ] = required
				elif tag == 'NumericValue':
					# See what previous tag is
					parentTag = self.removeNS( elem.getparent().tag )
					if parentTag == 'CompetencyWeight':
						# Add attributes and text as mesurement of competency
						self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'compLvlMin' ] =  elem.attrib.get( 'minValue' )
						self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'compLvlMax' ] =  elem.attrib.get( 'maxValue' )
						self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'compLvl' ] = elem.text
					elif parentTag == 'CompetencyEvidence':
						if compEvTypeId == evidenceId == self.yearsExpTypeId:
							self.skil[ taxGroupId ][ 'skills' ][ skill ][ 'yrsExp' ] = elem.text
				elif tag == 'EvidenceId':
					evidenceId = elem.attrib.get( 'id' )
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
					<EvidenceId description="Years of Experience in Competency" id="7" idOwner="Self" />
					<NumericValue description="Range in years for experience">4</NumericValue>
				</CompetencyEvidence>
				<CompetencyWeight type="skillLevel">
					<NumericValue description="1" maxValue="10" minValue="1">9</NumericValue>
		       </CompetencyWeight>
			</Competency>
			<Competency name="JEE">
				<TaxonomyId idOwner="Skill" id="" />
				<CompetencyEvidence dateOfIncident="2001-08-23" name="Years of Experience" typeDescription="Years of Experience" typeId="7">
				</CompetencyEvidence>
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
