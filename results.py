#!/usr/bin/python3
import cgi
import cgitb
import sys

sys.path.append('/scripts/')

from compare_trajectories import get_similarity

form = cgi.FieldStorage()
code = form.getvalue("submission")

subjective = bool(int(form.getvalue("subjective")))
pb = form.getvalue("pb")

print("Content-Type: text/plain\n\n")

if not code:
    print("Please fill in the form")
elif not pb:
    print("Please define the problem to check")
else:
    print(get_similarity(code, pb, subjective=subjective))









