from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import *
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
# from django.http import get


def index(request):
    return render(request, 'items/index.html')


def items(request):
    article_datas = Article.objects.all().order_by('-id')

    context = {
        'items': article_datas
    }
    return render(request, 'items/items.html', context)


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
def delete(request: HttpRequest, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect("items:items")


@require_POST
def delete_comment(request: HttpRequest, pk):
    article_id = request.POST.get('article_id')
    print(article_id)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect("items:article_detail", article_id)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request: HttpRequest, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('items:article_detail', article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'items/update.html', context)


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


# @require_POST
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
