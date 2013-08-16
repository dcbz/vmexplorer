#!/usr/bin/env python

import sys
import vmmap
import HTML

b = []
v = vmmap.vmmap(sys.argv[1])
for i in v.get_maps():
	b.append(["%s" % i])
htmlcode = HTML.table(b)
print htmlcode

