#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: itnoobzzy
# @Date  : 2021/3/10
# @Desc  : 配置管理序列化文件

import time

from rest_framework import serializers

from .models import *


class TemplateInfoSerializer(serializers.ModelSerializer):
    """模板表序列化类"""
    class Meta:
        model = TCaseTemplateInfo
        fields = ('module_name', 'module_type', 'regular_type', 'regular_type_flag', 'status', 'eff_time', 'exp_time')

    def validate(self, attrs):
        user_name = self.context['request'].data.get('user_name', '')
        # TODO：模板类型暂定为当前登录用户所属产品线名称
        module_type = self.context['request'].data.get('module_type', '')
        if not user_name:
            raise serializers.ValidationError('请传入用户名称！')
        if not module_type:
            raise serializers.ValidationError('请传入用户所属产品线名称！')
        attrs['author'] = user_name
        attrs['module_type'] = module_type
        return attrs

    def update(self, instance, validated_data):
        """根据模板id更新模板信息"""
        instance.module_type = validated_data['module_type']
        instance.module_name = validated_data['module_name']
        instance.save()
        return instance

    def create(self, validated_data):
        """新增模板"""
        validated_data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        existed = TCaseTemplateInfo.objects.create(**validated_data)
        return existed


class TemplateListSerializer(serializers.ModelSerializer):
    """模板表序列化类"""

    class Meta:
        model = TCaseTemplateInfo
        fields = ('module_name', )

    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        module_name = self.context['request'].data.get('module_name', '')
        product_name = self.context['request'].data.get('product_name', '')
        kwargs = {
            'module_name': module_name,
            'product_name': product_name
        }
        list_info, total_count = TCaseTemplateInfo.objects.get_template_info(page, pageSize, **kwargs)
        attrs['list_info'] = list_info
        attrs['total_count'] = total_count
        return attrs


class CaseListSerializer(serializers.ModelSerializer):
    """用例列表序列化类"""
    case_id = serializers.CharField(label="用例id", help_text="用例id", required=False, allow_blank=True)
    class Meta:
        model = TTestCaseInfo
        fields = "__all__"

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        template_id = self.context['request'].data.get('template_id', '')
        product_name = self.context['request'].data.get('test_action', '')
        case_name = self.context['request'].data.get('case_name', '')
        kwargs = {
            'template_id': template_id,
            'case_name': case_name,
            'product_name': product_name
        }
        # 如果传递模板id，是查询模板绑定用例列表，如果没传，就是查询所有用例
        if template_id:
            list_info, total_count = TTestCaseInfo.objects.get_bind_case_info(page, pageSize, **kwargs)
        else:
            list_info, total_count = TTestCaseInfo.objects.get_all_case_info(page, pageSize, **kwargs)
        attrs['list_info'] = list_info
        attrs['total_count'] = total_count
        return attrs


class CaseInfoSerializer(serializers.ModelSerializer):
    """用例列表序列化类"""
    class Meta:
        model = TTestCaseInfo
        fields = "__all__"

    def update(self, instance, validated_data):
        """根据用例id更新用例信息"""
        instance.case_name = validated_data['case_name']
        instance.test_process = validated_data['test_process']
        instance.preset_data = validated_data['preset_data']
        instance.input_data = validated_data['input_data']
        instance.test_action = validated_data['test_action']
        instance.save()
        return instance

    def validate(self, attrs):
        # 新增或编辑用例必须传对应的模板id
        test_action = self.context['request'].data.get('test_action', '')
        author = self.context['request'].data.get('author', '')

        if not test_action:
            raise serializers.ValidationError("更新或新增用例时需传入用户所属产品线名称！")

        if not author:
            raise serializers.ValidationError("更新或新增用例时需传入用户名称！")

        return attrs

    def create(self, validated_data):
        """新增用例"""
        validated_data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        existed = TTestCaseInfo.objects.create(**validated_data)
        return existed


class TemplateBindCaseInfoSerializer(serializers.ModelSerializer):
    """
    查询模板已绑定用例(不需要分页)和未绑定用例(需要分页)序列化类
    """
    class Meta:
        model = TTestCaseInfo
        fields = "__all__"

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        case_name = self.context['request'].data.get('case_name', '')
        case_template_id = self.context['request'].data.get('case_template_id', '')
        product_name = self.context['request'].data.get('product_name', '')
        if not case_template_id:
            raise serializers.ValidationError('请传入模板id!')
        if not product_name:
            raise serializers.ValidationError('请传入产品名称！')

        # 已绑定用例信息
        bind_case_ids = TemplateBindCaseInfo.objects.get_bind_case_id(case_template_id)
        bind_case_info_qs = TTestCaseInfo.objects.filter(case_id__in=bind_case_ids).values('case_id', 'case_name')
        bind_case_info = [case_info for case_info in bind_case_info_qs]

        # 未绑定用例信息
        kwargs = {
            'case_name': case_name,
            'case_template_id': case_template_id,
            'product_name': product_name,
            'bind_id_list': bind_case_ids
        }
        unbind_case_info, total_count = TTestCaseInfo.objects.get_unbind_case_info(page, pageSize, **kwargs)

        ret_info = {
            "bind_info": bind_case_info,
            "unbind_info": unbind_case_info
        }

        attrs['list_info'] = ret_info
        attrs['total_count'] = total_count

        return attrs


class TemplateUnBindCaseInfoSerializer(serializers.ModelSerializer):
    """
    查询未绑定用例信息，需要传入已绑定用例id列表
    """
    class Meta:
        model = TTestCaseInfo
        fields = "__all__"

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        pageSize = self.context['request'].data.get('pageSize', 10)
        case_name = self.context['request'].data.get('case_name', '')
        bind_id_list = self.context['request'].data.get('bind_id_list', [])
        product_name = self.context['request'].data.get('product_name', '')
        case_template_id = self.context['request'].data.get('case_template_id', '')

        if not product_name:
            raise serializers.ValidationError('请传入产品名称！')

        # 未绑定用例信息
        kwargs = {
            'case_name': case_name,
            'product_name': product_name,
            'bind_id_list': bind_id_list,
            'case_template_id': case_template_id
        }
        unbind_case_info, total_count = TTestCaseInfo.objects.get_unbind_case_info(page, pageSize, **kwargs)

        ret_info = {
            "unbind_info": unbind_case_info
        }

        attrs['list_info'] = ret_info
        attrs['total_count'] = total_count

        return attrs





