#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import importlib
import optparse
import os.path
import sys


HELPTEXT = "%s <options>" % os.path.normpath(sys.argv[0])

if __name__ == "__main__":
	parser = optparse.OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input", action="store", type="string", dest="resumeInputFile",
		help="Name of resume in XML format that will be processed")
	parser.add_option("-o", "--output", action="store", type="string", dest="resumeOutputFile",
		help="Name of output file (STDOUT if not specified)")
	parser.add_option("-t", "--type", action="store", type="string", dest="resumeType",
		help="Resume type: HR-XML (xhrml), XmlResume (xmlres) or Europass (europass)")
	parser.add_option("-w", "--writer", action="store", type="string", dest="writer",
		help='Writer class that will output resume')
	parser.add_option("-l", "--list", action="store_true", dest="listWriters", default=False,
		help='Lists available writers for given resume type. After listing them, program will exit.')
	options, args = parser.parse_args()
	
	if   options.resumeType == 'hrxml':
		resTypeDisplayName = 'HrXml'
	elif options.resumeType == 'xmlres':
		resTypeDisplayName = 'XmlResume'
	elif options.resumeType == 'europass':
		resTypeDisplayName = 'Europass'
	else:
		print " "
		print "Supported resume types are: 'hrxml', 'xmlres' and 'europass'."
		print "Unknown resume type '%s', aborting ..." % options.resumeType
		sys.exit(1)
	writerBase = 'ResumeWriter.' + resTypeDisplayName
	parserModule = 'ResumeParser.' + resTypeDisplayName + 'Parser'

	# Exit after listing available module writers
	if options.listWriters:
		try:
			import pkgutil
		except ImportError:
			print "Unable to import module 'pkgutil', aborting ..."
			sys.exit(2)					
		print " "
		print "List of available writer modules for resume type '%s':" % resTypeDisplayName
		module = importlib.import_module( writerBase )
		pkgpath = os.path.dirname(module.__file__)
		print [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
		sys.exit(0)

	try:
		modWriter = importlib.import_module( writerBase + '.' + options.writer )
	except ImportError:
		print "Unable to import writer '%s' aborting ..." % (writerBase + '.' + options.writer)
		sys.exit(3)
	
	try:
		modParser = importlib.import_module( parserModule )
	except ImportError:
		print "Unable to import parser '%s' aborting ..." % parserModule
		sys.exit(3)

	# Check if input file exists before passing it to parser
	if not os.path.exists( options.resumeInputFile ):
		print "Resume input file '%s' does not exist, aborting ..." % options.resumeInputFile
		sys.exit(4)

	parser = modParser.ResumeParser( options.resumeInputFile )
	writer = modWriter.ResumeWriter( options.resumeOutputFile )
	parser.parse()
	model = parser.getModel()
	writer.write(model)
