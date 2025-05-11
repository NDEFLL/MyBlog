from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
import os
import uuid

from .models import Post, Profile, ExternalLink, Article, Message
from .forms import ArticleForm, MessageForm


def is_admin(user):
    return user.is_superuser

def blog_home(request):
    posts = Post.objects.all().order_by('-pub_date')
    user = request.user
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None
    else:
        profile = None
    external_links = ExternalLink.objects.all()
    return render(request, 'blog.html', {'posts': posts, 'profile': profile, 'external_links': external_links})


def article_list(request):
    # 从数据库中筛选出已发布的文章（is_published=True），并按照创建时间降序排列
    articles = Article.objects.filter(is_published=True).order_by('-created_at')
    # 将筛选后的文章列表传递给 blog/article_list.html 模板进行渲染
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, pk):
    # 根据文章的主键 pk 从数据库中获取对应的文章对象，如果文章不存在则返回 404 错误
    article = get_object_or_404(Article, pk=pk)
    # 调用文章对象的 increase_views 方法，增加文章的浏览量。
    article.increase_views()
    return render(request, 'blog/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, '文章发布成功！')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {
        'form': form,
    })

@login_required
# 需要用户登录并且是管理员才能访问
@user_passes_test(is_admin)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, '文章更新成功！')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {
        'form': form,
        'article_id': article.id
    })

@login_required
# 需要用户登录并且是管理员才能访问
@user_passes_test(is_admin)
def article_delete(request, pk):
    # 根据文章的主键 pk 从数据库中获取对应的文章对象，如果文章不存在则返回 404 错误
    article = get_object_or_404(Article, pk=pk)
    # 删除文章，并跳转到文章列表页
    article.delete()
    messages.success(request, '文章删除成功！')
    return redirect('article_list')

# 上传图片
@login_required
def upload_articleimage(request):
    # 检查请求的方法是否为POST，并且请求中是否包含一个名为'image'的文件
    if request.method == 'POST' and request.FILES.get('upload'):
        try:
            # 拆功能键图片记录（先不与文章关联）
            image_file = request.FILES['upload']
            # 验证文件大小（示例限制5MB）
            if image_file.size > 5 * 1024 * 1024:
                return JsonResponse({'error': '文件大小不能超过5MB'}, status=400)
            # # 保存到数据库中
            # article_image = ArticleImage.objects.create(
            #     image_data=image_file.read(),
            #     content_type=image_file.content_type,
            #     article_id=None    #临时标记
            # )
            encoded = base64.b64encode(image_file.read()).decode()
            content_type = image_file.content_type
            # 返回 CKEditor 需要的响应格式
            return JsonResponse({
                # 用于获取上传的图片数据
                'url':f'data:{content_type};base64,{encoded}'
            })
        except Exception as e:
            return JsonResponse(
                {
                    'uploaded': False,
                    'error': {
                        'message': f'上传失败: {str(e)}'
                    }
                },status=400
            )
    return JsonResponse({
        'uploaded': False,
        'error': {'message': '无效请求'}
    },status=400)

# def get_article_image(request, image_id):
#     try:
#         image = ArticleImage.objects.get(id=image_id)
#         return HttpResponse(image.image, content_type=image.content_type)
#     except ArticleImage.DoesNotExist:
#         return HttpResponse(status=404)

def message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '留言已提交，感谢您的反馈！')
            return redirect('message')
    else:
        form = MessageForm()
    return render(request, 'blog/message.html', {'form': form})

@login_required
def message_list(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面')
        return redirect('home')
    
    message_list = Message.objects.all()
    return render(request, 'blog/message_list.html', {'message_list': message_list})

@login_required
def mark_message_read(request, message_id):
    if not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作')
        return redirect('home')
    
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    messages.success(request, '留言已标记为已读')
    return redirect('message_list')
