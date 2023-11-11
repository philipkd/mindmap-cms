import os, marko, glob
from django.http import HttpResponse
from django.shortcuts import render

def index(request):

	files = glob.glob('_external/content/preview/*.txt')
	bodies = []
	for file in files:
		f = open(file,'r')
		bodies.append(f.read())
	body = marko.convert("\n".join(bodies))

	context = {
	    "author": "Gaurav Singhal",
	    "website": {
	        "domain": "https://pluralsight.com",
	        "views": 200
	    },
	    "odds": [1, 3, 5],
	    "body": body
	}
	return render(request, "index.html", context)

