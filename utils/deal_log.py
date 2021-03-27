#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : deal_log.py
# @Author: itnoobzzy
# @Date  : 2021/3/16
# @Desc  : 日志处理

import time
import logging
import os

from auto_test_platform.settings import *

class DealLog:
    def __init__(self):
        self.log = ''

    def _get_log(self):
        CUR_DATE = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file_name = f'{BASE_DIR}/log/{CUR_DATE}.log'
        os.system(f'touch {file_name}')
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s[line:%(lineno)d] %(message)s',
                            level=logging.INFO,
                            filename=file_name)

        return logging

    def info(self, message):
        self.log = self._get_log()
        self.log.info(message)

    def debug(self, message):
        self.log = self._get_log()
        self.log.debug(message)

    def warning(self, message):
        self.log = self._get_log()
        self.log.warning(message)

    def error(self, message):
        self.log = self._get_log()
        self.log.error(message)



