
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from .serializers import *
from .models import *
from operate_data_manage.models import TTestOperateDataInfo
from utils.deal_token import DealToken


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    list:
        用户列表数据
    update_user_info：
        更新用户信息
    create:
        创建新增用户
    login：
        用户登录
    query_user_menu_info：
        查询用户菜单信息
    """
    serializer_class = UserListSerializer
    queryset = UserInfo.objects.all()
    # JWT或者session两种权限认证方式
    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_permissions(self):
        """根据请求动作，判断是否需要权限认证"""
        if self.action == "retrieve":
            # return [permissions.IsAuthenticated]
            # TODO:暂时不权限认证
            return []
        elif self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'update_user_info':
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserRegSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'query_user_menu_info':
            return UserListSerializer
        elif self.action == 'query_menu_info':
            return MenuInfoSerializer
        elif self.action == 'del_user_info':
            return UserDeleteSerializer
        else:
            return UserListSerializer

    def create(self, request, *args, **kwargs):
        """
        增加用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:用户名和token
        """
        serializer = self.get_serializer(data=request.data)
        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            user = self.perform_create(serializer)
            ret_dict["info"]["token"] = self._get_token(user.user_name)
            ret_dict["info"]["user_name"] = user.user_name
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def _update_user_info(self, serializer, user_id):
        """更新用户信息"""
        user_name = serializer.validated_data['user_name']
        user_password = serializer.validated_data['user_password']
        user_role_id = serializer.validated_data['role_id']
        product_name = serializer.validated_data['product_name']
        if user_name:
            kwargs = {"user_name": user_name}
            self._update(user_id, **kwargs)
        if user_password:
            kwargs = {"user_password": user_password}
            self._update(user_id, **kwargs)
        if user_role_id:
            kwargs = {"role_id": user_role_id}
            self._update(user_id, **kwargs)
        if product_name:
            kwargs = {"product_name": product_name}
            self._update(user_id, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=UserUpdateSerializer)
    def update_user_info(self, request, *args, **kwargs):
        """更新用户信息"""
        serializer = self.get_serializer(data=request.data)
        user_id = request.data.get('user_id')
        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            self._update_user_info(serializer, user_id)

            ret_dict['info'] = '更新成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=UserDeleteSerializer)
    def del_user_info(self, request, *args, **kwargs):
        """删除用户信息"""
        serializer = self.get_serializer(data=request.data)
        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = '删除成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        ret_dict = {
            'status': 0,
            'info': {}
        }

        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = serializer.validated_data
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=UserListSerializer)
    def query_user_menu_info(self, request, *args, **kwargs):
        """获取用户列表数据"""

        serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        # 获取产品名称列表和产品信息
        product_name = request.data.get('product_name', '')
        prov_name = request.data.get('prov_name', '')
        product_info = TTestOperateDataInfo.objects.get_all_product_info(product_name, prov_name)
        product_name_list = TTestOperateDataInfo.objects.get_product_name_list()

        if serializer.is_valid(raise_exception=False):
            ret_dict['info']['user_list'] = serializer.validated_data['user_list']
            ret_dict['info']['user_role_info'] = serializer.validated_data['user_role_info']
            ret_dict['info']['total_count'] = serializer.validated_data['total_count']
            ret_dict['info']['role_name'] = serializer.validated_data['role_name']
            ret_dict['info']['product_name'] = serializer.validated_data['product_name']
            ret_dict['info']['product_info'] = product_info
            ret_dict['info']['product_list'] = product_name_list
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=MenuInfoSerializer)
    def query_menu_info(self, request, *args, **kwargs):
        """查询多级菜单树信息"""
        serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = serializer.validated_data['menu_info_list']
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)

    def _get_token(self, user_name):
        """生成token"""
        payload = {
            "user_name": user_name
        }
        deal_token = DealToken(payload)
        return deal_token.get_token()

    def _update(self, user_id, **kwargs):
        UserInfo.objects.update_user_info(user_id, **kwargs)


class RoleViewSet(viewsets.ModelViewSet):
    """
    query_role_authority:
        查询角色权限信息
    """
    queryset = RoleAuthorityInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'query_role_authority':
            return RoleAuthorityInfoSerializer
        elif self.action == 'create':
            return UserRegSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'query_user_menu_info':
            return UserListSerializer
        elif self.action == 'update_role_authority':
            return RoleUpdateInfoSerializer
        elif self.action == 'delete_role_authority':
            return RoleDeleteSerializer
        else:
            return RoleSerializer

    @action(detail=False, methods=['post'], serializer_class=RoleAuthorityInfoSerializer)
    def query_role_authority(self, request, *args, **kwargs):
        """获取角色列表数据"""
        serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        # 获取产品名称列表和产品信息

        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = serializer.validated_data['role_list']
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=RoleUpdateInfoSerializer)
    def update_role_authority(self, request, *args, **kwargs):
        """获取角色列表数据"""
        serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        # 获取产品名称列表和产品信息

        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = '更新成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)

    @action(detail=False, methods=['post'], serializer_class=RoleDeleteSerializer)
    def delete_role_authority(self, request, *args, **kwargs):
        """删除角色列表数据"""
        serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }

        if serializer.is_valid(raise_exception=False):
            ret_dict['info'] = '删除成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400
        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_200_OK, headers=headers)