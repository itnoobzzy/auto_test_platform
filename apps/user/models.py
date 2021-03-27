import hashlib

from django.db import models
from django.core.paginator import Paginator
from django.contrib.auth.models import AbstractUser

class RoleAuthorityInfoQs(models.query.QuerySet):
    """角色权限信息表查询集"""

    def get_menu_info(self, role_id):
        """获取对应角色id的菜单信息"""
        menu_name_list = []
        menu_id_list = []
        menu_data = self.filter(role_id=role_id).values()
        for menu in menu_data:
            menu_name_info = MenuInfo.objects.filter(menu_id=menu['menu_id']).values()
            for menu_name in menu_name_info:
                menu_name_list.append(menu_name['menu_name'])
                menu_id_list.append(menu_name['menu_id'])
        return menu_name_list, menu_id_list

    def get_role_infos(self):
        """获取所有角色信息"""
        return self.filter().values('role_name', 'role_id').distinct()

    def get_role_info(self, role_id):
        """根据role_id， 获取角色信息"""
        role_info = self.filter(role_id=role_id).values('role_name', 'role_desc')
        role_name = ''
        role_desc = ''
        for data in role_info:
            role_name = data['role_name'] or ''
            role_desc = data['role_desc'] or ''
        return role_name, role_desc

    def get_role_name(self, role_id):
        """获取对应角色id的角色名称"""
        return self.filter(role_id=role_id).values('role_name').distinct()


class UserInfoQs(models.query.QuerySet):
    """用户信息查询集"""

    def get_md5(self, encode_str: str, encoding='utf-8'):
        """
        MD5加密字符串
        :param encode_str: 需要加密的字符串
        :param encoding: 默认为utf-8
        :return:
        """
        hl = hashlib.md5()
        hl.update(encode_str.encode(encoding=encoding))
        return hl.hexdigest()

    def create_admin(self):
        """第一次登录默认创建admin用户"""
        first_data = self.filter(user_name='admin').values()
        if not first_data:
            user_password = 'admin'
            # md5加密
            user_password = self.get_md5(user_password)
            self.create(
                user_name='admin',
                user_password=user_password,
                role_id=1,
                product_name='自动化测试平台'
            )

    def get_user_info(self, user_name, user_password):
        """查询对应用户名用户信息"""
        user_info = {}
        user_data = self.filter(user_name=user_name).values()
        for data in user_data:
            md5_password = self.get_md5(user_password)
            user_info['user_id'] = data['id']
            user_info['current_branch'] = data['current_branch']
            user_info['password'] = data['user_password']
            user_info['user_role_id'] = data['role_id']
            user_info['product_name'] = data['product_name']
            user_info['new_password'] = md5_password
            user_info['token'] = data['token']
        return user_info

    def get_product_name(self, user_id):
        """根据用户id查询对应产品名称"""
        try:
            return self.filter(id=user_id).values('product_name')[0].get('product_name')
        except IndexError:
            return ''

    def get_all_user_info(self, user_name=None):
        """如果传递用户名查询所有该用户信息，否则查询所有用户信息"""
        if user_name:
            return self.filter(user_name__contains=user_name)
        return self.all()

    def get_pagination_info(self, page, page_size, user_name=None):
        """
        查询分页后的用户列表信息
        :param page: 当前页数
        :param page_size: 每页数量
        :param user_name: 用户名
        :return:
        """
        user_infos = self.get_all_user_info(user_name)
        ptr = Paginator(user_infos, page_size)
        total_count = ptr.count
        cur_page_info = ptr.page(page)

        user_list = []
        for user in cur_page_info:
            user_dict = {}
            user_dict['id'] = user.id
            user_dict['user_name'] = user.user_name
            user_dict['user_password'] = user.user_password
            user_dict['role_id'] = user.role_id
            user_dict['product_name'] = user.product_name
            role_name = RoleAuthorityInfo.objects.filter(role_id=user.role_id).values('role_name').distinct()
            if role_name:
                user_dict['role_name'] = [_['role_name'] for _ in role_name][0]
            user_list.append(user_dict)

        return user_list, total_count

    def _query_exist_info(self, user_id):
        """根据用户id查询已存在的用户信息"""
        try:
            exist_info = self.filter(id=user_id).values('user_name', 'user_password',
                                                        'role_id', 'product_name')[0]
        except IndexError:
            exist_info = {}
        return exist_info

    def _judge_exist(self, user_id, update_key, update_value):
        """
        判断更新数据是否不变
        :param user_id: 用户id
        :param update_key: 需要更新的字段名
        :param update_value: 需要更新的值
        :return: Boolean
        """
        exist_info = self._query_exist_info(user_id).get(update_key)
        return exist_info != update_value

    def update_user_info(self, user_id: str, **kwargs: dict):
        """
        更新用户信息，如果信息不变不执行更新
        :param user_id: 用户id
        :param kwargs: 需要更新的命名关键字
        :return:
        """
        for update_key, update_value in kwargs.items():
            if self._judge_exist(user_id, update_key, update_value):
                if update_key == 'user_password':
                    update_password = self.get_md5(update_value)
                    self.filter(id=user_id).update(user_password=update_password)
                else:
                    self.filter(id=user_id).update(**{update_key: update_value})


class MenuInfo(models.Model):
    """菜单信息表"""
    MENU_LEVEL = (
        (1, '一级菜单'),
        (2, '二级菜单'),
        (3, '三级菜单'),
    )
    menu_id = models.CharField(max_length=10, default='', verbose_name='菜单目录id', help_text='菜单目录id')
    menu_level = models.IntegerField(choices=MENU_LEVEL, verbose_name='菜单目录级别', help_text='菜单目录级别')
    menu_name = models.CharField(max_length=10, default='', verbose_name='菜单名称', help_text='菜单名称')
    parent_menu_id = models.CharField(max_length=10, default='', verbose_name='菜单父目录id', help_text='菜单父目录id')
    menu_url = models.CharField(max_length=256, default='', verbose_name='菜单路由', help_text='菜单路由')

    class Meta:
        verbose_name = '菜单信息'
        verbose_name_plural = verbose_name
        db_table = 't_test_menu_info'


class RoleAuthorityInfo(models.Model):
    """角色权限信息表"""
    role_id = models.CharField(max_length=10, default='', verbose_name='角色id', help_text='角色id')
    role_name = models.CharField(max_length=20, default='', verbose_name='角色名称', help_text='角色名称')
    role_desc = models.CharField(max_length=200, default='', verbose_name='角色描述', help_text='角色描述')
    menu_id = models.CharField(max_length=10, default='', verbose_name='菜单目录id', help_text='菜单目录id')
    objects = RoleAuthorityInfoQs.as_manager()

    class Meta:
        verbose_name = "角色权限信息表"
        verbose_name_plural = verbose_name
        db_table = 't_test_role_authority_info'


class UserInfo(models.Model):
    """用户信息模型类"""
    user_name = models.CharField(max_length=30, null=False, blank=False, verbose_name="用户名")
    user_password = models.CharField(max_length=256, verbose_name="密码", null=False, blank=False)
    role_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='角色id', help_text='角色id')
    current_branch = models.CharField(max_length=128, blank=True, null=True, verbose_name="用户所属分支")
    product_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="分支产品线名称")
    token = models.CharField(max_length=256, blank=True, null=True, verbose_name='登录token', help_text='登录token')
    objects = UserInfoQs.as_manager()

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"
        db_table = 't_test_user_info'

    def __str__(self):
        return self.role_id

# class User