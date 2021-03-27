#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: itnoobzzy
# @Date  : 2021/3/10
# @Desc  : 用户, 角色信息序列化文件

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class MenuInfoSerializer(serializers.ModelSerializer):
    """多级菜单信息序列化类"""

    def _get_menu_info(self):
        menu_info = MenuInfo.objects.filter().values()
        menu_info_list = list()

        self._get_menu1(menu_info, menu_info_list)
        self._get_menu2(menu_info, menu_info_list)
        self._get_menu3(menu_info, menu_info_list)

        return menu_info_list

    def _get_menu1(self, menu_info, menu_info_list):
        for menu in menu_info:
            menu_id = menu['menu_id']
            menu_name = menu['menu_name']
            parent_menu_id = menu['parent_menu_id']
            if parent_menu_id == '0':
                menu_info_list.append({'menu_id': menu_id, "menu_name": menu_name, "children_info": list()})

    def _get_menu2(self, menu_info, menu_info_list):
        for menu in menu_info:
            parent_menu_id = menu['parent_menu_id']
            menu_id = menu['menu_id']
            menu_name = menu['menu_name']
            menu_url = menu['menu_url']

            if parent_menu_id != '0':
                for parent in menu_info_list:
                    if parent['menu_id'] == parent_menu_id:
                        parent['children_info'].append(
                            {"menu_id": menu_id,
                             "menu_name": menu_name,
                             "menu_url": menu_url,
                             "children_info": list()})

    def _get_menu3(self, menu_info, menu_info_list):
        for menu in menu_info:
            parent_menu_id = menu['parent_menu_id']
            menu_id = menu['menu_id']
            menu_name = menu['menu_name']
            menu_url = menu['menu_url']
            for parent in menu_info_list:
                children_info = parent['children_info']
                for children in children_info:
                    if parent_menu_id == children['menu_id']:
                        children['children_info'].append(
                            {"menu_id": menu_id,
                             "menu_name": menu_name,
                             "menu_url": menu_url})

    def validate(self, attrs):
        menu_info_list = self._get_menu_info()
        attrs['menu_info_list'] = menu_info_list
        return attrs

    class Meta:
        model = MenuInfo
        fields = ('menu_url',)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAuthorityInfo
        fields = "__all__"


class RoleAuthorityInfoSerializer(serializers.ModelSerializer):
    """角色对应权限信息序列化类"""

    role_id = serializers.CharField(label="角色id", help_text="角色名", required=False, allow_blank=True)

    def _get_role_auth_info(self):
        """获取角色信息和菜单权限信息"""
        role_id = self.context['request'].data.get('role_id', None)
        if role_id:
            role_id_list = RoleAuthorityInfo.objects.filter(role_id=role_id).values('role_id').distinct()
        else:
            role_id_list = RoleAuthorityInfo.objects.filter().values('role_id').distinct()
        ret_list = []
        for role_id in role_id_list:
            role_info_dict = {}
            role_id = role_id['role_id']
            role_name, role_desc = RoleAuthorityInfo.objects.get_role_info(role_id)
            menu_name_list = RoleAuthorityInfo.objects.get_menu_info(role_id)[0]
            menu_id_list = RoleAuthorityInfo.objects.get_menu_info(role_id)[1]

            role_info_dict['role_id'] = role_id
            role_info_dict['role_name'] = role_name
            role_info_dict['role_desc'] = role_desc
            role_info_dict['menu_name_list'] = menu_name_list
            role_info_dict['menu_id_list'] = menu_id_list

            ret_list.append(role_info_dict)
        return ret_list

    def validate(self, attrs):
        ret_list = self._get_role_auth_info()
        attrs['role_list'] = ret_list
        return attrs

    class Meta:
        model = RoleAuthorityInfo
        fields = ('role_id',)


class RoleUpdateInfoSerializer(serializers.ModelSerializer):
    """更新角色信息序列化类"""
    # id = serializers.CharField(label="id", help_text="id", required=True, allow_blank=False)
    role_id = serializers.CharField(label="角色id", help_text="角id", required=True, allow_blank=False)
    role_name = serializers.CharField(label="角色名称", help_text="角色名称", required=True, allow_blank=False)
    role_desc = serializers.CharField(label="角色描述", help_text="角色描述", required=True, allow_blank=False)

    def validate(self, attrs):
        RoleAuthorityInfo.objects.filter(role_id=attrs['role_id']).delete()
        menu_id_list = self.context['request'].data.get('menu_id_list', [])
        if not menu_id_list:
            RoleAuthorityInfo(**attrs).save()
        for menu_id in menu_id_list:
            role_info = RoleAuthorityInfo()
            role_info.role_id = attrs['role_id']
            role_info.role_name = attrs['role_name']
            role_info.role_desc = attrs['role_desc']
            role_info.menu_id = menu_id
            role_info.save()

        return attrs

    class Meta:
        model = RoleAuthorityInfo
        fields = ('role_id', 'role_name', 'role_desc')


