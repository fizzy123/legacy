import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from persons.models import Person, Comment

def index(request):
    return render(request,'persons/index.html',{})

def results(request):
    if request.GET.has_key('q'):
        search_terms = request.GET['q']
    else:
        search_terms = ''
    return render(request,'persons/results.html',{'search_terms':search_terms})

def comments(request, user_id):
    person = Person.objects.get_or_create(user=user_id)[0]
    comments = Comment.objects.filter(owner=person)
    comment_list = []
    for comment in comments:
        comment_dict = {}
        comment_dict['pk'] = comment.pk
        comment_dict['created'] = comment.created
        comment_dict['text'] = comment.text
        comment_dict['upvotes'] = comment.upvotes
        comment_dict['downvotes'] = comment.downvotes
        comment_dict['up_active'] = comment in Person.objects.get_or_create(user = request.COOKIES.get('user_id'))[0].upvotes.all()
        comment_dict['down_active'] = comment in Person.objects.get_or_create(user = request.COOKIES.get('user_id'))[0].downvotes.all()
        comment_list.append(comment_dict)
    context = {'comments':comment_list,'user_id':user_id}
    return render(request, 'persons/person.html', context)

def add(request, user_id):
    person = Person.objects.get_or_create(user = user_id)[0]
    comment = Comment(owner=person, text = request.POST['text'])
    person.save()
    comment.save()
    return HttpResponseRedirect(reverse('persons:comments', args=(user_id,)))

def vote(request, comment_id):
    user = Person.objects.get_or_create(user = request.COOKIES.get('user_id'))[0]
    comment = Comment.objects.get(pk=int(comment_id))
    up_change = 0
    down_change = 0

    if request.POST['vote']=='up':
        if comment in user.upvotes.all():
            user.upvotes.remove(comment)
            comment.upvotes = comment.upvotes-1
            up_change = -1
        else:
            if comment in user.downvotes.all():
                user.downvotes.remove(comment)
                down_change = -1
                comment.downvotes = comment.downvotes-1
            user.upvotes.add(comment)
            comment.upvotes = comment.upvotes+1
            up_change = 1
    elif request.POST['vote']=='down':
        if comment in user.downvotes.all():
            user.downvotes.remove(comment)
            comment.downvotes = comment.downvotes-1
            down_change = -1
        else:
            if comment in user.upvotes.all():
                user.upvotes.remove(comment)
                comment.upvotes = comment.upvotes-1
                up_change = -1
            comment.downvotes = comment.downvotes+1    
            user.downvotes.add(comment)
            down_change = 1
    context= {'up_change':up_change, 'down_change':down_change}        
    user.save()
    comment.save()
    return HttpResponse(json.dumps(context), content_type="application/json")

