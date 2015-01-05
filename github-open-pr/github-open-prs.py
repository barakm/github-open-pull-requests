__author__ = 'barakme'

#####################################################################
#
#   Python script to generate an XML file with entries for each open
# pull request on any repo in a given organization.
#
#   Expects two command line parameters - a github token,
# and an organization name
#
# Author: barakme
#
#######################################################################
from github3 import login
import xml.etree.ElementTree as ET
import xml.dom.minidom
import sys


def print_usage():
    print "Usage:\n" \
          "======" \
          "python github-open-prs.py <token> <organization>"

if len(sys.argv) != 3:
    print_usage()
    exit(1)

token = sys.argv[1]
org_name = sys.argv[2]
print "logging in to github"
gh = login(token=token)

print "Retrieving organization %s" % org_name
org = gh.organization(org_name)

print "Retrieving repos"
it_repos = org.iter_repos(type='all')
pullsNode = ET.Element("pull_requests")

pull_counter = 0

for repo in it_repos:
    print "Scanning repo: %s" % repo.name
    it_pulls = repo.iter_pulls(state='open')
    for pull in it_pulls:
        print "Found Pull request: %s" % pull.title
        pullNode = ET.SubElement(pullsNode, "pull")
        pullNode.set("repo", repo.name)
        pullNode.set("title", pull.title)
        pullNode.set("url", pull.html_url)
        pullNode.set("user",  pull.user.login)
        pullNode.set("created", pull.created_at.ctime())
        pull_counter += 1

pullsNode.set("total", "%i" % pull_counter)

tree = ET.ElementTree(pullsNode)

xml_string = ET.tostring(pullsNode)
parsed_xml = xml.dom.minidom.parseString(xml_string)
pretty_xml_string = parsed_xml.toprettyxml(indent="\t")

print pretty_xml_string

text_file = open("output.xml", "w")
text_file.write(pretty_xml_string)
text_file.close()






