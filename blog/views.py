from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Post, Profile, ExternalLink

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