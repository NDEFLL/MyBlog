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
    articles = Article.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    return render(request, 'blog/article_detail.html', {'article': article})

@login_required
@user_passes_test(is_admin)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, '文章发布成功！')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, '文章删除成功！')
    return redirect('article_list')