class RoleDeleteSerializer(serializers.ModelSerializer):
    """删除角色信息序列化类"""
    role_id = serializers.CharField(label="角色id", help_text="角色id", required=True, allow_blank=False)

    def validate(self, attrs):
        RoleAuthorityInfo.objects.filter(role_id=attrs['role_id']).delete()
        return attrs

    class Meta:
        model = RoleAuthorityInfo
        fields = ('role_id', )


class LoginSerializer(serializers.ModelSerializer):
    """登录序列化类：返回菜单信息,用户信息,token"""
    user_name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False)

    user_password = serializers.CharField(
        label="密码",
        required=True,
        allow_blank=False,
        style={'input_type': 'password'},
        help_text="密码",
        write_only=True
    )


    def validate(self, attrs):
        """验证用户名和密码是否正确"""
        user_info = UserInfo.objects.get_user_info(attrs['user_name'], attrs['user_password'])
        password = user_info.get('password', 1)
        # 前端传递过来加密后的密码
        new_password = user_info.get('new_password', 2)

        if new_password != password:
            raise serializers.ValidationError("用户名或密码错误！")

        attrs['user_role_id'] = user_info.get('user_role_id')
        attrs['user_id'] = user_info.get('user_id')
        attrs['product_name'] = user_info.get('product_name')
        attrs['token'] = user_info.get('token')
        attrs['cur_branch'] = user_info.get('current_branch')
        # 获取用户菜单权限
        attrs['menu_name_list'] = RoleAuthorityInfo.objects.get_menu_info(user_info.get('user_role_id'))[0]

        return attrs

    class Meta:
        model = UserInfo
        fields = ("user_name", "user_password")


class UserUpdateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False)

    user_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="密码",
        label="密码",
        required=True, allow_blank=False
    )

    current_branch = serializers.CharField(label="当前分支", help_text="当前分支", required=False, allow_blank=False)
    product_name = serializers.CharField(label="分支产品线名称", help_text="分支产品线名称", required=False, allow_blank=False)

    class Meta:
        model = UserInfo
        fields = "__all__"


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类，
    """
    user_name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserInfo.objects.all(), message="用户已经存在")])

    user_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="密码",
        label="密码"
    )

    role_id = serializers.CharField(label="角色id", help_text="角色id", required=False, allow_blank=True)
    current_branch = serializers.CharField(label="当前分支", help_text="当前分支", required=False, allow_blank=True)
    product_name = serializers.CharField(label="分支产品线名称", help_text="分支产品线名称", required=False, allow_blank=True)

    def create(self, validated_data):
        """
        触发信号量将密码加密后保存至数据库
        :param validated_data:
        :return:
        """
        instance = UserInfo.objects.create(**validated_data)
        return instance

    class Meta:
        model = UserInfo
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = UserInfo
        fields = ("token",)

    def validate(self, attrs):
        page = self.context['request'].data.get('page', 1)
        page_size = self.context['request'].data.get('pageSize', 10)
        user_name = self.context['request'].data.get('user_name', None)
        user_id = self.context['request'].data.get('user_id', None)
        user_role_id = self.context['request'].data.get('user_role_id', None)
        user_list, total_count = UserInfo.objects.get_pagination_info(page, page_size, user_name)
        user_role_info = RoleAuthorityInfo.objects.get_role_infos()
        product_name = UserInfo.objects.get_product_name(user_id)

        attrs['user_role_info'] = user_role_info
        attrs['user_list'] = user_list
        attrs['total_count'] = total_count
        attrs['product_name'] = product_name
        attrs['role_name'] = RoleAuthorityInfo.objects.get_role_name(user_role_id)
        return attrs


class UserDeleteSerializer(serializers.ModelSerializer):
    """
    用户删除序列化类
    """
    id = serializers.CharField(label="用户id", help_text="用户id",
                                     required=True, allow_blank=False)

    class Meta:
        model = UserInfo
        fields = ("id",)

    def validate(self, attrs):
        id = self.context['request'].data.get('id', None)
        if not id:
            raise serializers.ValidationError("请传入用户id！")
        UserInfo.objects.filter(id=id).delete()
        return attrs






