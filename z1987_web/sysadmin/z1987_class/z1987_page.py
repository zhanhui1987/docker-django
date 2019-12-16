#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/8/31 16:15
# @Author  : Zhanhui
# @File    : z1987_page.py


from django.core.handlers.wsgi import WSGIRequest


class Page(object):
    def __init__(self, request=None):
        """
        根据传入的 request 或 page和size，获取分页数据：page_start和page_end
        :param request: 请求对象，应是 rest_framework.request.Request 类型
        """

        # 默认页码为第一页，每页数量为30
        self._page = 1
        self._size = 30

        # 初始化默认属性
        self._init_attribute()

        self._request = request

        # 获取page和size
        self._get_page_size_from_request()

        # 计算page_start和page_end
        self._set_page_start_and_end()

    def _init_attribute(self):
        self.page_start = 0
        self.page_end = 0
        self.error_msg = None

    def _set_page_start_and_end(self):
        """
        计算page_start和page_end
        :return:
        """

        if self.error_msg is None:
            self._calculate_page_start_and_end()

    def _calculate_page_start_and_end(self):
        # 根据page_no和page_size获取分页信息

        # 获取开始和结束位置
        try:
            self.page_start = (self._page - 1) * self._size
            self.page_end = self._page * self._size

            if self.page_start < 0:
                self.page_start = 0
            if self.page_end < 0:
                self.page_end = 0
        except Exception as e:
            self.error_msg = e

    def _get_page_size_from_request(self):
        # 从request中获取page和size

        if isinstance(self._request, WSGIRequest):
            # 从request的get中获取page和size
            try:
                self._page = int(self._request.GET.get("page"))
            except (TypeError, ValueError):
                pass

            try:
                self._size = int(self._request.GET.get("size"))
            except (TypeError, ValueError):
                pass
        else:
            self.error_msg = "传入的request错误的类型： %s" % type(self._request)

    def page_info(self, result_total, page_url, search_field=None):
        """
        获取分页相关的数据
        :param result_total: 查询的数据总量
        :param page_url: 当前页的链接，用于显示页码条时使用
        :param search_field: 搜索关键字
        :return:
        """

        # 确保传入的total是有效的数字
        try:
            result_total = abs(int(result_total))
        except (TypeError, ValueError):
            result_total = 0

        # 根据result_total和page_size获取最大页码数

        max_page_no, remainder = divmod(result_total, self._size)
        if remainder:
            max_page_no += 1

        # 查看页码数是否超过最大页码数
        if max_page_no:
            if self._page > max_page_no:
                self._page = max_page_no
        else:
            self._page = 1

        # 设置当前页码数
        current_page_no = self._page

        # 设置当前页面上显示的数据总数
        if result_total:
            current_page_data_count = self._size
            # 若当前是最后一页，则需要对当前页面上的数据总数进行调整
            if current_page_no == max_page_no:
                current_page_data_count = result_total - (current_page_no - 1) * self._size
        else:
            current_page_data_count = 0

        # 获取page_list，用于显示跳转用的页码条
        page_list = self._get_page_list(current_page_no, max_page_no, page_url, self._size, search_field)

        page_info = {
            "page_size": self._size,
            "total_count": result_total,
            "current_page_no": current_page_no,
            "page_list": page_list,
            "current_page_data_count": current_page_data_count,
            "max_page_no": max_page_no,
        }

        return page_info

    @staticmethod
    def _get_page_list(current_page_no, max_page_no, page_url, page_size, search_field):
        # 获取显示页码条所用的page_list

        page_list = list()

        # 设置当前页码前后显示的页码数量，只显示这几个
        show_page_no_count = 2
        # 设置是否有隐藏的上一页/下一页的页码
        no_hide_previous_page_no = True
        no_hide_last_page_no = True

        # 将首页的信息放入page_list中
        page_list.append({"page_no": 1, "page_show": "第一页"})

        # 将所有的页码放入page_list中，需注意的是，要考虑show_page_no_count（即当前页面前后显示几个页码）
        for i in range(1, max_page_no + 1):
            # 设置每一页的页码数和是否有跳转链接，page_no代表页码数，has_url代表该页码数是否有对应的跳转链接。
            page_data = {"page_no": i}

            # 若页码i比当前页码小的值，大于显示的页码数，则应将其替换为其他字符（...），且这种情况应只出现一次。
            if current_page_no - i > show_page_no_count:
                if no_hide_previous_page_no:
                    page_data["page_no"] = "..."

                    # 设置了比当前页码小的隐藏页码之后，后续再有类似的情况则不应再进行设置。
                    no_hide_previous_page_no = False
                else:
                    continue

            # 若页码i比当前页码大的值，大于显示的页码数，则应将其替换为其他字符（...），且这种情况应只出现一次。
            if i - current_page_no > show_page_no_count:
                if no_hide_last_page_no:
                    page_data["page_no"] = "..."

                    # 设置了比当前页码大的隐藏页码之后，后续再有类似的情况则不应再进行设置。
                    no_hide_last_page_no = False
                else:
                    continue

            page_list.append(page_data)

        # 将最后一页的信息放入page_list中
        page_list.append({"page_no": max_page_no, "page_show": "最后一页"})

        # 设置page_list中，每一个page_no的跳转链接。有跳转链接的条件是：非当前页码且是数字类型页码（区别于隐藏页码）
        for page_data in page_list:
            if isinstance(page_data["page_no"], int) and page_data["page_no"] != current_page_no:
                page_data["page_url"] = "%s?page=%s&size=%s" % (page_url, page_data["page_no"], page_size)

                if search_field:
                    page_data["page_url"] = "%s&search_field=%s" % (page_data["page_url"], search_field)

        return page_list
