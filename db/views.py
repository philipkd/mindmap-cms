import os, marko, glob, re
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

DB_DIR = str(settings.BASE_DIR) + "/" + "_external/content/db3/"
NOTES_DIR = DB_DIR + 'files/'

class Note:
    @staticmethod
    def get_tags(file):
        tags = list(map(lambda x: x[0],re.findall(r'#(.*?)([\. ]|$)',file)))
        if (re.search(r'/- ',file)):
            tags.append('_stbd')
        return tags

    @staticmethod
    def get_title(file):
        file = re.sub(r'\.txt$','',file)
        file = re.sub(r'^\d{4}/','',file)
        file = re.sub(r' *#.*','',file)
        return file
    
    def __init__(self,file):

        self.file = file
        self.tags = self.get_tags(file)
        self.title = self.get_title(file)
        f = open(NOTES_DIR + file)
        self.text = f.read()

    def __repr__(self):
        return str(f'{self.title} ({len(self.text):d})')

class Database:

    @staticmethod
    def listify_tag_counts(df):
        return df.agg(lambda x: [Tag(x[0]), x[1]],1).tolist()

    def __init__(self):

        files = glob.glob(NOTES_DIR + '**/*.txt', recursive=True)

        df = pd.DataFrame(data=files,columns=['file'])
        df['file'] = df['file'].str.replace(NOTES_DIR,'')
        df['tags'] = df['file'].apply(Note.get_tags)

        self.df = df[df.apply(lambda x: False if '_pi' in x['tags'] else True,axis=1)]

    def __tag_counts(self):
        tag_counts = pd.Series([item for sublist in self.df['tags'] for item in sublist]).value_counts()
        tag_counts = tag_counts.to_frame(name='count').reset_index().rename(columns={'index':'tag'})
        return tag_counts

    def notes_by_tag(self,tag):
        notes = []
        df = self.df[self.df.apply(lambda x: True if tag in x['tags'] else False,axis=1)]
        df.apply(lambda x: notes.append(Note(x['file'])), axis=1)
        
        dash_notes = list(filter(lambda x: x.title.startswith('-'), notes))
        other_notes = list(filter(lambda x: not x.title.startswith('-'), notes))        
        return sorted(dash_notes,key=lambda x: x.title) + sorted(other_notes,key=lambda x: x.title)

    def basic_tag_counts(self):
        tag_counts = self.__tag_counts()
        tag_counts = tag_counts[~tag_counts.tag.str.contains('^_')]
        return self.listify_tag_counts(tag_counts)

    def special_tag_counts(self):
        tag_counts = self.__tag_counts()
        tag_counts = tag_counts[tag_counts.tag.str.contains('^_')]
        return self.listify_tag_counts(tag_counts)

class Tag:

    f = open(DB_DIR + 'tags.txt')
    tags = {}
    for line in f.readlines():
        split = line.strip().split(':')
        tags[split[0]] = split[1]        

    def __init__(self,tag):
        self.tag = tag

    def display(self):
        if self.tag in self.tags:
            return self.tags[self.tag]
        return self.tag.capitalize()

    def __str__(self):
        return self.tag

    def __repr__(self):
        return f'Tag({self.tag})'

def tag(request,tag):

    db = Database()

    notes = db.notes_by_tag(tag)
    for note in notes:
        note.md = marko.convert(note.text)

    context = {
        "tag": Tag(tag),
        "notes": notes,
    }
    return render(request, "tag.html", context)    


def index(request):

    db = Database()

    context = {
        "special_tag_counts": db.special_tag_counts(),
        "basic_tag_counts": db.basic_tag_counts(),
    }

    return render(request, "db.html", context)

