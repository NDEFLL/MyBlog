from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_show, name='project_show'),
    path('gxddc/',views.gxddc_proj,name='gxddc_proj'),
    path('heart_proj/',views.heart_proj,name='heart_proj'),
    path('yq_proj/',views.yq_proj,name='yq_proj'),
    # path('bilibili/', views.bilibili_proj, name='bilibili_proj'),
] 