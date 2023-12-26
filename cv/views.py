import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
	context = {}

	csv = str(settings.BASE_DIR) + "/" + "ext/content/CV/index-timeline.csv"

	df = pd.read_csv(csv)
	content = dict(df[df['cat'] != 'Hidden'].reset_index())
	i = 0
	to_render = []
	for row in content['desc']:
	    
	    to_render.append({'title': content['year'][i],'desc': content['desc'][i]})
	    i += 1
	to_render

	context['cv'] = to_render

	return render(request, "cv/index.html", context)
