'''
Created on 2014. 12. 23.

@author: user
'''

import datetime
from haystack import indexes
from models import Entries

class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='Title')
    category = indexes.CharField(model_attr='Category')
    creation_date = indexes.DateTimeField(model_attr='created')
    content = indexes.CharField(model_attr='content')
    
    def get_model(self):
        return Entries

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created=datetime.datetime.now())
    