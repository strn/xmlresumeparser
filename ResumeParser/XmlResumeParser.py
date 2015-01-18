#!/usr/bin/python
# -*- coding: utf-8 -*-

import ResumeModel
from lxml import etree

class XmlResumeParser():
	
  def __init__(self, input_file, target):
    self.target = target
    self.input = open(input_file, "r")
    self.root = etree.parse(input_file).getroot()
    self.breadcrumb = []
    self.model = ResumeModel.ResumeModel()
    self.skillset_idx = -1
    self.job_idx = -1
    self.degree_idx = -1
    self.award_idx = -1

  def close(self):
    self.input.close()

  def parse(self):
    self.parse_r(self.root)
    
  def parse_r(self, parent):
    if not self.process_target(parent, self.target):
      return
    # Make sure only Elements are processed
    if not isinstance(parent.tag, basestring):
      return
    self.breadcrumb.append(parent.tag)
    self.process_element(parent)
    for child in list(parent):
      self.parse_r(child)
    self.breadcrumb.pop()

  def process_target(self, parent, target):
    target_attr = parent.attrib.get("target")
    if target is None:
      if target_attr is None:
        return True
      else:
        return False
    else:
      if target_attr is None:
        return True
      else:
        if target.find('+') > -1 or target.find(',') > -1:
          op = "+" if target.find('+') > -1 else ","
          target_set = set(target.split(op))
          target_attr_set = set(target_attr.split(op))
          if target.find('+') > -1:
            return True if len(target_set.intersection(target_attr_set)) \
              == len(target_set) else False
          else:
            return True if len(target_set.intersection(target_attr_set)) > 0 \
              else False
        else:
          return True if target_attr == target else False

  def process_element(self, elem):
    #print "breadcrumb:",self.breadcrumb
    key = "/".join(self.breadcrumb)
    tag = elem.tag
    last_tag = self.breadcrumb[-1:][0]
    #print "tag:",tag
    print "key:",key
    #print "last tag:",last_tag
    if key.startswith("resume/header/name/"):
      self.model.name = self.append(self.model.name, elem.text)
    elif key.startswith("resume/header/address/"):
      if tag == "street":
        self.model.address = elem.text
      elif tag == "city" or tag == "state":
        self.model.address = self.append(self.model.address, elem.text, ", ")
      elif tag == "zip":
        self.model.address = self.append(self.model.address, elem.text, " ")
    elif key == "resume/header/address":
      # Untagged style address
      self.model.address = elem.text
    elif key.startswith("resume/header/contact/"):
      if tag == "phone":
        self.model.phone = "PHONE: " + elem.text
      elif tag == "email":
        self.model.email = "EMAIL: " + elem.text
      else:
        self.model.contacts.append(elem.tag.upper() + ": " + elem.text)
    elif key == "resume/objective":
      self.model.objective_title = self.get_title(elem)
    elif key.startswith("resume/objective/"):
      self.model.objectives.append(elem.text)
    elif key == "resume/skillarea/title":
      self.model.skillarea_title = self.get_title(elem)
    elif key == "resume/skillarea/skillset":
      self.skillset_idx = self.skillset_idx + 1
      self.model.skillset_titles.append(self.get_title(elem))
      self.model.skillsets.append([])
    elif key == "resume/skillarea/skillset/skill":
      if elem.attrib.get("level") != None:
        self.model.skillsets[self.skillset_idx].append(elem.text +
          " (" + elem.attrib.get("level") + ")")
      else:
        self.model.skillsets[self.skillset_idx].append(elem.text)
    elif key == "resume/history":
      self.model.jobs_title = self.get_title(elem)
    elif key == "resume/history/job":
      self.job_idx = self.job_idx + 1
      self.model.job_achievements.append([])
    elif key.startswith("resume/history/job/"):
      if tag == "jobtitle":
        self.model.job_titles.append(elem.text)
      elif tag == "employer":
        self.model.job_employers.append(elem.text)
      elif tag == "from":
        if len(list(elem)) == 1:
          date_from = self.format_date(list(elem)[0])
          self.model.job_employers[self.job_idx] = \
            self.model.job_employers[self.job_idx] + " (" + date_from
      elif tag == "to":
        if len(list(elem)) == 1:
          date_to = self.format_date(list(elem)[0])
          self.model.job_employers[self.job_idx] = \
            self.model.job_employers[self.job_idx] + " - " + date_to + ")"
      elif tag == "description":
        self.model.job_descriptions.append(elem.text)
      elif tag == "achievement":
        self.model.job_achievements[self.job_idx].append(elem.text)
    elif key == "resume/academics":
      self.model.academics_title = self.get_title(elem)
    elif key == "resume/academics/degrees/degree":
      self.degree_idx = self.degree_idx + 1
      self.model.academics.append([])
    elif key.startswith("resume/academics/degrees/degree/"):
      if tag == "level":
        self.model.academics[self.degree_idx] = elem.text
      elif tag == "major":
        self.model.academics[self.degree_idx] = \
          self.model.academics[self.degree_idx] + ", " + elem.text
      elif tag == "institution":
        self.model.academics[self.degree_idx] = \
          self.model.academics[self.degree_idx] + " from " + elem.text
      elif tag == "from":
        if len(list(elem) == 1):
          from_date = self.format_date(list(elem)[0])
          self.model.academics[self.degree_idx] = \
            self.model.academics[self.degree_idx] + " (" + elem.text
      elif tag == "to":
        if len(list(elem) == 1):
          to_date = self.format_date(list(elem)[0])
          self.model.academics[self.degree_idx] = \
            self.model.academics[self.degree_idx] + " - " + elem.text + ")"
    elif key == "resume/awards":
      self.model.awards_title = self.get_title(elem)
    elif key == "resume/awards/award":
      self.award_idx = self.award_idx + 1
      self.model.awards.append([])
    elif key.startswith("resume/awards/award/"):
      if tag == "title":
        self.model.awards[self.award_idx] = elem.text
      elif tag == "organization":
        self.model.awards[self.award_idx] = \
          self.model.awards[self.award_idx] + " from " + elem.text
      elif tag == "date":
        award_date = self.format_date(elem)
        self.model.awards[self.award_idx] = \
          self.model.awards[self.award_idx] + " (" + award_date + ")"

  def format_date(self, elem):
    if elem.tag != "date":
      return elem.tag
    dmy = ["", "", ""]
    for child in list(elem):
      if child.tag == "day":
        dmy[0] = child.text
      elif child.tag == "month":
        dmy[1] = child.text
      elif child.tag == "year":
        dmy[2] = child.text
      else:
        continue
    filtered_dmy = filter(lambda e : len(e) > 0, dmy)
    if len(filtered_dmy) > 0:
      return " ".join(filtered_dmy)

  def get_title(self, elem):
    title = elem.attrib.get("title")
    if title is None:
      return elem.tag.upper()
    else:
      return title

  def append(self, buf, str, sep=" "):
    if buf == None:
      buf = str
    else:
      buf = buf + sep + str
    return buf


if __name__ == "__main__":
	print "Testing XmlResumeParser ..."
	print
	parser = XmlResumeParser('example2.xml', None)
	parser.parse()
	parser.model.to_string()
