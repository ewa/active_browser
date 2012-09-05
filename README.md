active_browser
=============

**What is it?**
It's a browser-launching script that looks to see if you
already have a browser open before it starts up something new.

**Why?**
Because browsers are big ugly bloated monstrosities, and running
one at time is plenty.  If this script is your default browser, then
you don't won't have to wait for your e-mail program to open Firefox
while Chrome is just sitting there (or vice versa).

**How do I set it up?**
There's one big global variable called BROWSER_TABLE.  It's a list of
tuples, each of which has 3 elements: A *name* (just used for user
interface), a *recognizer function* that decides whether or not any
given process "looks like" it's that browser, and a *launcher
function* that calls that browser.



