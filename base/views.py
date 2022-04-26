from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from .decorator import admin_only


def home(request):
    posts = Post.objects.filter(active=True, featured=True)

    context = {'posts': posts}
    return render(request, 'index.html', context)


@admin_only
@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('index')

    context = {'form': form}
    return render(request, 'post_form.html', context)


def post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return HttpResponse('This post doesnt exist')
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('post', slug=post.slug)

    context = {'post': post}
    return render(request, 'post.html', context)
