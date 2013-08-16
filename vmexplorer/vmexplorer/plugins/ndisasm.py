#!/usr/bin/env python

import os
import subprocess
from django.http import HttpResponse

NDISASMPATH = "/usr/local/bin/ndisasm"

class ndisasm:
	def __init__(self):
		print "[+] loaded plugin ndisasm."
		self.url_handler  = "NDISASM"
		self.stn_regexp   = [".*_TEXT.*"] # all readable mappings

	def dispatch(self,request,filename):
		htmlcode = "<html><head><title>NDISASM Plugin - pid %s.</title></head>" % request.GET["pid"]
		htmlcode += "<body><pre>"
		htmlcode += subprocess.check_output([NDISASMPATH,"-b64",filename])
		htmlcode += "</pre></body></html>"
		os.unlink(filename)
		return HttpResponse(htmlcode)
	# end dispatch
# end class

def load_plugin():
	n = ndisasm()
	return n
