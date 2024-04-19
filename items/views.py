from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import *
from django.db.models import Count
from .models import *
from spartamarket.util import *

import json


def index(request: HttpRequest):
    category = request.GET.get('category')
    keyword = request.GET.get('keyword')
    sort = request.GET.get('sort')
    if not category:
        category = 'title'

    if not keyword:
        keyword = ''

    if not sort:
        sort = 'recent'

    item_list = None
    if category == 'title':
        item_list = Item.objects.filter(title__icontains=keyword)
    elif category == 'username':
        item_list = Item.objects.filter(user__username__icontains=keyword)
    elif category == 'content':
        item_list = Item.objects.filter(content__icontains=keyword)

    if sort == 'recent':
        item_list = item_list.order_by('-created_at')
    elif sort == 'click':
        item_list = item_list.all().order_by('-click_count')
    elif sort == 'like':
        item_list = item_list.annotate(like_count=Count('like_users')).order_by('-like_count')

    item_context_list = []
    for item in item_list:
        item_context = {
            'item': item,
            'url': '',
            'like_count': item.like_users.count(),
            'price_comma': "{:,}".format(item.price)
        }
        if item.item_images.exists():
            item_context['url'] = item.item_images.all()[0].filepath.url

        item_context_list.append(item_context)

    context = {
        'item_context_list': item_context_list,
        'sort': sort
    }
    return render(request, 'items/index.html', context)


def item_detail(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    item.click_count += 1
    item.save()

    is_like_on = item.like_users.filter(id=request.user.id).exists()

    item_context = {
        'item': item,
        'id': item.id,
        'title': item.title,
        'user': item.user.username,
        'content': item.content,
        'like': item.like_users.count(),
        'images': [],
        'is_like_on': is_like_on
    }
    if item.item_images.exists():
        for image in item.item_images.all():
            item_context['images'].append(image.filepath.url)

    context = {
        'item': item_context
    }
    return render(request, 'items/item_detail.html', context)


def register(request: HttpRequest):
    return render(request, 'items/register.html')


@require_POST
def delete(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    item.delete()

    print(f'delete. id = {id}')
    return redirect("items:index")


@require_GET
def update(request: HttpRequest, id):
    item = get_object_or_404(Item, id=id)
    context = {
        'id': item.id,
        'title': item.title,
        'price': item.price,
        'content': item.content,
        'images': []
    }
    if item.item_images:
        for image in item.item_images.all():
            context['images'].append(
                {
                    'id': image.id,
                    'url': image.filepath.url
                })

    return render(request, 'items/register.html', context)


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


@require_POST
def do_register(request: HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is not None:
            item = get_object_or_404(Item, id=id)
            delete_image_id_list = request.POST.getlist('deleteImageId[]')
            images = Image.objects.filter(id__in=delete_image_id_list)
            images.delete()
        else:
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

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded or invalid request'})


@require_POST
def like(request: HttpRequest, id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=id)

        if item.like_users.filter(id=request.user.id).exists():
            print('remove like')
            item.like_users.remove(request.user)
        else:
            print('add like')
            item.like_users.add(request.user)
    else:
        return redirect("items:item_detail", id)

    return redirect("items:item_detail", id)
