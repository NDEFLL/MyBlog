from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Post, Profile, ExternalLink, Article
from .forms import ArticleForm

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
# 需要用户登录并且是管理员才能访问
@user_passes_test(is_admin)
def article_create(request):
    # 如果请求方法是 POST，说明用户提交了创建文章的表单，验证表单数据的有效性
    # 如果有效则保存文章，并将文章的作者设置为当前登录用户，最后跳转到文章详情页
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.content = request.POST.get('content')
            article.save()
            messages.success(request, '文章发布成功！')
            return redirect('article_detail', pk=article.pk)
    # 如果请求方法是 GET，显示一个空的文章表单。
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
# 需要用户登录并且是管理员才能访问
@user_passes_test(is_admin)
def article_edit(request, pk):
    # 根据文章的主键 pk 从数据库中获取对应的文章对象，如果文章不存在则返回 404 错误
    article = get_object_or_404(Article, pk=pk)
    # 如果请求方法是 POST，说明用户提交了编辑文章的表单
    # 验证表单数据的有效性，如果有效则更新文章信息，最后跳转到文章详情页
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('article_detail', pk=article.pk)
    else:
        # 如果请求方法是 GET，显示一个已填充文章信息的表单。
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})

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