'''
Created on 2014. 12. 23.

@author: user
'''

import datetime
from haystack import indexes
from models import Entries

class EntriesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    Title = indexes.CharField(model_attr='Title')
    Category = indexes.CharField(model_attr='Category')
    created = indexes.DateTimeField(model_attr='created')
    Content = indexes.CharField(model_attr='Content')
    Comments = indexes.CharField(model_attr='Comments')
    
    def get_model(self):
        return Entries

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    