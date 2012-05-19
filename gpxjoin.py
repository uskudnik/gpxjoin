#!/usr/bin/env python
# encoding: utf-8
"""
gpxjoin.py

Created by  on 2012-05-19.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import argparse
from BeautifulSoup import BeautifulStoneSoup
import datetime

gpx_time_format = "%Y-%m-%dT%H:%M:%SZ"

def main():
	parser = argparse.ArgumentParser(description="Join multiple gpx files")
	parser.add_argument("gpx_files", metavar='GPX XML file', nargs="+", type=str, action='append')
	args = parser.parse_args(sys.argv[1:])
	xmls = list()
	for ffile in args.gpx_files[0]:
		ffile = open(ffile, "r")
		filecontent = ffile.readlines()[0]
		xml = BeautifulStoneSoup(filecontent)
		starttime = datetime.datetime.strptime(xml.find("metadata").find("time").string, gpx_time_format)
		xmls += [[starttime, filecontent]]
	
	ffiles = sorted(xmls, key=lambda *d: d[0]) 
	
	joined_gpx = ffiles[0][1].split("</gpx>")[0]
	
	for date, ffile in ffiles[1:]:
		header, content = ffile.split("</metadata>")
		joined_gpx += content.split("</gpx>")[0]
	joined_gpx += "</gpx>"
	
	output_filename = " + ".join([f.split(".gpx.xml")[0] for f in args.gpx_files[0]]) + ".gpx.xml"
	output_gpx = file(output_filename, "w")
	output_gpx.write(joined_gpx)
	output_gpx.close()
	
if __name__ == '__main__':
	main()

