from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.static import serve

from z1987_web.settings import STATIC_ROOT
from app_blog import views as blog_views


# admin链接
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
]

# 首页链接
urlpatterns += [
    path("", blog_views.blog, name="index"),
]

# 静态文件链接
urlpatterns += [
    path('favicon.ico', RedirectView.as_view(url='static/image/favicon.ico')),
    path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),
]

# blog链接
urlpatterns += [
    path("blog/", include("app_blog.urls")),
]
