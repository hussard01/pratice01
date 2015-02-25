from django.contrib import admin


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import blog


admin.site.register(blog.models.Entries)
admin.site.register(blog.models.Categories)
admin.site.register(blog.models.Comments)
admin.site.register(blog.models.TagModel)
admin.site.register(blog.models.Blog)

u = User.objects.get(username='user')
u.set_password('1234')
u.save()


"""
from django import forms
from redactor.widgets import RedactorEditor


class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = blog.models.Entries
        widgets = {
           'short_text': RedactorEditor(),
        }

class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm
"""