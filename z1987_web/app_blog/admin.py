from django.contrib import admin

from app_blog.models import Blog, BlogBrowse, BlogBrowseSkipIp


admin.site.site_header = "千里目博客系统"
admin.site.site_title = "博客"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("blog_id", "title", "active", "show_type", "browse_count", "like_count")
    search_fields = ("title", "content")
    list_filter = ("show_type",)
    list_display_links = ("blog_id", "title")
    ordering = ("-blog_id",)
    readonly_fields = ("blog_md5",)


@admin.register(BlogBrowse)
class BlogBrowseAdmin(admin.ModelAdmin):
    list_display = ("blog_browse_id", "active", "dt_created", "dt_updated", "blog", "user_ip")
    search_fields = ("user_ip", "blog__title", "blog__content")
    list_filter = ("active",)
    list_display_links = ("blog_browse_id",)
    ordering = ("-blog_browse_id",)


@admin.register(BlogBrowseSkipIp)
class BlogBrowseSkipIpAdmin(admin.ModelAdmin):
    list_display = ("skip_id", "active", "dt_created", "dt_updated", "ip")
    search_fields = ("ip",)
    list_filter = ("active",)
    list_display_links = ("skip_id", "ip")
    ordering = ("-skip_id",)

