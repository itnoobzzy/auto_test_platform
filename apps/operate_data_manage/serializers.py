#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: itnoobzzy
# @Date  : 2021/3/10
# @Desc  : 运营数据管理序列化文件
import time, datetime

from rest_framework import serializers

from .models import *


class AreaListSerializer(serializers.ModelSerializer):
    """产品落地省份列表"""
    class Meta:
        model = TTestOperateDataInfo
        fields = ('operate_desc', )

    def validate(self, attrs):
        search_prov_name = self.context['request'].data.get('search_prov_name', '')
        search_product_name = self.context['request'].data.get('search_product_name', '')

        product_info = TTestOperateDataInfo.objects.get_all_product_info(search_product_name, search_prov_name)

        product_list = TTestOperateDataInfo.objects.get_product_name_list()

        ret_info = {
            "product_info": product_info,
            "product_list": product_list,
        }

        attrs['list_info'] = ret_info
        attrs['total_count'] = 0
        return attrs


class ViewInfoSerializer(serializers.ModelSerializer):
    """运营数据视图信息"""
    class Meta:
        model = TTestOperateViewInfo
        fields = ('milepost_date', )

    def _get_opreate_param_value(self, operate_data):
        """获取测试能力信息"""
        data_info = {}
        data_info['test_case_count'] = 0
        data_info['whole_test_times'] = 0
        data_info['test_case_execute_times'] = 0
        data_info['api_call_times'] = 0
        data_info['business_landing_times'] = 0
        for data in operate_data:
            sub_index = data['operative_sub_index']
            if sub_index == '测试用例数':
                data_info['test_case_count'] += int(data['operate_data'])
            elif sub_index == '自动化测试次数':
                data_info['whole_test_times'] += int(data['operate_data'])
            elif sub_index == '测试用例执行次数':
                data_info['test_case_execute_times'] += int(data['operate_data'])
            elif sub_index == '接口能力调用次数':
                data_info['api_call_times'] += int(data['operate_data'])
                data_info['business_landing_times'] += 1

        return data_info

    def validate(self, attrs):
        product_name = self.context['request'].data.get('product_name', '')
        if not product_name:
            raise serializers.ValidationError('请传入展示产品线名称！')

        view_data = TTestOperateViewInfo.objects.exclude(milepost_date='').values().order_by('-flag_update_time')

        milestone_desc = []

        for data in view_data:
            milepost_desc = data['milepost_desc']
            milepost_date = data['milepost_date']
            add_sign = 0
            for desc in milestone_desc:
                if desc['date'] == milepost_date:
                    desc['milepost_desc'] += ', ' + milepost_desc
                    add_sign = 1
            if not add_sign:
                milestone_desc.append({"date": milepost_date, "milepost_desc": milepost_desc})

        new_milestone_desc = sorted(milestone_desc, key=lambda e: e.__getitem__('date'))

        cur_month = time.strftime('%Y-%m', time.localtime(time.time()))
        today = datetime.date.today()
        # 获取当前月的第一天
        first = today.replace(day=1)
        # 减一天，得到上个月的最后一天
        last_month = (first - datetime.timedelta(days=1)).strftime('%Y-%m')
        operate_data = TTestOperateDataInfo.objects.filter(operate_month=cur_month).values()
        last_operate_data = TTestOperateDataInfo.objects.filter(operate_month=last_month).values()

        data_info = self._get_opreate_param_value(operate_data)
        last_data_info = self._get_opreate_param_value(last_operate_data)

        ret_info = {
            "data_info": data_info,
            "last_data_info": last_data_info,
            "milestone_desc": new_milestone_desc,
        }

        attrs['list_info'] = ret_info
        attrs['total_count'] = 0
        return attrs


class AreaProvListSerializer(serializers.ModelSerializer):
    """运营数据省份参数信息视图集"""

    class Meta:
        model = TTestOperateDataInfo
        fields = ('operate_desc', )


    def validate(self, attrs):
        product_name = self.context['request'].data.get('product_name', '')
        if not product_name:
            raise serializers.ValidationError('请传入展示产品线名称！')

        param_list, prov_name = TTestOperateDataInfo.objects.get_area_prov_info(product_name)

        ret_info = {
            "param_list": param_list,
            "prov_name": prov_name,
        }

        attrs['list_info'] = ret_info
        attrs['total_count'] = 0
        return attrs


class OperateConfigListSerializer(serializers.ModelSerializer):
    """运营数据配置列表信息"""
    class Meta:
        model = TTestOperateDataInfo
        fields = ('operate_desc', )


    def validate(self, attrs):
        product_name = self.context['request'].data.get('product_name', '')
        if not product_name:
            raise serializers.ValidationError('请传入产品线名称！')

        prov_name = self.context['request'].data.get('prov_name', '')
        operate_month = self.context['request'].data.get('operate_month', '')
        operate_month = '%s-%s' % (operate_month[:4], operate_month[-2:]) if operate_month else operate_month
        operative_index = self.context['request'].data.get('operative_index', '')
        page = int(self.context['request'].data.get('page', ''))
        pageSize = int(self.context['request'].data.get('pageSize', ''))

        kwargs = {
            'product_name': product_name,
            'prov_name': prov_name,
            'operate_month': operate_month,
            'operative_index': operative_index
        }

        data_list, total_count = TTestOperateDataInfo.objects.get_operate_data_list_info(page, pageSize, **kwargs)

        attrs['list_info'] = data_list
        attrs['total_count'] = total_count
        return attrs


class OperateConfigInfoSerializer(serializers.ModelSerializer):
    """运营数据配置新增， 更新， 删除序列化类"""
    class Meta:
        model = TTestOperateDataInfo
        fields = "__all__"

    # def validate(self, attrs):
    #     product_name = self.context['request'].data.get('product_name', '')
    #     operative_index = self.context['request'].data.get('operative_index', '')
    #     operative_sub_index = self.context['request'].data.get('operative_sub_index', '')
    #     prov_name = self.context['request'].data.get('prov_name', '')
    #     show_flag = self.context['request'].data.get('show_flag', '')
    #     id = self.context['request'].data.get('id', '')
    #     operate_data = self.context['request'].data.get('operate_data', '')
    #     units = self.context['request'].data.get('units', '')
    #     target_value = self.context['request'].data.get('target_value', '')
    #
    #     return attrs

    def update(self, instance, validated_data):
        """根据模板id更新模板信息"""
        instance.operative_sub_index = validated_data['operative_sub_index']
        instance.operate_data = validated_data['operate_data']
        instance.units = validated_data['units']
        instance.target_value = validated_data['target_value']
        instance.save()

        operative_index = validated_data['operative_index']
        operative_sub_index = validated_data['operative_sub_index']
        prov_name = validated_data['prov_name']
        show_flag = validated_data['show_flag']

        # 是否展示
        TTestOperateDataInfo.objects.filter(
            operative_index=operative_index,
            operative_sub_index=operative_sub_index,
            prov_name=prov_name).update(show_flag=show_flag)

        return instance

    # def create(self, validated_data):
    #     """新增模板"""
    #     validated_data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #     existed = TCaseTemplateInfo.objects.create(**validated_data)
    #     return existed


