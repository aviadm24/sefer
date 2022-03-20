# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Index(models.Model):
#     url = models.URLField(max_length=200)
#     json = models.JSONField()
#
#     def __str__(self):
#         return self.url
#
#
# class Texts(models.Model):
#     url = models.URLField(max_length=200)
#     json = models.JSONField()
#
#     def __str__(self):
#         return self.url
#
#
# class Commentators(models.Model):
#     main_text_url = models.ForeignKey(Texts, on_delete=models.CASCADE)
#     url = models.URLField(max_length=200)
#     json = models.JSONField()
#
#     def __str__(self):
#         return self.url
#
#
# class Links(models.Model):
#     url = models.URLField(max_length=200)
#     json = models.JSONField()
#
#     def __str__(self):
#         return self.url
#
#
# class TitleMeta(models.Model):
#     url = models.URLField(max_length=200)
#     json = models.JSONField()
#
#     def __str__(self):
#         return self.url
#
#
# class Ycomment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField(null=True, blank=True)
#     url = models.CharField(max_length=200)
#     comment_reference = models.CharField(null=True, blank=True, max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.url
#
#
# class Yfiles(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(null=True, blank=True)
#     url = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.pk
#
#
# class MainCategories(models.Model):
#     catJson = models.JSONField()
#     url = models.URLField(max_length=200)
#
#     def __str__(self):
#         return self.url
