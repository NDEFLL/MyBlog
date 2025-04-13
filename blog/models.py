from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    bio = models.TextField(blank=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    music_url = models.URLField(blank=True)

class ExternalLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    # content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)
    content = CKEditor5Field('内容')  # 使用 CKEditor 5
   # config_name指定ckeditor配置文件，不指定就使用default

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])




