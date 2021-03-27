#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : deal_token.py
# @Author: itnoobzzy
# @Date  : 2021/3/11
# @Desc  : 生成token

import jwt
import datetime

from auto_test_platform.settings import JWT_EXPIRE, SECRET_KEY, JWT_ISS

class BaseTokenInfo:
    """token所需基本信息"""
    algorithm = 'HS256'
    secret = SECRET_KEY
    iss = JWT_ISS
    exp = JWT_EXPIRE
    iat = datetime.datetime.utcnow() # 生成token默认从当前时间开始
        

class DealToken(BaseTokenInfo):
    """
    token处理
    """
    def __init__(self, payload=dict):
        """
        :param payload:  需要加密的对象
        """
        self.payload = payload

        self.dic = {
            'exp': self.iat + datetime.timedelta(seconds=self.exp),  # 过期时间
            'iat': self.iat,  # 开始时间
            'iss': self.iss,  # 签名
            'data': payload,
        }

    def get_token(self):
        """
        生成token
        :return:
        """
        try:
            token = jwt.encode(self.dic, self.secret, algorithm=self.algorithm)
        except Exception as e:
            print(e)
        else:
            return token

    def decode_token(self, token: str):
        """
        解码token获取数据
        :param token: token
        :return:
        """
        try:
            data = jwt.decode(token, self.secret, issuer=self.iss, algorithms=self.algorithm)  # 解密，校验签名
        except Exception as e:
            return False
        else:
            return data