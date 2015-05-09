#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Namespace import NAMESPACEMAP

# Dictionary that converts month's ordinal number to name
# in particular language
monthDict = {
	'en' : [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ],
	'de' : [ 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember' ],
	'sr' : [ 'јануар', 'фебруар', 'март', 'април', 'мај', 'јун', 'јул', 'август', 'септембар', 'октобар', 'новембар', 'децембар' ]
}
		
class BaseParser:

	"""
	This class contains base utility methods, required in all classes
	"""


	def removeNS(self, tag):
		"""
		Removes namespace from tag
		Returns: clean name
		"""
		i = tag.find('}')
		if i >= 0:
			tag = tag[i+1:]
		return tag


	def text2lines(self, text, delim='\n'):
		"""
		Breaks text to lines, stripping whitespace
		Returns: list of text lines
		"""
		return filter(None, map((lambda x: x.strip()), text.split( delim )))


	def getMonthYear(self, date, lang='en'):
		"""
		Returns: date converted to human readable form
		"""
		dateList = date.split( '-' )
		return '%s %s' % ( monthDict[lang][int(dateList[1])-1], dateList[0] )


if __name__ == "__main__":
	parser = BaseParser()
	tag = '{namesp}tag'
	print 'Tag with namespace:',tag
	print 'After removing namespace:',parser.removeNS( tag )
	text = """
	
		One line
		Two lines
		Three lines
		
		
	"""
	print 'Text to lines:',parser.text2lines(text)
	dt = '1923-05-17'
	print 'Date:',dt
	print 'Date in Serbian:',parser.getMonthYear(dt, 'sr')
	print 'Date in German:',parser.getMonthYear(dt, 'de')
	print 'Date in English:',parser.getMonthYear(dt)
