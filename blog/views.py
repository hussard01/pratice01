#from django.shortcuts import render
 #-*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

#import md5

# Create your views here.
def index(request, page=1):
    page_title = "blog article list"    
    
    if isinstance(page, int) == False:
        page=1
        
    page = int(page)
    
    per_page = 5
    start_pos = (page-1) * per_page
    end_pos = start_pos + per_page
    
    entries = Entries.objects.all().select_related().order_by('-created')[start_pos:end_pos]    
    
    
    total_count = Entries.objects.count()
    total_page = (total_count/per_page)+1
    res = total_count%per_page         
    
    tpl = loader.get_template('list.html')
    ctx = Context({
        'page_title':page_title,
        'entries':entries,
        'current_page':page,
        'total_page':range(1, total_page+1),    
        'res':res,        
    })
    
    return HttpResponse(tpl.render(ctx))


def read(request, entry_id=None):
    page_title = 'view contents'
    
    current_entry = Entries.objects.get(id=int(entry_id))
    
    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
    except:
        next_entry = None
    
    #comment
    comments = Comments.objects.filter(Entry=entry_id).order_by('created')
    
    tpl = loader.get_template('read.html')
    
    ctx = Context({
        'page_title':page_title,
        'current_entry':current_entry,
        'prev_entry':prev_entry,
        'next_entry':next_entry,
        'comments':comments,
    })
    
    ctx.update(csrf(request))
    
    return HttpResponse(tpl.render(ctx))

def write(request):
    page_title = 'write article!!!!!!!!!!!'
    
    tpl = loader.get_template('write_form.html')
    categories = Categories.objects.all()

    ctx = Context({
            'page_title' : page_title,
            'categories' : categories, 
    })
    
    ctx.update(csrf(request))
   
    return HttpResponse(tpl.render(ctx))
    

def add_post(request):

    if request.POST.has_key("title")==False:
        return HttpResponse("write title!!!")
    else:
        if len(request.POST['title']) == 0:
            return HttpResponse('글 title엔 적어도 한 글자는 넣자!')
        else:
            entry_title = request.POST["title"]
    
    if request.POST.has_key('content') == False:
        return HttpResponse('글 본문을 입력해야 한다우.')
    else:
        if len(request.POST['content']) == 0:
            return HttpResponse('글 본문엔 적어도 한 글자는 넣자!')
        else:
            entry_content = request.POST["content"]
    
    try :
        entry_category = Categories.objects.get(id=request.POST['category'])
    except:
        return HttpResponse('sadfasdf')
    
    
    tags = []
    tag_list = []
    split_tags = unicode(request.POST['tags']).split(',')
    for tag in split_tags:
        tags.append(tag.strip())
    for tag in tags:
        tag_list.append(TagModel.objects.get_or_create(Title=tag)[0])
        
    
    new_entry = Entries(Title=entry_title, Content=entry_content, Category=entry_category)
    new_entry.save()
    
    for tag in tag_list:
        new_entry.Tags.add(tag)
    if len(tag_list) > 0:
        try:
            new_entry.save()
        except:
            return HttpResponse("error is occured")
    
    
    return HttpResponse("success to write number %s" % new_entry.id)

def add_comment(request):
    cmt_name = request.POST.get('name', '')
    if not cmt_name.strip():
        return HttpResponse("fill out name")
    
    cmt_password = request.POST.get('password', '')
    if not cmt_password.strip():
        return HttpResponse('fill out password')
    #cmt_password = md5.md5(cmt_password).hexdigest()
    
    cmt_content = request.POST.get('content','')
    if not cmt_content.strip():
        return HttpResponse('fill out commnet')
    
    if request.POST.has_key('entry_id') == False:
        return HttpResponse('select the article')
    else:
        try:
            entry = Entries.objects.get(id=request.POST['entry_id'])
        except:
            return HttpResponse('nothing')
    
    try:
        if request.is_ajax():        
            new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry=entry)
            new_cmt.save()
            entry.Comments += 1
            entry.save()
            
       
            return_data = {
                'entry_id' : entry.id,
                'msg': get_comments(request, entry.id, True),
            }
            return HttpResponse(simplejson.dumps(return_data))
        else:
            return HttpResponseRedirect('/blog/')
    except:
        return HttpResponse('fail to write1')
    return HttpResponse('fail to write2')

@csrf_exempt
def get_comments(request, entry_id=None, is_inner=False):
    comments = Comments.objects.filter(Entry=entry_id).order_by('created')
    tpl = loader.get_template('comments.html')
    ctx = Context({
        'comments' : comments
    })      
    ctx.update(csrf(request))
    
    if is_inner == True:
        return tpl.render(ctx)
    else:
        return HttpResponse(tpl.render(ctx))
    
def login(request):
    request.session['blog_login_session'] = 'guest'
    return HttpResponse('[%s] logged in successfully' % request.session['blog_login_session'])

def logout(request):
    del request.session['blog_login_session']
    return HttpResponse('logged out successfully')

   
"""
def del_comment(request):
    if request.POST.has_key('id') == False:
        return HttpResponse('fail to delete')
    else:
        del_comment = Comments.objects.get(id=request.POST['id'])
        if request.POST['password'] == del_comment.Password:
            del_comment.delete()
            return HttpResponse('success to delete')
    return HttpResponse('fail to delete')
    
"""