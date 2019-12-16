#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2019/3/18 20:33
# @Author  : zhanhui
# @File    : urls.py


from django.urls import path

from app_blog import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("detail/<str:blog_md5>", views.blog_detail, name="blog_detail"),
    path("blog_redirect/<path:url>", views.outside_redirect, name="outside_redirect"),
]
