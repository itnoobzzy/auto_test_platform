"""auto_test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.views.generic.base import TemplateView

from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import (
    UserViewSet,
    RoleViewSet
)
from config_manage.views import (
    TemplateCaseViewSet
)
from whole_process_test.views import (
    TestResultViewSet,
    WholeProcessTestViewSet
)
from operate_data_manage.views import (
    OperateDataViewSet,
    OperateDataConfigViewSet
)


router = routers.DefaultRouter()

# 新增，修改用户信息
router.register(r'user', UserViewSet, basename="user")
# 角色
router.register(r'role', RoleViewSet, basename="role")

# 配置管理
router.register(r'config_manage', TemplateCaseViewSet, basename="config_manage")

# 测试结果管理
router.register(r'test_result_manage', TestResultViewSet, basename="test_result_manage")

# 全流程测试管理
router.register(r'whole_process_test', WholeProcessTestViewSet, basename="whole_process_test")

# 运营数据展示
router.register(r'operate_data_show', OperateDataViewSet, basename="operate_data_show")

# 运营数据配置管理
router.register(r'operate_data_config', OperateDataConfigViewSet, basename="operate_data_config")

urlpatterns = [
    path('',TemplateView.as_view(template_name='index.html')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='自动化测试平台')),
    # simple jwt 认证接口
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
