#from django.shortcuts import render
 #-*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
#from django.utils import simplejson
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/login_form')
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
    
    return HttpResponseRedirect("/blog")
    #return HttpResponse("success to write number %s" % new_entry.id)

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
        if request.is_ajax:
            new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry=entry)
            new_cmt.save()
            entry.Comments += 1
            entry.save()
            
       
            return_data = {
                'entry_id' : entry.id,
                'msg': get_comments(request, entry.id, True),                
            }
            
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
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
   

def del_comment(request):
    """
    if request.POST.has_key('entry_id') == False:
        return HttpResponse('select the article')
    else:
        try:
            entry = Entries.objects.get(id=request.POST['entry_id'])
        except:
            return HttpResponse('nothing')
    """ 
    if request.POST.has_key('id') == False:
        return HttpResponse('fail to delete')
    else:
        del_comment = Comments.objects.get(id=request.POST['id'])
        #if request.POST['password'] == del_comment.Password:            
        del_comment.delete()                
        return HttpResponse('success to delete')
    return HttpResponse('fail to delete')

def joinform(request):
    page_title = 'Joinform'
    
    ##add duplicated email check
  #  if request.is_ajax():
    

    
        
    
    tpl = loader.get_template('join_form.html')

    ctx = Context({
            'page_title' : page_title,
    })
  
    return HttpResponse(tpl.render(ctx))
    
@csrf_exempt
def join(request):
   
    if request.POST.has_key("email")==False:
        return HttpResponse("no email")
    else:
        if len(request.POST['email']) == 0:
            return HttpResponse("enter the email")
        else:
            email = request.POST['email']

            if request.is_ajax():
                email_flag = User.objects.filter(email=email)
                if email_flag:                    
                    return HttpResponse(False)
                else:
                    return HttpResponse(True)
                
        
    if request.POST.has_key("password")==False:
        return HttpResponse("no password")
    else:
        if len(request.POST['password']) == 0:
            return HttpResponse("enter the email")
        else:
            password = request.POST['password']
    
    try:
        user = User.objects.create_user('none1', email=email, password=password)
        user.save()
        return HttpResponseRedirect('/login_form')
            
    except:
        return HttpResponse("failed to join1")
    
    return HttpResponse("failed to join2")

def loginform(request):
    page_title = 'Loginform'
    
    tpl = loader.get_template('login_form.html')

    ctx = Context({
            'page_title' : page_title,
    })
  
    return HttpResponse(tpl.render(ctx))

@csrf_exempt    
def loginAction(request):
   # if 'email' in request.POST:
   #     return HttpResponse("no email123")
   # else:
    if len(request.POST['email']) == 0:
        return HttpResponse("enter the email")
    else:
        email = request.POST['email']
        print email
            
#    if 'password' in request.POST:
#        return HttpResponse("no password")
#    else:
    if len(request.POST['password']) == 0:
        return HttpResponse("enter the email")
    else:
        password = request.POST['password']
    
    try:
        
        #user = User.objects.get(email=email)
        
        user = authenticate(username = 'none', password = password)        
        
        if user.is_active:
            print ("here1")
            login(request, user)
            print ("here2")
            return HttpResponse('logged in successfully')
        else:
            return HttpResponse('wrong password')             
    except:
        HttpResponse("don't have Email")
    
    return HttpResponseRedirect('/login_form')    

def logout(request):
    logout(request)
    return HttpResponse('logged out successfully')


