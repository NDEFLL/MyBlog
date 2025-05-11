from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import base64

from django_ckeditor_5.fields import CKEditor5Field
from django.utils.safestring import mark_safe


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
    content = CKEditor5Field('内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']      # 指定按照created_at字段进行排序

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Message(models.Model):
    CONTACT_CHOICES = [
        ('email', '邮箱'),
        ('qq', 'QQ'),
        ('wechat', '微信'),
        ('phone', '手机号码'),
    ]

    name = models.CharField(max_length=100, verbose_name='姓名')
    contact_type = models.CharField(max_length=10, choices=CONTACT_CHOICES, verbose_name='联系方式类型')
    contact_info = models.CharField(max_length=100, verbose_name='联系方式')
    content = models.TextField(verbose_name='留言内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='留言时间')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = '留言'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# class Image(models.Model):
#     image_data = models.BinaryField() #存储图片的二进制数据
#     uploaded_at = models.DateTimeField("上传时间",auto_now_add=True)    #图片上传时间（auto_now_add=True 在图片上传时自动设置当前时间）
#     content_type = models.CharField("文件类型", max_length=100)  # 用于存储文件的MIME类型
#     image_name = models.CharField()

# 文章图片
# class ArticleImage(models.Model):
#     image_data = models.BinaryField() #存储图片的二进制数据
#     uploaded_at = models.DateTimeField("上传时间",auto_now_add=True)    #图片上传时间（auto_now_add=True 在图片上传时自动设置当前时间）
#     content_type = models.CharField("文件类型",max_length=100)      #用于存储文件的MIME类型
#     # 用于建立与 Article 模型的外键关系
#     # on_delete=models.CASCADE表示当关联的Article被删除时，对应的ArticleImage也会被删除
#     # related_name='image'表示在Article模型中可以通过image访问与之关联的ArticleImage对象
#     article = models.ForeignKey(Article,on_delete=models.CASCADE,
#                                 related_name='image')
#
#     # 定义模型的元数据
#     class Meta:
#         verbose_name = "文章图片"
#         verbose_name_plural = verbose_name
#
#     # 将图片转为二进制数据
#     def base64_image(self):
#         import base64
#         return f"data:{self.content_type};base64,{base64.b64encode(self.image_data).decode()}"



