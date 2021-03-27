#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: itnoobzzy
# @Date  : 2021/3/10
# @Desc  : 全流程测试列化文件
import codecs
from django.core.paginator import Paginator
from rest_framework import serializers

from .models import *
from config_manage.models import TTestCaseInfo


class TestResultListSerializer(serializers.ModelSerializer):
    """测试结果序列化类"""
    class Meta:
        model = TTestRequireInfo
        fields = ('require_file_desc', )

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        require_name = self.context['request'].data.get('require_name', '')
        product_name = self.context['request'].data.get('product_name', '')
        if not product_name:
            raise serializers.ValidationError('请传入该用户所属产品线名称！')
        test_status = self.context['request'].data.get('result_type', '')
        kwargs = {
            'require_name': require_name,
            'test_status': test_status,
            'product_name': product_name
        }
        list_info, total_count = TTestRequireInfo.objects.get_test_result_info(page, pageSize, **kwargs)
        attrs['list_info'] = list_info
        attrs['total_count'] = total_count
        return attrs


class ResultDetailSerializer(serializers.ModelSerializer):
    """测试结果详情序列化类"""
    class Meta:
        model = TTestRequireInfo
        fields = ('require_file_desc', )

    total_count = 0
    test_pass = 0
    test_not_pass = 0

    def _get_instance_id(self, require_name):
        """根据测试名称查询实例id"""
        instance_id = 0
        ins_info = TTestInstanceInfo.objects.filter(offer_id=require_name).values('instance_id')
        for info in ins_info:
            instance_id = info['instance_id']
        return instance_id

    def _handle_read(self, file_path):
        """处理读取"""
        value = ''
        if file_path:
            value = codecs.open(file_path, encoding='gbk', errors='ignore').read()
        return value

    def _read_result_file(self, result_info, result_dict, point_type):
        """读取结果文件信息"""
        for result in result_info:
            file_type = result['file_type']
            file_path = result['file_path']
            if point_type == '单元测试':
                if file_type == 'expect_result':
                    result_dict['expect_result'] = '通过'
                elif file_type == 'real_result':
                    value = self._handle_read(file_path)
                    result_dict['real_result'] = value
                elif file_type == 'result_desc':
                    result_dict[file_type] = file_path
            else:
                if file_type != 'result_desc':
                    value = self._handle_read(file_path)
                    result_dict[file_type] = value
                else:
                    result_dict[file_type] = file_path

    def _get_task_info(self, instance_id, page, pageSize, result_type):
        """根据实例id和结果类型（通过，不通过，单元测试）获取任务信息"""
        task_id_info = TTestTaskInfo.objects.filter(instance_id=instance_id)

        task_id_list = [task.task_id for task in task_id_info]
        self.test_not_pass = len(
            TResultFileInfo.objects.filter(task_id__in=task_id_list, file_type='result_desc',
                                                      file_path='不通过'))
        self.test_pass = len(task_id_list) - self.test_not_pass

        if result_type:
            task_info = list(
                TResultFileInfo.objects.filter(task_id__in=task_id_list, file_path=result_type,
                                                          file_type='result_desc').values('task_id'))
        else:
            task_info = [{'task_id': task_id} for task_id in task_id_list]

        ptr = Paginator(task_info, pageSize)
        self.total_count = ptr.count
        cur_page = ptr.page(page)

        info = []
        for task in cur_page:
            task_id = task['task_id']
            case_id = ''
            test_info = TTestTaskInfo.objects.filter(task_id=task_id).values('case_id')
            for test in test_info:
                case_id = test['case_id']
            case_info = TTestCaseInfo.objects.filter(case_id=case_id).values()
            case_name = ''
            point_type = ''
            for case in case_info:
                case_name = case['case_name']
                point_type = case['point_type']

            result_info = TResultFileInfo.objects.filter(task_id=task['task_id']).values()
            result_dict = {"result_desc": "", "expect_result": "", "real_result": ""}
            # 读取文件获得预期结果和实际结果
            self._read_result_file(result_info, result_dict, point_type)

            info.append({'task_id': task_id, 'test_name': case_name, 'result_desc': result_dict['result_desc'],
                         'real_result': result_dict['real_result'], 'expect_result': result_dict['expect_result']})
        return info

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        require_name = self.context['request'].data.get('require_name')
        result_type = self.context['request'].data.get('result_type', '')
        if not require_name:
            raise serializers.ValidationError('请传入测试任务名称！')
        instance_id = self._get_instance_id(require_name)

        info = self._get_task_info(instance_id, page, pageSize, result_type)
        ret_info = {
            'ret_info': info,
            'test_pass': self.test_pass,
            'test_not_pass': self.test_not_pass
        }
        attrs['list_info'] = ret_info
        attrs['total_count'] = self.total_count
        return attrs







