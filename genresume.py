#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import importlib
import optparse
import os.path
import sys


HELPTEXT = "%s <options>" % os.path.normpath(sys.argv[0])
# Dictionary with resume types and their display names
RESTYPES = {
	'hrxml'    : 'HrXml',
	'xmlres'   : 'XmlResume',
	'europass' : 'Europass',
}

if __name__ == "__main__":
	parser = optparse.OptionParser(usage=HELPTEXT)
	parser.add_option("-i", "--input", action="store", type="string", dest="resumeInputFile",
		help="Name of resume in XML format that will be processed.")
	parser.add_option("-o", "--output", action="store", type="string", dest="resumeOutputFile",
		help="Base name of output file (STDOUT if not specified).")
	parser.add_option("-p", "--photo", action="store_true", dest="resumePhoto", default=False,
		help="Whether to include photo or not.")
	parser.add_option("-e", "--personal-data", action="store_true", dest="personalData", default=False,
		help="Whether to include personal data or not.")
	parser.add_option("-x", "--experience", action="store_true", dest="experience", default=False,
		help="Whether to include years of experience or not.")
	parser.add_option("-t", "--type", action="store", type="string", dest="resumeType",
		help="Resume type: HR-XML (xhrml), XmlResume (xmlres) or Europass (europass).")
	parser.add_option("-w", "--writer(s)", action="store", type="string", dest="writer",
		help='List of comma-separated writer classes that will output resume.')
	parser.add_option("-l", "--list", action="store_true", dest="listWriters", default=False,
		help='Lists available writers. After listing them, program will exit.')
	options, args = parser.parse_args()
	
	try:
		resTypeDisplayName = RESTYPES[ options.resumeType ]
	except KeyError:
		print " "
		print "Supported resume types are: %s." % RESTYPES.keys()
		print "Unknown resume type '%s', aborting ..." % options.resumeType
		sys.exit(1)
	writerBase = 'ResumeWriter'
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
		writers = options.writer.split(",")
		modWriters = []
		for writer in writers:
			modWriter = importlib.import_module( writerBase + '.' + writer )
			modWriters.append( modWriter )
	except ImportError:
		print "Unable to import writer '%s' aborting ..." % (writerBase + '.' + writer)
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
	parser.parse()
	model = parser.getModel() 
	
	for modWriter in modWriters:
		writer = modWriter.ResumeWriter( options.resumeOutputFile )
		writer.write(model=model, \
			withPhoto=options.resumePhoto, \
			personalData=options.personalData, \
			experience=options.experience
		)
	
