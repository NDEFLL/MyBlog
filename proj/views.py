from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from connmysql import conn_mysql
import pandas as pd
import os
from django.conf import settings
from django.templatetags.static import static

# Create your views here.

# 读取评论数据
# sql = "select * from playlist;"
#
# conn = conn_mysql()
# cursor = conn.cursor()
# cursor.execute(sql)
# data = cursor.fetchall()


def show_top5(request):
    # 读取CSV数据
    top5 = pd.read_csv("proj/musicproj/top5_hot.csv")

    # 转换为字典列表（方便模板渲染）
    top5_data = top5.to_dict('records')
    # print(top5_data)

    # 2. 图片配置
    PICTURE_ROOT = "F:/项目/网易云音乐/Data/picture/"

    for item in top5_data:
        playlist_id = str(item['playlist_id'])
        img_filename = f"{playlist_id}.jpg"
        img_path = os.path.join(PICTURE_ROOT, img_filename)

        # 3. 生成正确的图片URL
        if os.path.exists(img_path):
            if settings.DEBUG:  # 开发环境
                item['image_url'] = os.path.join(settings.MEDIA_URL, img_filename)
            else:  # 生产环境
                item['image_url'] = f"/media/{img_filename}"  # 需配置Nginx别名
        else:
            item['image_url'] = static('img/default.jpg')  # 使用static标签

    return render(request, 'music.html', {'top5': top5_data})


def project_show(request):
    return render(request, 'projshow.html')

def bilibili_proj(request):
    return render(request, 'bilibili_proj.html')

def gxddc_proj(request):
    return render(request,'gxddc.html')

def heart_proj(request):
    return render(request,'heart.html')

def yq_proj(request):
    return render(request,'yq.html')