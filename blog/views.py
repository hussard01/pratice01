#from django.shortcuts import render
 #-*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from blog.models import Entries, Categories, TagModel, Comments
from django.template import Context, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog import forms

from haystack.query import SearchQuerySet



#from django.contrib.auth.decorators import permission_required
#from django.shortcuts import render, render_to_response
#from django.template.context import RequestContext

#import md5

def paging(page, total_count, per_page):
    
    
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
        
    return {'previous_page' : previous_page, 'next_page' : next_page, 'total_page2' : total_page2, 'res' :res} 

# Create your views here.
def list(request, page=1, blogid='common', entries=None):
    
    page_title = blogid + " list"    
        
    page = int(page)
    
    per_page = 5
    start_pos = (page-1) * per_page
    end_pos = start_pos + per_page
    
    if entries == None:
        entries = Entries.objects.filter(BlogId=blogid, Delflag='N').select_related().extra(select={'rownum': 'row_number() OVER (ORDER BY "created")'}).order_by('-created')[start_pos:end_pos]
        total_count = Entries.objects.filter(BlogId=blogid, Delflag='N').count()
    else :
        entries.order_by('-created')[start_pos:end_pos]
        total_count = entries.count()
    cpage = paging(page, total_count, per_page)        
    
    tpl = loader.get_template('blog/list.html')
    
    ctx = Context({
        'page_title':page_title,
        'entries':entries,
        'current_page':page,
        'previous_page':cpage['previous_page'],
        'next_page': cpage['next_page'],
        'total_page':cpage['total_page2'],    
        'res':cpage['res'],
        'count':total_count,
        'user' : request.user,
        'blogid':blogid,     
    })    
    
    return HttpResponse(tpl.render(ctx))

@login_required(login_url='/login/form')
def read(request, blogid='common', entry_id=None):
    page_title = 'view contents'
    
    current_entry = Entries.objects.get(id=int(entry_id), Delflag='N')
    
    #조회수 추가
    current_entry.Hit += 1    
    current_entry.save()
    
    #로그인 안하면 안보이게 끔 추가
    # hit 수 추가    
    try:
        prev_entry = current_entry.get_previous_by_created()
        if prev_entry.Delflag == 'Y':
            prev_entry = None
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created()
        if next_entry.Delflag == 'Y':
            next_entry =None
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
       
   
    

@login_required(login_url='/login/form')
def write(request, blogid='common'):
    
    writeform = forms.writeForm(request.POST)
    page_title = 'write article!!!!!!!!!!!'

    tpl = loader.get_template('blog/write_form.html')
    categories = Categories.objects.all()

    ctx = Context({
            'content' : writeform['content'],
            'page_title' : page_title,
            'categories' : categories,
            'blogid':blogid,
            'user' : request.user,
    })
    
    ctx.update(csrf(request))
   
    return HttpResponse(tpl.render(ctx))


@login_required(login_url='/login/form')
def updateform(request, blogid='common', entry_id=None):
        
    page_title = 'update article!'
        
    entry = Entries.objects.get(id=int(entry_id), Delflag='N')
    
    if request.user.username == entry.Name:        

        updateform1 = forms.writeForm(request.POST)
        updateform1.data['content'] = entry.Content
        
 
        categories = Categories.objects.all()
        tpl = loader.get_template('blog/update_form.html')
        
        ctx = Context({
                'page_title' : page_title,
                'entry' : entry,
                'blogid':blogid,
                'categories' : categories,
                'user' : request.user,
                'content' : updateform1['content'],
        })
        
        ctx.update(csrf(request))
   
        return HttpResponse(tpl.render(ctx))
    
    else:
        print "3"
        return HttpResponseRedirect('/blog/'+blogid+'/entry/'+entry_id)

    
@login_required(login_url='/login/form')
def add_post(request, blogid='common'):

    #if request.method == 'Post'
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
    
    if request.user == False:
        return HttpResponse('ㅁㄴㅇㄹ')
    
    
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
        
    new_entry = Entries(BlogId = blogid, Name=request.user.username, Title=entry_title, Content=entry_content, Category=entry_category)
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


