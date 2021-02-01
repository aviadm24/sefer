from django.db import models
from django.contrib.auth.models import User


class Index(models.Model):
    url = models.URLField(max_length=200)
    json = models.JSONField()

    def __str__(self):
      return self.url


class Texts(models.Model):
    url = models.URLField(max_length=200)
    json = models.JSONField()

    def __str__(self):
        return self.url


class Links(models.Model):
    url = models.URLField(max_length=200)
    json = models.JSONField()

    def __str__(self):
        return self.url


class TitleMeta(models.Model):
    url = models.URLField(max_length=200)
    json = models.JSONField()

    def __str__(self):
        return self.url

# class Ycomment(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCAD)


class MainCategories(models.Model):
    catJson = models.JSONField()
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.cat
