import os.path

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import *
from .models import *
from .forms import ArticleForm, CommentForm
from datetime import datetime
from spartamarket.util import *

import json


# from django.http import get


def index(request: HttpRequest):
    item_list = Item.objects.all()

    item_context_list = []
    for item in item_list:
        item_context = {
            'id': item.id,
            'title': item.title,
            'user': item.user.username,
            'url': '',
            'click_count': item.click_count,
        }
        if item.item_images.exists():
            item_context['url'] = item.item_images.all()[0].filepath.url

        item_context_list.append(item_context)

    context = {
        'item_list': item_context_list
    }
    return render(request, 'items/index.html', context)


def item_detail(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    item.click_count += 1
    item.save()

    item_context = {
        'item': item,
        'id': item.id,
        'title': item.title,
        'user': item.user.username,
        'content': item.content,
        'like': 0,
        'url': '',
    }
    if item.item_images.exists():
        item_context['url'] = item.item_images.all()[0].filepath.url

    context = {
        'item': item_context
    }
    return render(request, 'items/item_detail.html', context)


def register(request: HttpRequest):
    if request.method == 'POST' and request.FILES['file']:
        item = Item()
        item.content = request.POST.get('content')
        item.title = request.POST.get('title')
        item.price = request.POST.get('price')
        item.user = request.user

        print(item)

        # item.save()
        return redirect("items:index")
    else:
        print('get')
        return render(request, 'items/register.html')


@require_POST
def check_register(request: HttpRequest):
    data = json.loads(request.body)
    print(f'check register={data}')

    context = {
        "isValid": True,
        'title': data['title'],
        'price': data['price'],
        'content': data['content'],
    }
    return JsonResponse(context)


def upload_to_file(request: HttpRequest, dirname):
    file_path_list = []
    upload_dir_path = os.path.join('media', dirname)
    if not os.path.exists(upload_dir_path):
        os.mkdir(upload_dir_path)

    for uploaded_file in request.FILES.values():
        ext = uploaded_file.name.split(".")[-1]
        hashed_filename = sha512_hash(
            f"{request.user.username}image_file{datetime.now()}") + f".{ext}"

        file_path = upload_dir_path + hashed_filename
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_path_list.append(dirname + hashed_filename)

    return file_path_list


@require_POST
def do_register(request: HttpRequest):
    if request.method == 'POST':
        item = Item()
        item.content = request.POST.get('content')
        item.title = request.POST.get('title')
        item.price = request.POST.get('price')
        item.user = request.user

        item.save()

        file_path_list = upload_to_file(request, 'upload/')

        for file_path in file_path_list:
            image = Image()
            image.filepath = file_path
            image.item = item
            image.save()
            print(f'image path = {image.filepath}')

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded or invalid request'})


@require_POST
def delete(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    item.delete()

    print(f'delete. id = {id}')
    return redirect("items:index")


@require_POST
def update(request: HttpRequest, id):
    print(f'update. id = {id}')
    return redirect("items:index")


def hello(request):
    name = 'silee'
    tags = [
        '#활발한', '#밝은', '#귀여운'
    ]
    books = {
        'today': '토지',
        'yesterday': '태백산맥',
        'tommorow': '무정'
    }
    context = {
        'name': name,
        'tags': tags,
        'books': books
    }

    return render(request, 'items/hello.html', context)


def data_throw(request):
    return render(request, 'items/data-throw.html')


def data_catch(request):
    message = request.GET.get('message')
    print(message)
    context = {
        'message': message
    }

    return render(request, 'items/data-catch.html', context)


@login_required
def create(request: HttpRequest):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article: Article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('items:article_detail', article.id)
    else:
        form = ArticleForm()

    context = {'form': form}
    return render(request, 'items/create.html', context)


def article_detail(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comments.all()
    context = {
        "article": article,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "items/article_detail.html", context)


@require_POST
def delete_comment(request: HttpRequest, pk):
    article_id = request.POST.get('article_id')
    print(article_id)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect("items:article_detail", article_id)


@require_POST
def comment_create(request: HttpRequest, pk):
    print('test')
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.article = article
        comment.save()
    return redirect("items:article_detail", article.pk)


@require_POST
def like(request: HttpRequest, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
    else:
        return redirect("accounts:login")

    return redirect("items:items")
