vmexplorer
==========

Django interface around vmmap, plugin system for providing additional inspection capability.

Plugins can be trivially added to the plugins/ directory where they will be auto-loaded.

Currently memxtract.c is written to extract from 64-bit processes. Need to add some code to support 32-bit processes as well


NOTE: memxtract needs privs to task_for_pid(), there are a bunch of ways to do this, code sign the bin and auth it |
chmod +s it and chown root it, or run the whole thing as root. Any way you want is fine, but introduces a security risk 
to the system...

