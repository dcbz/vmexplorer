#!/usr/bin/env python
# vmmap.py
# 
# Class for running vmmap on a pid and parsing output into a table.
#

import re
import subprocess

globals()["VMMAP_PATH"] = "/usr/bin/vmmap"

class vmmap:
	def __init__(self,pid):
		self.__pid = pid  # store pid for plugins to use to parse address space.
		self.update_maps()
	# end __init__
		
	def get_maps(self):
		return self.__vmmap
	

	def update_maps(self):
		self.__vmmap = [] # array of dictionary for storing results
		proc = subprocess.Popen([VMMAP_PATH,"-v","-interleaved",self.__pid],stdout=subprocess.PIPE)
		for line in proc.stdout:
			line = line.rstrip()
			m = re.search("([\\x20A-Za-z0-9_]+)\W+([0-9a-f]+-[0-9a-f]+)\W+\[.*\]\W([rwx\\x2d\\x2f]+)",line)
			if(m):
				if(m.group(1)[0:6] == "Submap"): # filter submap summaries for now
					continue

				n = re.search("[A-Z]=[A-Z]+[\\x20\\x09]+([^=]*)$",line)
				if(n):
					filename = n.group(1)
					filename = re.sub("[^\x20\x21-\x7e]","",filename)
				else:
					filename = None # anonymous mapping.


				self.__vmmap.append({
							"filename" : filename,
							"name"     : m.group(1).rstrip(), 
							"vmaddr"   : m.group(2).rstrip(), 
							"prot"     : m.group(3).rstrip()
				})
	# end update_maps

	def print_vm(self):
		for m in self.__vmmap:
			print m
	#end print_vm
if __name__ == "__main__":
	import sys
	if(len(sys.argv) != 2):
		print "usage: %s <pid>" % sys.argv[0]
		sys.exit(1)

	print "[+] Running vmmap on pid: %s" % sys.argv[1]
	v = vmmap(sys.argv[1])
	v.print_vm()
		
