from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from .models import *

from .forms import CustomUserChangeForm, CustomUserCreationForm
import json
import hashlib


def login(request: HttpRequest):
    context = {
        'error_message': ''
    }

    if request.method == "POST":
        username = request.POST.get('userid')
        user_password = request.POST.get('userpw')
        print(username, user_password)
        user = authenticate(request, username=username, password=user_password)
        print(f'user={user}')
        if user is not None:
            auth_login(request, user)
            return redirect('items:index')
        else:
            context['error_message'] = "아이디 또는 비밀번호가 일치하지 않습니다."

    return render(request, "accounts/login.html", context)


def logout(request: HttpRequest):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("items:index")


# @acc_bp.route("/checkNameDup", methods=["POST"])
@require_POST
def check_name_dup(request: HttpRequest):
    data = json.loads(request.body)
    existing_user: User = User.objects.filter(username=data.get('username'))
    if existing_user:
        return JsonResponse({"isDuplicate": True})  # 사용자 이름이 이미 존재함
    return JsonResponse({"isDuplicate": False})


def signup(request: HttpRequest):
    if request.method == "POST":
        password = request.POST.get('regPass')
        username = request.POST.get('regName')
        email = request.POST.get('regEmail')
        image = request.POST.get('regImage')
        comment = request.POST.get('regComment')

        user = User.objects.create_user(username=username, password=password, email=email, image=image, comment=comment)
        user.save()

        auth_login(request, user)

        return redirect('items:index')
    else:
        return render(request, "accounts/signup.html")


def user_list(request: HttpRequest):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'accounts/user_list.html', context)


@require_POST
def follow(request: HttpRequest, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), pk=user_id)
        if request.user != user:
            if request.user in user.followers.all():
                print('remove')
                user.followers.remove(request.user)
            else:
                print('add')
                user.followers.add(request.user)
    return redirect("accounts:user_list")


@require_POST
def delete(request: HttpRequest):
    print('delete')
    return redirect("items:index")


@require_http_methods(["GET", "POST"])
def update(request):
    print('update')
    return render(request, "accounts/update.html")


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("items:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)


def profile(request: HttpRequest):
    date_str = request.user.date_joined.strftime("%Y-%m-%d %H:%M")
    print(date_str)
    return render(request, 'accounts/profile.html')
