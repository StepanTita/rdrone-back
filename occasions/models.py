from django.db import models

from authentication.models import CustomUser


class Occasion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    image = models.TextField()
    lat = models.CharField(max_length=100)
    lng = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.IntegerField()
    status = models.CharField(max_length=100, default='')
    resolved = models.IntegerField()
    rejected = models.IntegerField()


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    reply_to = models.ForeignKey('Comment', on_delete=models.CASCADE, default=None, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)


class Resolutions(models.Model):
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resolved = models.BigIntegerField()
    rejected = models.BigIntegerField()
