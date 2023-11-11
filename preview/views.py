import os, marko
from django.http import HttpResponse
from django.shortcuts import render

def index(request):

	f = open('_external/content/preview/new-publishing-attempt.txt','r')
	body = marko.convert(f.read())

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

