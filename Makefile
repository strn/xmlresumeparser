SHELL = /bin/sh
XMLLINT = /usr/bin/xmllint
HRXMLDIR = /home/edu/hr-xml/HR-XML-2_5
CVBASENAME = Zoltan_Csala
RESUMEDIR = /home/zoli/doc/txt/xml

all: dummy

checkcv:
	$(XMLLINT) --noout --schema $(HRXMLDIR)/SEP/Resume.xsd $(RESUMEDIR)/$(CVBASENAME)_HR_XML_en.xml

gencv:
	./genresume.py -i $(RESUMEDIR)/$(CVBASENAME)_HR_XML_en.xml -t hrxml -w AsciiDoc -o $(CVBASENAME).adoc
	asciidoctor -b html5 $(CVBASENAME).adoc

clean:
	rm -f *.log *.pyc *.html *.pdf *.adoc
	
