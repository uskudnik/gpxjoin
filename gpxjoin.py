#!/usr/bin/env python
# encoding: utf-8
"""
gpxjoin.py

Licensed under MIT License.

Copyright (c) 2012, Urban Skudnik <urban.skudnik@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import sys
import argparse
from BeautifulSoup import BeautifulStoneSoup
import datetime

gpx_time_format = "%Y-%m-%dT%H:%M:%SZ"

def main():
	parser = argparse.ArgumentParser(description="Join multiple gpx files")
	parser.add_argument("gpx_files", metavar='GPX XML file', nargs="+", type=str, action='append')
	args = parser.parse_args(sys.argv[1:])
	files = list()
	
	# To make sure our data files are attached in correct order; we don't trust file system (download order, ...)
	for ffile in args.gpx_files[0]:
		ffile = open(ffile, "r")
		filecontent = ffile.readlines()[0]
		xml = BeautifulStoneSoup(filecontent)
		starttime = datetime.datetime.strptime(xml.find("metadata").find("time").string, gpx_time_format)
		files += [[starttime, filecontent]]
	
	ffiles = sorted(files, key=lambda *d: d[0]) 
	
	# GPX end tag is unnecessary from initial file
	joined_gpx = ffiles[0][1].split("</gpx>")[0]
	
	# "Header" data (initial xml tag, gpx tag, metadata, etc.) is unnecessary
	# in subsequent file, therefore we remove it, along with end GPX tag.
	for date, ffile in ffiles[1:]:
		header, content = ffile.split("</metadata>")
		joined_gpx += content.split("</gpx>")[0]
	
	# Processed all files, append end GPX tag
	joined_gpx += "</gpx>"
	
	# Filename is a combination of all files names
	output_filename = " + ".join([f.split(".gpx.xml")[0] for f in args.gpx_files[0]]) + ".gpx.xml"
	output_gpx = file(output_filename, "w")
	output_gpx.write(joined_gpx)
	output_gpx.close()
	
if __name__ == '__main__':
	main()

