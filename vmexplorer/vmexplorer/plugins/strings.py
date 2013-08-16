#!/usr/bin/env python

import os
import subprocess
from django.http import HttpResponse

STRINGSPATH = "/usr/bin/strings"

class strings:
	def __init__(self):
		print "[+] loaded plugin strings."
		self.url_handler  = "STRINGS"
		self.stn_regexp   = [".*"] # all readable mappings

	def dispatch(self,request,filename):
		htmlcode = "<html><head><title>STRINGS Plugin - pid %s.</title></head>" % request.GET["pid"]
		htmlcode += "<body><pre>"
		htmlcode += subprocess.check_output([STRINGSPATH, filename])
		htmlcode += "</pre></body></html>"
		os.unlink(filename)
		return HttpResponse(htmlcode)
	# end dispatch
# end class

def load_plugin():
	x = strings()
	return x
