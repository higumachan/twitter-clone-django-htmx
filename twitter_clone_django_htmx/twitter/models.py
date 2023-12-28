import uuid

from django.db import models

from accounts.models import CustomUser
from commons.models import UserTimestampedModel


# Create your models here.

class Tweet(UserTimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=280)


class Like(UserTimestampedModel):
    id = models.UUIDField(primary_key=True, editable=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
