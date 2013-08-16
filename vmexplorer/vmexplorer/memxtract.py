#!/usr/bin/env python

import os
import tempfile

globals()["MEMXTRACT"] = os.getcwd() + "/vmexplorer/bin/memxtract"

#usage: ./memxtract <pid> <output file> <start address> <end address>

class memxtract:
	def __init__(self,pid,startaddr,endaddr):
		self.__filename = tempfile.mktemp()
		os.system("%s %s %s %s %s" % (MEMXTRACT,pid,self.__filename,startaddr,endaddr))

	def file(self):
		return self.__filename

