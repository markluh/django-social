from django import forms
from .models import Post, Comment, Community, Profile, Status
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image", "community"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent"]

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["name", "description"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["text"]
