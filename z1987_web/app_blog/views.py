from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from app_blog.models import Blog, BlogBrowse, BlogBrowseSkipIp

from sysadmin.z1987_class.z1987_page import Page
from sysadmin.z1987_glib.my_tool import init_response_data


def blog(request):
    """
    获取博客列表
    :param request:
    :return:
    """

    # 初始化返回的数据
    response_data = init_response_data()

    # 设置查询参数
    blog_params = {
        "active": True,
        "show_type": "external",
    }

    blog_query_set = Blog.objects.filter(**blog_params).values("blog_md5", "title", "content").order_by("-blog_id")

    # 查看是否有传入搜索内容，有的话，从title或content中过滤包含搜索内容的blog
    search_field = request.GET.get("search_field", "")
    if search_field:
        # 将搜索内容按空格分开，并对每一个进行搜索处理
        for search_keyword in search_field.split():
            search_keyword = search_keyword.strip()
            if search_keyword:
                blog_query_set = blog_query_set.filter(
                    Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword)
                )

    # 获取分页信息
    p_obj = Page(request)

    data = blog_query_set[p_obj.page_start:p_obj.page_end]

    if data.exists():
        # 每个blog内容显示的最大长度
        max_content_length = 150

        for row in data:
            content = row.get("content")

            if content and len(content) > max_content_length:
                row["content"] = "%s%s" % (str(content[:max_content_length]), "...")

    # 设置返回参数
    response_data["results"] = data
    response_data["search_field"] = search_field
    response_data["results_count"] = blog_query_set.count()
    response_data["page_info"] = p_obj.page_info(response_data["results_count"], request.path, search_field)

    return render(request, "blog/blog.html", response_data)


def blog_detail(request, blog_md5):
    """
    博客详情页
    :param request:
    :param blog_md5:
    :return:
    """

    # 初始化api返回值
    response_data = init_response_data()

    # 设置查询参数
    blog_detail_params = {
        "active": True,
        "blog_md5": blog_md5,
        "show_type": "external",
    }

    # 是否能够获取到相应的博客信息
    has_blog = False

    try:
        blog_obj = Blog.objects.get(**blog_detail_params)

        # 统计浏览次数
        _increase_browse_count(request, blog_obj)

        data = model_to_dict(blog_obj)

        # 处理参考网址
        if data.get("reference_url") is not None:
            data["reference_url_list"] = \
                [_process_reference_url(url.strip()) for url in data.get("reference_url").split("\n") if url.strip()]
        else:
            data["reference_url_list"] = list()

        response_data["blog"] = data
        has_blog = True
    except Exception as e:
        del e

    if has_blog:
        return render(request, "blog/blog_detail.html", response_data)
    else:
        return HttpResponseRedirect(reverse("blog"))


def outside_redirect(request, url):
    """
    跳转到外部链接
    :param request:
    :param url:
    :return:
    """

    del request

    if url.startswith("http") or url.startswith("https"):
        pass
    else:
        url = "http://%s" % url

    return HttpResponseRedirect(url)


# ---- 内部函数 START ---- #

def _increase_browse_count(request, blog_obj):
    """
    记录博客被浏览的情况
    :param request:
    :param blog_obj:
    :return:
    """

    if isinstance(blog_obj, Blog):
        # 获取访问者ip
        visitor_ip = _get_visitor_ip(request)

        # 确认信息有效性
        if visitor_ip:
            # 将blog浏览量+1
            blog_obj.browse_count += 1
            blog_obj.save()

            # 保存博客浏览情况
            blog_browse_obj = BlogBrowse()
            blog_browse_obj.blog = blog_obj
            blog_browse_obj.user_ip = visitor_ip
            blog_browse_obj.save()


def _get_visitor_ip(request):
    """
    获取访问者ip
    :param request:
    :return:
    """

    if "HTTP_X_FORWARDED_FOR" in request.META.keys():
        user_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        user_ip = request.META.get("REMOTE_ADDR")

    # 查看获取到的IP是否在博客浏览量应忽略的IP列表中
    if user_ip is not None:
        try:
            skip_ip_obj = BlogBrowseSkipIp.objects.get(ip=user_ip)
        except BlogBrowseSkipIp.DoesNotExist:
            pass
        else:
            del skip_ip_obj
            user_ip = ""
    else:
        user_ip = ""

    return user_ip


def _process_reference_url(url):
    # 处理参考链接，将不是以http和https开头的url进行处理

    if url.startswith("http") or url.startswith("https"):
        pass
    else:
        url = "http://%s" % url

    return url


# ---- 内部函数 END ---- #
