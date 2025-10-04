from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),

    # posts
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    # communities
    path("communities/create/", views.create_community, name="create_community"),
    path("communities/<int:community_id>/", views.community_detail, name="community_detail"),
    path("communities/<int:community_id>/join/", views.join_community, name="join_community"),
    path("communities/<int:community_id>/leave/", views.leave_community, name="leave_community"),

    # profiles & follow
    path("profile/", views.profile_page, name="profile"),
    path("profile/<str:username>/", views.profile_page, name="profile_public"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("unfollow/<str:username>/", views.unfollow_user, name="unfollow_user"),

    # status
    path("status/create/", views.status_create, name="status_create"),

    # chat
    path("chat/<str:username>/", views.chat_with, name="chat_with"),
    path("chat/<str:username>/send/", views.send_message, name="send_message"),
]
