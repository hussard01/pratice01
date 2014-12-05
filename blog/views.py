#from django.shortcuts import render
 #-*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
#from django.utils import simplejson
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import login as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.template import RequestContext
#import md5

# Create your views here.
def list(request, page=1, blogid='common'):
    
    page_title = blogid + " list"    
        
    #if isinstance(page, int) == False:
    #    print 'aaaaaaaaaaaaa'
    #    page=1
     
    # blogid=1,
    page = int(page)
    
    per_page = 5
    start_pos = (page-1) * per_page
    end_pos = start_pos + per_page
        
    entries = Entries.objects.filter(BlogId=blogid, Delflag='N').select_related().extra(select={'rownum': 'row_number() OVER (ORDER BY "created")'}).order_by('-created')[start_pos:end_pos]
         
    total_count = Entries.objects.filter(BlogId=blogid, Delflag='N').count()
    total_page = (total_count/per_page)+1
        
    #보여줄 페이지 수 계산 / 10개씩
    if page%10 == 0:
        first_page = page-9
    else:
        first_page = ((page/10)*10)+1        

    if total_page > first_page+10:
        last_page = first_page+10        
    else:
        if total_count%5 == 0:
            last_page= total_page
        else : 
            last_page= total_page+1    
    
    
    total_page2 = range(first_page, last_page)
    
    #다음페이지, 이전페이지 계산
    previous_page = 0
    next_page = 0    
    if first_page-10 > 0 :
        previous_page = first_page-10
    if first_page+10 <= total_page :             
        next_page = first_page+10
        
    res = total_count%per_page    
    
    tpl = loader.get_template('blog/list.html')
    
    ctx = Context({
        'page_title':page_title,
        'entries':entries,
        'current_page':page,
        'previous_page':previous_page,
        'next_page': next_page,
        'total_page':total_page2,    
        'res':res,
        'count':total_count,
        'user' : request.user,
        'blogid':blogid,     
    })    
    
    return HttpResponse(tpl.render(ctx))

@login_required(login_url='/login_form')
def read(request, blogid='common', entry_id=None):
    page_title = 'view contents'
    
    current_entry = Entries.objects.get(id=int(entry_id))
    
    #로그인 안하면 안보이게 끔 추가
    # hit 수 추가    
    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
    except:
        next_entry = None
    
    #comment
    comments = Comments.objects.filter(Entry=entry_id, Delflag='N').order_by('created')
    
    tpl = loader.get_template('blog/read.html')
    
    ctx = Context({
        'page_title':page_title,
        'current_entry':current_entry,
        'entry_id' : current_entry,
        'prev_entry':prev_entry,
        'next_entry':next_entry,
        'comments':comments,
        'user' : request.user,
        'blogid':blogid,
    })
    
    ctx.update(csrf(request))
    
    return HttpResponse(tpl.render(ctx))

@login_required(login_url='/login_form')
def write(request, blogid='common'):
    page_title = 'write article!!!!!!!!!!!'
    
    tpl = loader.get_template('blog/write_form.html')
    categories = Categories.objects.all()

    ctx = Context({
            'page_title' : page_title,
            'categories' : categories,
            'blogid':blogid,
            'user' : request.user,
    })
    
    ctx.update(csrf(request))
   
    return HttpResponse(tpl.render(ctx))
    
@login_required(login_url='/login_form')
def add_post(request, blogid='common'):

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
        
    
    new_entry = Entries(BlogId = blogid, Title=entry_title, Content=entry_content, Category=entry_category)
    new_entry.save()
    
    for tag in tag_list:
        new_entry.Tags.add(tag)
    if len(tag_list) > 0:
        try:
            new_entry.save()
        except:
            return HttpResponse("error is occured")
    
    return HttpResponseRedirect("/blog/"+ blogid)
    #return HttpResponse("success to write number %s" % new_entry.id)

@login_required(login_url='/login_form')   
def del_post(request, blogid='common', entry_id=None):

    try:
        del_entry = Entries.objects.get(id=int(entry_id))
        #if request.POST['password'] == del_comment.Password:            
        del_entry = Entries.objects.filter(id=int(entry_id)).update(Delflag='Y')
        del_entry.save()
        return HttpResponseRedirect("/blog/"+ blogid)
    except:                
        return HttpResponseRedirect("/blog/"+ blogid)
     
