from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
import json

from .models import User, Post, Follow_data


def index(request):
    if request.method == "POST":
        post_text = request.POST.get("newpost", "").strip()
        user = request.user

        if not post_text:
            messages.error(request, "Post content cannot be empty.")
        else:
            # Create and save the new post
            Post.objects.create(user=user, text=post_text)
        return HttpResponseRedirect(reverse("index"))
    else:
        posts_text = Post.objects.all().order_by('-date_time')
        paginator = Paginator(posts_text, 10) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
           "page_obj": page_obj
        })


def user_profile_view(request, user_id):
    if request.method == "POST":
        follow_value = request.POST.get("follow_button_profile")
        profile_id_follow = request.POST.get("follow_button_profile_id")
        user = request.user

        try:
            profile_user = User.objects.get(id=profile_id_follow)
        except User.DoesNotExist:
            return HttpResponse("User does not exist.")

        follows_data, created = Follow_data.objects.get_or_create(user=user)
        follower_data, _ = Follow_data.objects.get_or_create(user_id=user_id)

        if follow_value == "Unfollow":
            follows_data.follows.remove(profile_user)
            follower_data.followers.remove(user)
        else:
            follows_data.follows.add(profile_user)
            follower_data.followers.add(user)

        return HttpResponseRedirect(reverse("user_profile", args=[user_id]))

    else:
        try:
            profile_user = User.objects.get(id=user_id)
        except User.DoesNotExist: 
            return HttpResponse("User does not exist.")

        user_posts = Post.objects.filter(user=user_id).order_by('-date_time')
        paginator = Paginator(user_posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        follow_data = Follow_data.objects.filter(user=user_id).first()
        n_followers = follow_data.followers.count() if follow_data else 0
        n_follows = follow_data.follows.count() if follow_data else 0

        user = request.user
        if not user.is_authenticated:
            follow_info = "Not authenticated"
        elif user == profile_user:
            follow_info = "Do not show"
        elif follow_data and user in follow_data.followers.all():
            follow_info = "Unfollow"
        else:
            follow_info = "Follow"

        return render(request, "network/user_page.html", {
            "page_obj": page_obj,
            "username": profile_user.username,
            "n_follows": n_follows,
            "n_followers": n_followers,
            "follow_info": follow_info,
            "profile_id": profile_user.id,
            "user": user
        })


@login_required(login_url="login")
def following_views(request):
    user_signin = request.user
    follow_data = Follow_data.objects.filter(user=user_signin).first()
    
    if not follow_data:
        return HttpResponse("No following data available.")

    followed_users = follow_data.follows.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-date_time')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@login_required(login_url="login")
def edit_post_views(request, post_id):
    edited_post = get_object_or_404(Post, id=post_id)
    if request.user != edited_post.user:
        return HttpResponse("You do not have permission to edit this post.")

    if request.method == "POST":
        data = json.loads(request.body)
        new_text = data.get("newpost_text", "").strip()

        if not new_text:
            return JsonResponse({"error": "Post content cannot be empty."}, status=400)

        edited_post.text = new_text
        edited_post.save()
        return JsonResponse({"success_message": "Post edited successfully."}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def likes_change_API_views(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not signed in"}, status=403)

        data = json.loads(request.body)
        post_id = data.get("post_id")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist"}, status=404)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        likes_num = post.likes.count()
        return JsonResponse({
            "message": "Success",
            "likes_num": likes_num
        }, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "network/login.html")
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "network/register.html")

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "network/register.html")

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
