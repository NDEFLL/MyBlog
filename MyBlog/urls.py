"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import proj.views
from proj import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('proj/', include('proj.urls')),
    path('music/', views.show_top5, name='top5'),
    path('projshow/',views.project_show,name='项目展示列表'),
    path('projshow/biliproj/',views.bilibili_proj)
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root="F:/项目/网易云音乐/Data/picture/"  # 实际路径
    )
