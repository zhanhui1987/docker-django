"""
定义blog相关的表。
"""

from django.db import models

from app_blog.models_choice import SHOW_TYPE_CHOICE

from z1987_web.settings import BLOG_MD5_EXTRA_STR
from sysadmin.z1987_glib.my_md5 import md5


class Blog(models.Model):
    class Meta:
        db_table = "blog"
        verbose_name = "博客"
        verbose_name_plural = "博客 （blog）"
        ordering = ("-blog_id",)

    blog_id = models.AutoField(primary_key=True, verbose_name="博客编号")

    active = models.BooleanField(default=True, verbose_name="是否生效")
    dt_created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="创建时间")
    dt_updated = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    blog_md5 = models.CharField(max_length=32, db_index=True, blank=False, null=False, unique=True,
                                verbose_name="博客MD5值")

    show_type = models.CharField(max_length=10, default="internal", db_index=True, choices=SHOW_TYPE_CHOICE,
                                 verbose_name="是否对外发布")

    title = models.CharField(max_length=255, null=False, blank=False, verbose_name="博客标题")
    content = models.TextField(verbose_name="博客内容")
    reference_url = models.TextField(null=True, blank=True, verbose_name="参考链接")

    browse_count = models.IntegerField(default=0, null=False, blank=False, verbose_name="浏览总数")
    like_count = models.IntegerField(default=0, null=False, blank=False, verbose_name="点赞总数")

    def __str__(self):
        return "%s. %s" % (self.blog_id, self.title)

    # 重写save函数，以确保每个blog都有blog_md5
    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)

        if not self.blog_md5:
            self.blog_md5 = md5("%s.%s_%s" % (self.blog_id, self.title, BLOG_MD5_EXTRA_STR))
            self.save()


class BlogBrowse(models.Model):
    class Meta:
        db_table = "blog_browse"
        verbose_name = "博客浏览情况"
        verbose_name_plural = "博客浏览情况 （blog_browse）"

    blog_browse_id = models.AutoField(primary_key=True, verbose_name="博客浏览情况编号")

    active = models.BooleanField(default=True, verbose_name="是否生效")
    dt_created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="创建时间")
    dt_updated = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    blog = models.ForeignKey(Blog, default=0, related_name="blog_browse", null=True, blank=True,
                             on_delete=models.SET_DEFAULT, verbose_name="浏览的博客")

    user_ip = models.CharField(max_length=32, null=True, blank=True, verbose_name="浏览用户的IP")

    def __str__(self):
        return "%s, %s" % (self.blog_browse_id, self.blog)


class BlogBrowseSkipIp(models.Model):
    class Meta:
        db_table = "blog_browse_skip_ip"
        verbose_name = "博客浏览忽略的IP"
        verbose_name_plural = "博客浏览忽略的IP （blog_browse_skip_ip）"

    skip_id = models.AutoField(primary_key=True, verbose_name="忽略编号")

    active = models.BooleanField(default=True, verbose_name="是否生效")
    dt_created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="创建时间")
    dt_updated = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    ip = models.CharField(max_length=32, null=True, blank=True, verbose_name="忽略的IP")

    def __str__(self):
        return "%s. %s" % (self.skip_id, self.ip)
