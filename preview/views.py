import os, marko
from django.http import HttpResponse



def index(request):

	f = open('content/preview/new-publishing-attempt.txt','r')
	text = f.read()
	print(marko.convert(text))

	return HttpResponse(marko.convert(text))