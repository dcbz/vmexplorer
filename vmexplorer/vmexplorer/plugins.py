#!/usr/bin/env python

import os
import glob

class plugins:
	def __init__(self):
		__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/bin/*.py")]