@csrf_exempt
@login_required(login_url='/login/form')
def update_post(request, blogid='common', entry_id=None):

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
    
    if request.user == False:
        return HttpResponse('ㅁㄴㅇㄹ')
        
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
     
    Entries.objects.filter(id=entry_id).update(Title=entry_title, Content=entry_content, Category=entry_category)  
    new_entry = Entries.objects.get(id=entry_id)  
    
    for tag in tag_list:        
        new_entry.Tags.add(tag)
    if len(tag_list) > 0:
        try:
            new_entry.save()
        except:
            return HttpResponse("error is occured")
    
    return HttpResponseRedirect("/blog/"+ blogid)
    #return HttpResponse("success to write number %s" % new_entry.id)
        


@login_required(login_url='/login/form')   
def del_post(request, blogid='common', entry_id=None):

    try:
        del_entry = Entries.objects.get(id=int(entry_id))
        #if request.POST['password'] == del_comment.Password:            
        del_entry = Entries.objects.filter(id=int(entry_id)).update(Delflag='Y')
        del_entry.save()
        return HttpResponseRedirect("/blog/"+ blogid)
    except:                
        return HttpResponseRedirect("/blog/"+ blogid)
     
@login_required(login_url='/login/form')
def add_comment(request):

    if request.user == False:
        return HttpResponse('ㅁㄴㅇㄹ')
    
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
            new_cmt = Comments(Name=request.user, Password=cmt_password, Content=cmt_content, Entry=entry)
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
@login_required(login_url='/login/form')
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
   
@login_required(login_url='/login/form')
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
    print "2222222222222222222222222222222"
    
    tpl = loader.get_template('join_form.html')

    ctx = Context({
            'page_title' : page_title,
    })
  
    return HttpResponse(tpl.render(ctx))
    
@csrf_exempt
def join(request):

    page_title = 'Joinform'
    print "asdfffffffffffffff1111"


    if request.method == 'POST':

        form = forms.joinForm(request.POST)

        if request.is_ajax() and request.POST.has_key('name'):
            print "bbbbbbbb"
            name_flag = User.objects.filter(username=request.POST['name'])
            if name_flag:
                return HttpResponse(False)
            else:
                return HttpResponse(True)


        if request.is_ajax() and request.POST.has_key('email'):
            email_flag = User.objects.filter(email=request.POST['email'])
            if email_flag:
                return HttpResponse(False)
            else:
                return HttpResponse(True)

        if form.is_valid():
            data = form.cleaned_data

            try:
                user = User.objects.create_user(data['name'], email=data['email'], password=data['password'])
                user.save()
                return HttpResponseRedirect('/login/form')

            except:
                form.add_error(None, "중복된 아이디")
                return render_to_response('join_form.html', {'form': form,'page_title' : page_title})
            return render_to_response('join_form.html', {'form': form,'page_title' : page_title})
    else:
        form = forms.joinForm()

    return render_to_response('join_form.html', {'form': form,'page_title' : page_title})


def loginform(request):
    page_title = 'Loginform'
    
    tpl = loader.get_template('login_form.html')

    ctx = Context({
            'page_title' : page_title,
    })
    return HttpResponse(tpl.render(ctx))

@csrf_exempt
def loginAction(request, next='index'):

    page_title = 'Loginform'

    if request.method == 'POST':
        form = forms.loginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            try:
                user = authenticate(username=data['name'], password = data['password'])

                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        #print (next_page)
                        return HttpResponseRedirect('/index')
                        #return render_to_response('layout/index.html', {'user': user}, context_instance=RequestContext(request))
                    else:
                        print ("here4")
                        return HttpResponseRedirect('/login/form')
                else:
                    form.add_error(None, "로그인 실패")
                    return render_to_response('login_form.html', {'form': form,'page_title' : page_title})

            except:
                form.add_error(None, "잘못된 접근입니다.")
                return render_to_response('login_form.html', {'form': form,'page_title' : page_title})

    print ("here7")
    return HttpResponseRedirect('/index')    

@login_required(login_url='/login/form')
def logout(request):
    print "aaaaaaaaaaa"
    auth_logout(request)
    return HttpResponseRedirect('/index')


@csrf_exempt    
@login_required(login_url='/login/form')
def profile(request, next='index'):
    pass


@csrf_exempt
def searchAction(request):

    entries = SearchQuerySet().filter(Title__contains=request.POST.get('q'))

    return list(request, 1, request.POST['blogid'], entries)


