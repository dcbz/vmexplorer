from django.conf.urls import patterns, include, url
from django.http import HttpResponse
import vmmap
import memxtract
import sys
import os
import re

globals()["LOADED_PLUGINS"] = []

def plugins_list(plugins_dirs):
    """ List all python modules in specified plugins folders """
    for path in plugins_dirs.split(os.pathsep):
        for filename in os.listdir(path):
            name, ext = os.path.splitext(filename)
            if ext.endswith(".py"):
                yield name


def import_plugins(plugins_dirs, env):
    """ Import modules into specified environment (symbol table) """
    for p in plugins_list(plugins_dirs):
        m = __import__(p, env)
        # env[p] = m
        globals()["LOADED_PLUGINS"].append(m.load_plugin())


plugins_dirs = os.getcwd() + "/vmexplorer/plugins"
sys.path.extend(plugins_dirs.split(os.pathsep))

import_plugins(plugins_dirs, globals())

def dispatch(request):
	if(request.path.split("/")[-1] == "pid"):
		return build_table(request) # show mappings for pid
		

	for p in globals()["LOADED_PLUGINS"]:
		if(request.GET.has_key("CMD") and request.GET["CMD"] == p.url_handler):
			print "[+] Dispatching to plugin: %s" % p.url_handler
			m = memxtract.memxtract(request.GET["pid"],request.GET["startaddr"],request.GET["endaddr"])
			filename = m.file()
			return p.dispatch(request,filename)
        return index_form(request) # return index form, enter pid etc.

def perm2color(pn):
	color = "white"
	if(pn == 1):
		color = 'blue'
	if(pn == 2):
		color = 'yellow'
	if(pn == 4):
		color = 'red'
	if(pn == 6):
		color = 'green'
	if(pn == 5):
		color = 'purple'
	if(pn == 3):
		color = 'orange'
	if(pn == 7):
		color = 'brown'
	return color

def table_space():
	return \
"""
 <TR>
  <TD bgcolor=gray><br></TD>
 </TR>
 <TR>
"""


def table_entry(v,pid):
# Print an entry in the table colored appropriately based on protections.
# r-- : blue
# -w- : yellow
# --x : red
# rw- : green
# r-x : purple
# -wx : orange
# rwx : brown
#
	pn = 0
	perm = v["prot"].split("/")[0]
	if(perm[0] == 'r'):
		pn += 4
	if(perm[1] == 'w'):
		pn += 2
	if(perm[2] == 'x'):
		pn += 1
	color = perm2color(pn)
	txt = "%s" % v # string version of dictionary for now
	strv =  "<font face=arial>"
	strv += "<b>NAME:</b> %s <br>"
	strv += "<b>ADDRESS RANGE:</b> %s <br>"
	strv += "<b>MEMORY PERMISSIONS:</b> %s <br>"
	strv += "<b>FILE NAME:</b> %s <br>"
	strv += "</font>"
	strv = strv % (v["name"],v["vmaddr"],v["prot"],v["filename"]) 
	plgtxt = ""
	if(pn & 4): # readable	
		# add urls for plugins.
		for p in globals()["LOADED_PLUGINS"]:
			for r in p.stn_regexp:
				m = re.search(r,v["name"])
				if(m):
					plgtxt += "<a href=./?CMD=%s&pid=%s&startaddr=%s&endaddr=%s>%s</a>" % (p.url_handler,pid,v["vmaddr"].split("-")[0],v["vmaddr"].split("-")[1],p.url_handler)
				plgtxt += "&nbsp;"
	txt = \
"""
 <TR>
  <TD bgcolor=%s>%s%s</TD>
 </TR>
 <TR>
""" % (color,strv,plgtxt)
	return txt


def index_form(request):
	htmlcode = "<html><head><title> vmexplorer - select pid </title></head>"
	htmlcode =  "<font face=arial>"
	htmlcode += "<body>Enter PID: <form action=pid><input type=text name=pid><input type=submit name=btn_smt value=\"get mappings\"></form>"
	htmlcode += "</body></font></html>"
	return HttpResponse(htmlcode)

def build_table(request):
	b = []
	pid = request.GET["pid"]
	htmlcode = "<html><head><title> vmexplorer - memory map of %s </title></head><body>" % pid
	htmlcode += "<TABLE width=100% cellpadding=\"4\" style=\"border: 1px solid #000000; border-collapse: collapse;\" border=\"1\">"
	v = vmmap.vmmap(pid)
	old_n = 0 # save end of mapping
	for i in v.get_maps():
		if(int(i["vmaddr"].split("-")[0],16) != old_n):
			htmlcode += table_space()
		old_n = int(i["vmaddr"].split("-")[1],16)
		htmlcode += table_entry(i,pid)
	htmlcode += "</table></body></html>"
	return HttpResponse(htmlcode)

