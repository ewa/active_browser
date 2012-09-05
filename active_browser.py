#!/usr/bin/env python

import psi.process
import os
import pwd
import sys

class CantGetArgsError (AttributeError):
    pass

def basename(proc):
    if len(proc.args) > 0:
        return os.path.basename(proc.args[0])
    newargs=proc.command.split()        # Imperfect!
    if len(newargs) > 0:
        return os.path.basename(newargs[0])
    raise CantGetArgsError(msg=proc) 


def has_name(proc, names):
    
    """ Try to match any of the names against either the process's
    accounting name or its argv[0]. """

    n = proc.name
    if n in names:
        return True
    n = basename(proc)
    if n in names:
        return True
    return False

def is_firefox(proc):
    return has_name(proc, ['firefox'])

def is_chromium(proc):
    return has_name(proc, ['chromium-browse', 'chromium-browser'])

def is_chrome(proc):
    return has_name(proc, ['chrome'])

def match_always(proc):
    return True

def run_generic(command,url):
    
    """We just assume command is in the user's path. """
    os.execvp(command, [command, url])

def mkrg(command):

    """mkrg = make run_generic: returns a closure with "command" bound in run_generic"""

    def do_it(url):
        return run_generic(command, url)
    do_it.func_name = 'do_it(%s,...)'%(command)
    return do_it

    
# Priority-ordered: earlier is preferred
BROWSER_TABLE = [('chromium', is_chromium, mkrg('chromium-browser')),
                 ('firefox',  is_firefox, mkrg('firefox')),
                 ('chrome',   is_chrome, mkrg('chrome')),
                 ('DEFAULT',  match_always, mkrg('sensible-browser'))
                 ]

def main(argv):

    if len(argv) != 2:
	sys.stderr.write("Usage: %s <url>\n" % sys.argv[0])
        return -1
    url = argv[1]
    verbose = False

    running_browsers = set()
    me_uid = os.getuid()
    me = pwd.getpwuid(me_uid).pw_name
    if verbose:
        print "You are", me, "uid", me_uid
    procs = psi.process.ProcessTable().values()
    my_procs = [p for p in procs if p.ruid == me_uid]
    #print "Your processes", [(p.name, p.pid, p.args) for p in my_procs]
    for p in my_procs:        
        for b in BROWSER_TABLE:
            b_name = b[0]
            b_func = b[1]
            if b_func(p)==True:
                #print "You have a browser: %d is %s, I think" % (p.pid, b_name)
                running_browsers.add(b_name)

    #"Sort" by position in BROWSER_TABLE
    prioritized = []
    for b in BROWSER_TABLE:
        b_name = b[0]
        b_run  = b[2]
        if b_name in running_browsers:
            prioritized.append((b_name, b_run))
    if verbose:
        print "Prioritized browser options:", prioritized
    if len(prioritized) == 0:
        sys.stderr.write("No browser available!  Consider adding a default with the match_all predicate.\n")
        sys.exit(1)
    best_browser = prioritized[0]
    (b_name, b_run) = best_browser
    print "Delegating to", b_name
    return b_run(url)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
