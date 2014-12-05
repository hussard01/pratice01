from django.contrib import admin
import blog.models

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
#from django.contrib.auth.backends import ModelBackend
 
# Register your models here.

admin.site.register(blog.models.Entries)
admin.site.register(blog.models.Categories)
admin.site.register(blog.models.Comments)
admin.site.register(blog.models.TagModel)
admin.site.register(blog.models.Blog)



#u = User.objects.get(username='admin')
#u.set_password('1234')
#u.save()

