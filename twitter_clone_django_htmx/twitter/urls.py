from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tweets", views.tweets, name="tweets"),
    path("post_tweet", views.post_tweet, name="post_tweet"),
    path("new_tweets", views.check_new_tweet, name="new_tweets"),
]