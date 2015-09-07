#!/usr/bin/python
# -*- coding: utf-8 -*-


from   odf.opendocument import OpenDocumentText
from   odf.style import FontFace, ListLevelProperties, ParagraphProperties, Style, TextProperties
from   odf.text import List, ListItem, ListLevelStyleBullet, ListStyle, P, Span
from   pprint import pprint
import sys
from   BaseWriter import BaseWriter
import ResumeWriter.Util.Lookup as Lkp



class ResumeWriter(BaseWriter):
	
	"""
	Open Document Format writer
	"""

	def __init__(self, filename=None):
		# This number says how many jobs in job history
		# will be listed in full (with all details)
		# The rest will be mentioned just by employer name
		if filename == None:
			print "(E) Can't output ODF file to STDOUT, exiting ..."
			sys.exit(2)
		else:
			self.doc = OpenDocumentText()
		self.filename = filename
		self.jobDivide = 2


	def __del__(self):
		# File name must be in Unicode format
		self.doc.save( u"" + self.filename, True )


	def write(self, model=None, lang='en_GB', withPhoto=False, personalData=False, experience=False):
		if model == None:
			self.wrln( "Empty resume model." )
			return
		self.lang = lang
		self.withPhoto = withPhoto
		self.personalData = personalData
		self.experience = experience
		self.initDocStyles()
		self.writeHeader(model)
		#self.writeAddress(model)
		#self.writeSummary(model)
		#self.writeSkills(model)
		#self.writeEmployment(model)
		#self.writeCertifications(model)
		#self.writeEducation(model)
		#self.writeLanguages(model)
		#self.writeHobbies(model)
		#self.writeReferences(model)


	# Initialization of document styles
	def initDocStyles(self):
		# font
		self.doc.fontfacedecls.addElement((FontFace(name="Arial", \
			fontfamily="Arial", fontsize="11", fontpitch="variable", \
			fontfamilygeneric="swiss")))

		# styles
		styleStandard = Style(name="Standard", family="paragraph", attributes={"class":"text"})
		styleStandard.addElement(ParagraphProperties(punctuationwrap="hanging", \
			writingmode="page", linebreak="strict"))
		styleStandard.addElement( TextProperties(fontname="Arial", fontsize="11pt") )
		self.doc.styles.addElement(styleStandard)
		
		# automatic styles
		styleNormal = Style(name="ResumeText", parentstylename="Standard", family="paragraph")
		self.doc.automaticstyles.addElement(styleNormal)
		
		styleBoldText = Style(name="ResumeBoldText", parentstylename="Standard", family="text")
		styleBoldText.addElement( TextProperties(fontweight="bold") )
		self.doc.automaticstyles.addElement( styleBoldText )

		styleListText = ListStyle(name="ResumeListText")
		styleListBullet = ListLevelStyleBullet(level="1", stylename="ResumeListTextBullet", \
			numsuffix=".", bulletchar=u'\u2022')
		styleListBullet.addElement( ListLevelProperties(spacebefore="0.1in", minlabelwidth="0.2in") )
		styleListText.addElement(styleListBullet)
		self.doc.automaticstyles.addElement(styleListText)
		
		styleBoldPara = Style(name="ResumeH2", parentstylename="Standard", family="paragraph")
		styleBoldPara.addElement( TextProperties(fontweight="bold") )
		self.doc.automaticstyles.addElement(styleBoldPara)
		
		styleBoldCenter = Style(name="ResumeH1", parentstylename="Standard", family="paragraph")
		styleBoldCenter.addElement( TextProperties(fontweight="bold") )
		styleBoldCenter.addElement( ParagraphProperties(textalign="center") )
		self.doc.automaticstyles.addElement(styleBoldCenter)


	def writeHeader(self, model):
		self.doc.text.addElement(P(text="Ime Prezime", stylename="ResumeH1"))
		self.doc.text.addElement(P(text="Adresa", stylename="ResumeH2"))
