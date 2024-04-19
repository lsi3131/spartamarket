from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST


def users(request):
    return render(request, 'users/users.html')


def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {
        "member": member,
    }
    return render(request, "users/profile.html", context)


@require_POST
def follow(request: HttpRequest, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        print(member)
        if request.user != member:
            if request.user in member.followers.all():
                print('remove')
                member.followers.remove(request.user)
            else:
                print('add')
                member.followers.add(request.user)
        return redirect("users:profile", member.username)
    return redirect("accounts:login")
