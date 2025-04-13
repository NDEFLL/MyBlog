from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django_ckeditor_5.views import upload_file

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('/ckeditor5/upload/', upload_file, name='ckeditor_5_upload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