@login_required(login_url='/login_form')
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
                'user' : request.user,                
            }
            
            
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
    except:
        return HttpResponse('fail to write1')
    return HttpResponse('fail to write2')

@csrf_exempt
@login_required(login_url='/login_form')
def get_comments(request, entry_id=None, is_inner=False):
    comments = Comments.objects.filter(Entry=entry_id, Delflag='N').order_by('created')
    tpl = loader.get_template('blog/comments.html')
    ctx = Context({
        'entry_id' : entry_id,
        'comments' : comments,
    })      
    ctx.update(csrf(request))
    
    if is_inner == True:
        return tpl.render(ctx)
    else:
        return HttpResponse(tpl.render(ctx))
   
@login_required(login_url='/login_form')
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
        return HttpResponse('fail to delete1')
    else:
        if request.POST.has_key('entry_id') == False:
            return HttpResponse('select the article')
        else:
            entry = Entries.objects.get(id=request.POST['entry_id'])
            
            if request.POST.has_key('password') == False:
                return HttpResponse('fail to delete2')
            else :                
                del_comment = Comments.objects.get(id=int(request.POST['id']))
                if request.POST['password'] == del_comment.Password:
                    del_comment.update(Delflag='Y')
                    entry.Comments -= 1
                    entry.save()
                else :
                    return HttpResponse('password is wrong')
                    
            #del_comment = Comments.objects.get(id=request.POST['id'])
            #del_comment.save()                
        return  HttpResponseRedirect('')
    return HttpResponse('fail to delete2')

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
        user = User.objects.create_user('none', email=email, password=password)
        user.save()
        return HttpResponseRedirect('/login_form')
            
    except:
        return HttpResponse("failed to join1")
    
    return HttpResponse("failed to join2")

def loginform(request):
    page_title = 'Loginform'
    
    tpl = loader.get_template('login_form.html')
    """
    next_loginform= ''
    
    if request.GET.has_key('next'):        
        if len(request.GET['next']) != 0:
            next_loginform = request.GET['next']
    """
    ctx = Context({
            'page_title' : page_title,
    #        'next' : next_loginform,
    })
    return HttpResponse(tpl.render(ctx))

@csrf_exempt    
def loginAction(request, next='index'):
   # if 'email' in request.POST:
   #     return HttpResponse("no email123")
   # else:

    """
    if 'next_page' in request.POST:
        next_page = request.POST['next_page']
        print next_page
    else:
        next_page = 'index'
    """
   
    if 'email' in request.POST:
        if len(request.POST['email']) == 0:
            return HttpResponse("enter the email")
        else:
            email = request.POST['email']
    else:
        print "asdfasdf"
              
#    if 'password' in request.POST:
#        return HttpResponse("no password")
#    else:
    if len(request.POST['password']) == 0:
        return HttpResponse("enter the password")
    else:
        password = request.POST['password']
    try:
        

        #user = User.objects.get(email=email)
        print "aaaaaaaaaaaaaaaaa"
        #user = authenticate(username = 'none', password = password)        
    #    user = authenticate(username= 'none' , email=email, password = password)
        user = authenticate(username= 'admin' , email=email, password = password)
    
        if user is not None:        
            if user.is_active:
                print ("here2")
                """                
                print str(request.GET['next'])
                
                if len(request.GET['next']) == 0:
                    print "test"
                    request.GET['next'] = 'index'
                """                    
                login(request, user)
                print ("here3")
                #print (next_page)
                #return HttpResponseRedirect('/index')
                return render_to_response('layout/index.html', {'user': user}, context_instance=RequestContext(request)) 
            else:
                print ("here4")
                return HttpResponse('wrong password')
        else:             
            print ("here5")
            return HttpResponseRedirect('/blog') 
            
    except:
        print ("here6")
        HttpResponse("don't have Email")
    
    print ("here7")
    return HttpResponseRedirect('/index')    

@login_required(login_url='/login_form')
def logout(request):
    print "aaaaaaaaaaa"
    auth_logout(request)
    #return HttpResponseRedirect('/blog')


