#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/11/20 18:05
# @Author  : Zhanhui
# @File    : logging_handlers.py


import os
import re
import time

from logging import FileHandler


class SafeFileHandler(FileHandler):
    def __init__(self, file_name, mode="a", encoding=None, delay=0, backup_count=0):
        """
        Use the specified filename for streamed logging
        """
        FileHandler.__init__(self, file_name, mode, encoding, delay)

        self.mode = mode
        self.encoding = encoding
        self.suffix_format = "%Y-%m-%d"
        self.suffix_time = ""

        self.backup_count = backup_count
        self.file_name = file_name

        if not hasattr(self, "delay"):
            self.delay = delay

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_base_filename():
                self.build_base_filename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            del e
            self.handleError(record)

        # clean redundant backup
        self._clean_backup()

    def check_base_filename(self):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        time_tuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix_format, time_tuple) or not os.path.exists(
                self.baseFilename + "." + self.suffix_time):
            return True
        else:
            return False

    def build_base_filename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        current_time_tuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix_format, current_time_tuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = "a"
        if not self.delay:
            self.stream = self._open()

    def _clean_backup(self):
        """
        Clean redundant backup
        :return:
        """

        if self.backup_count > 0:
            for s in self._get_files_to_delete():
                os.remove(s)

    def _get_files_to_delete(self):
        """
        Determine the files to delete when rolling over.
        :return:
        """

        files = list()

        # get log files list.
        dir_name, base_name = os.path.split(self.file_name)
        file_list = os.listdir(dir_name)

        ext_match = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$")

        prefix = "%s." % base_name
        prefix_len = len(prefix)

        if file_list:
            for file_name in file_list:
                if file_name[:prefix_len] == prefix:
                    suffix = file_name[prefix_len:]
                    if ext_match.match(suffix):
                        files.append(os.path.join(dir_name, file_name))

        if files:
            files.sort()
            if len(files) < self.backup_count:
                files = list()
            else:
                files = files[:len(files) - self.backup_count]

        return files
