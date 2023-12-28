from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from wheel.metadata import requires_to_requires_dist

from twitter.forms import TweetForm
from twitter.models import Tweet


def index(request):
    tweets = Tweet.objects.all().prefetch_related("created_by").order_by("-created_datetime")
    context = {
        "tweets": [{
            "content": tweet.content,
            "created_at": tweet.created_by.username,
        } for tweet in tweets]
    }
    return render(request, "twitter/pages/index.html", context)


@require_GET
def tweets(request):
    tweets = Tweet.objects.all().prefetch_related("created_by").order_by("-created_datetime")
    context = {
        "tweets": [{
            "content": tweet.content,
            "created_at": tweet.created_by.username,
        } for tweet in tweets]
    }
    return render(request, "twitter/component/tweets.html", context)

@require_POST
@login_required
def post_tweet(request):
    form = TweetForm(request.POST)
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
