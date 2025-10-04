from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import models


def home(request):
    return JsonResponse({"message": "Hello from Django in CodeSandbox!"})



def logout(request):
    auth_logout(request)
    return render(request, "login.html", {"message": "Logged out"})


def home_page(request):
    return render(request, "home.html")

@login_required(login_url="auth")
def profile_page(request):
    return render(request, "profile.html")

@login_required(login_url="auth")
def posts_page(request):
    return render(request, "posts.html")

@login_required(login_url="auth")
def community_page(request):
    return render(request, "community.html")
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home_page")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=email, password=password)
            return render(request, "login.html", {"message": "Signup successful. Please log in."})
        else:
            return render(request, "signup.html", {"error": "User already exists"})
    return render(request, "signup.html")

from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment, Community, CommunityMembership, Follow, Status, Message
from .forms import PostForm, CommentForm, CommunityForm, ProfileForm, StatusForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden

# Ensure user profile exists when accessing
def ensure_profile(user):
    Profile.objects.get_or_create(user=user)

@login_required(login_url="login")
def home_page(request):
    ensure_profile(request.user)
    # show recent posts from people you follow + communities you're in
    following_ids = request.user.following_set.values_list("following__id", flat=True)
    community_ids = request.user.communities.values_list("id", flat=True)
    posts = Post.objects.filter(
        models.Q(author__id__in=following_ids) |
        models.Q(community__id__in=community_ids) |
        models.Q(author=request.user)
    ).order_by("-created_at")[:50]
    return render(request, "home.html", {"posts": posts})

@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("home_page")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})

@login_required(login_url="login")
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm()
    return render(request, "post_detail.html", {"post": post, "comment_form": comment_form})

@login_required(login_url="login")
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            c.save()
            return redirect("post_detail", post_id=post.id)
    return redirect("post_detail", post_id=post.id)

@login_required(login_url="login")
def create_community(request):
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            CommunityMembership.objects.create(user=request.user, community=community)
            return redirect("community_detail", community_id=community.id)
    else:
        form = CommunityForm()
    return render(request, "create_community.html", {"form": form})

@login_required(login_url="login")
def community_detail(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    members = community.members.all()
    posts = community.posts.order_by("-created_at")
    return render(request, "community.html", {"community": community, "members": members, "posts": posts})

@login_required(login_url="login")
def join_community(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    CommunityMembership.objects.get_or_create(user=request.user, community=community)
    return redirect("community_detail", community_id=community.id)

@login_required(login_url="login")
def leave_community(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    CommunityMembership.objects.filter(user=request.user, community=community).delete()
    return redirect("community_detail", community_id=community.id)

@login_required(login_url="login")
def follow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return HttpResponseForbidden("Cannot follow yourself.")
    Follow.objects.get_or_create(follower=request.user, following=target)
    return redirect("profile", username=username)

@login_required(login_url="login")
def unfollow_user(request, username):
    target = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=target).delete()
    return redirect("profile", username=username)

@login_required(login_url="login")
def profile_page(request, username=None):
    # if username not provided show current
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    ensure_profile(user)
    is_following = False
    if user != request.user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, "profile.html", {"profile_user": user, "is_following": is_following})

@login_required(login_url="login")
def edit_profile(request):
    ensure_profile(request.user)
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})

@login_required(login_url="login")
def status_create(request):
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            return redirect("home_page")
    return redirect("home_page")

# Simple chat views
@login_required(login_url="login")
def chat_with(request, username):
    other = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user, recipient=other) |
         models.Q(sender=other, recipient=request.user))
    ).order_by("created_at")
    return render(request, "chat.html", {"other": other, "messages": messages})

@login_required(login_url="login")
def send_message(request, username):
    if request.method == "POST":
        other = get_object_or_404(User, username=username)
        text = request.POST.get("text")
        if text:
            Message.objects.create(sender=request.user, recipient=other, text=text)
            return redirect("chat_with", username=username)
    return redirect("chat_with", username=username)
