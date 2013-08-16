#!/usr/bin/env python

import os
import subprocess
from django.http import HttpResponse

XXDPATH = "/usr/bin/xxd"

class xxd:
	def __init__(self):
		print "[+] loaded plugin xxd."
		self.url_handler  = "XXD"
		self.stn_regexp   = [".*"] # all readable mappings

	def dispatch(self,request,filename):
		htmlcode = "<html><head><title>XXD Plugin - pid %s.</title></head>" % request.GET["pid"]
		htmlcode += "<body><pre>"
		htmlcode += subprocess.check_output([XXDPATH, filename])
		htmlcode += "</pre></body></html>"
		os.unlink(filename)
		return HttpResponse(htmlcode)
	# end dispatch
# end class

def load_plugin():
	x = xxd()
	return x
