from time import sleep
from datetime import datetime

from django import forms
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from wheel.metadata import requires_to_requires_dist

from twitter.forms import TweetForm
from twitter.models import Tweet


def update_last_read_datetime(request) -> datetime | None:
    last_data = None
    if request.user.is_authenticated:
        last_data = cache.get(f"last_read_datetime_{request.user.id}")
        cache.set(f"last_read_datetime_{request.user.id}", datetime.now().isoformat())
    return last_data

def get_last_read_datetime(request) -> datetime | None:
    if request.user.is_authenticated:
        datetime_str = cache.get(f"last_read_datetime_{request.user.id}")
        return datetime.fromisoformat(datetime_str) if datetime_str else None


def index(request):
    update_last_read_datetime(request)
    if request.user.is_authenticated:
        followings = request.user.following.all().values_list('following__id')
        tweets = Tweet.objects.filter(created_by__in=followings).prefetch_related("created_by").order_by("-created_datetime")
    else:
        tweets = Tweet.objects.all().prefetch_related("created_by").order_by("-created_datetime")
    context = {
        "tweets": [{
            "content": tweet.content,
            "created_by": tweet.created_by.username,
        } for tweet in tweets]
    }
    return render(request, "twitter/pages/index.html", context)


@require_GET
def tweets(request):
    tweets = Tweet.objects.all().prefetch_related("created_by").order_by("-created_datetime")

    context = {
        "tweets": [{
            "content": tweet.content,
            "created_by": tweet.created_by.username,
        } for tweet in tweets]
    }
    return render(request, "twitter/component/tweets.html", context)

@require_GET
def updated_tweets(request):
    last_update = update_last_read_datetime(request)
    tweets = Tweet.objects.all().prefetch_related("created_by").order_by("-created_datetime")
    new_tweets = list(tweets.filter(created_datetime__gt=last_update)) if last_update else []


    context = {
        "tweets": [{
            "content": tweet.content,
            "created_by": tweet.created_by.username,
        } for tweet in new_tweets]
    }
    return render(request, "twitter/component/tweets.html", context)


@require_POST
@login_required
def post_tweet(request):
    form = TweetForm(request.POST)
    sleep(3.0)
    if form.is_valid():
        tweet = Tweet(content=form.cleaned_data["content"], created_by=request.user, updated_by=request.user)
        tweet.save()
        context = {
            "tweet": {
                "content": tweet.content,
                "created_at": tweet.created_datetime,
                "created_by": tweet.created_by.username,
            }
        }
        return render(request, "twitter/component/tweet.html", context)
    # return validation error
    raise forms.ValidationError("Tweet validation error")


@require_GET
@login_required
def check_new_tweet(request):
    last_read_datetime = get_last_read_datetime(request)

    if last_read_datetime is None:
        num_new_tweets = 0
    else:
        followings = request.user.following.all().values_list('following__id')
        tweets = Tweet.objects.filter(created_by__in=followings).prefetch_related("created_by").order_by("-created_datetime")
        num_new_tweets = tweets.filter(created_datetime__gt=last_read_datetime).count()
    context = {
        "num_new_tweets": num_new_tweets,
    }
    return render(request, "twitter/component/check_new_tweets.html", context)
