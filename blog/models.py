from django.db import models

class Blog(models.Model):    
    BlogId = models.CharField(max_length=30, null=False)
    Name = models.CharField(max_length=30, null=True)    

class Categories(models.Model):
    Title = models.CharField(max_length=40, null=False)    
    
class TagModel(models.Model):
    Title = models.CharField(max_length=20, null=False)

class Entries(models.Model):
    BlogId = models.CharField(max_length=20, null=False)
    Title = models.CharField(max_length=80, null=False)    
    Content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    Category = models.ForeignKey(Categories)
    Tags = models.ManyToManyField(TagModel)
    Delflag = models.CharField(max_length=1, default='N', null=False)
    Name = models.CharField(max_length=20, null=False)
    Hit = models.PositiveSmallIntegerField(default=0, null=True)
    Recommand = models.PositiveSmallIntegerField(default=0, null=True)    
    deleted = models.DateTimeField(auto_now=True)
    Comments = models.PositiveSmallIntegerField(default=0, null=True)

class Comments(models.Model):
    Name = models.CharField(max_length=20, null=False)
    Password = models.CharField(max_length=32, null=False)
    Content = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=True)
    Delflag = models.CharField(max_length=1, default='N', null=False)
    Recommand = models.PositiveSmallIntegerField(default=0, null=True)
    deleted = models.DateTimeField(auto_now=True)
    Entry = models.ForeignKey(Entries)