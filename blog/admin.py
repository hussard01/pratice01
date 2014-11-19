from django.contrib import admin
import blog.models
# Register your models here.

admin.site.register(blog.models.Entries)
admin.site.register(blog.models.Categories)
admin.site.register(blog.models.Comments)
admin.site.register(blog.models.TagModel)