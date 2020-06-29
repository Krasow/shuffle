from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Post
from .forms import CreateBlog, UpdateBlog
from django.contrib.auth.models import User
from operator import attrgetter
from django.core.mail import send_mail
import requests

# Create your views here.
def banter_view(response):
    if 'createMemeBanter' in response.POST:
        Meme = Post.objects.create(author = response.user)
        headersJoke = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }
        Meme.body = requests.get('https://icanhazdadjoke.com/', headers=headersJoke).json()['joke']
        Meme.imagelink = requests.get('https://some-random-api.ml/meme').json()['image']
        Meme.title = 'Random Banter'
        Meme.save()
    post  = sorted(Post.objects.filter(), key=attrgetter('date_up'), reverse=True)
    context = {'post':post}
    return render(response, "banter.html", context)

@login_required
def post_create(request):
    current_user = request.user
    form = CreateBlog(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = request.user
        obj.author = author
        obj.save()
        form = CreateBlog()
        return redirect("/banter")
    return render(request, "banter_create.html", {"form":form})


def post_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'detail_banter.html', {'post':post})

def share_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if 'sendemail' in request.POST:
        send_mail(
            'BANTER | CHECK OUT YOUR SAVED POST BY ' + post.author.username,
            'Click the link to view the post: http://127.0.0.1:8000/banter/' + post.slug,
            'krasowska89@gmail.com',
            [request.user.email],
            fail_silently=False
            )
        return redirect('../')
    elif 'sendother' in request.POST:
        email = request.POST['email']
        send_mail(
            'BANTER | CHECK OUT THIS POST BY ' + post.author.username,
            'Click the link to view the post: http://127.0.0.1:8000/banter/' + post.slug,
            'krasowska89@gmail.com',
            [email],
            fail_silently=False
            )
        return redirect('../')
    return render(request, 'shareEmail.html', {})


def update_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        if request.POST:
            form = UpdateBlog(request.POST or None, request.FILES or None, instance=post)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                post = obj
                return redirect("/banter")
        form = UpdateBlog(
            initial = {
                "title": post.title,
                "body": post.body,
                "image": post.image,
            }
        )
        return render(request, 'update_banter.html', {"form":form})


def delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.delete()
    return redirect("/banter")
