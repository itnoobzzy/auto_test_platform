from django.db import models
from django.core.paginator import Paginator

class template_bind_case_info_qs(models.query.QuerySet):
    """模板绑定用例桥表查询集"""

    def get_bind_case_id(self, case_template_id):
        """返回绑定用例id列表"""
        case_id_qs = self.filter(case_template_id=case_template_id).values('case_id')
        return [_['case_id'] for _ in case_id_qs if case_id_qs.exists()]

    def get_bind_case_info(self, case_template_id):
        """返回模板下绑定的用例信息"""
        bind_ids = self.get_bind_case_id(case_template_id)
        case_info_list = []
        for case_id in bind_ids:
            case_info = TTestCaseInfo.objects.filter(case_id=case_id).values()

            for info in case_info:
                case_name = info['case_name']
                preset_data = info['preset_data']
                input_data = info['input_data']
                case_num = info['test_action']
                case_type = info['case_type']
                case_info_list.append({
                    'case_name': case_name,
                    'case_type': case_type,
                    'preset_data': preset_data,
                    'input_data': input_data,
                    'case_num': case_num
                })
        return case_info_list

    def add_bind_case_info(self, bind_case_list, case_template_id):
        """
        绑定新的用例：先删除对应模板下旧的用例id，再添加新的绑定的用例id
        :param bind_case_list: 新的绑定用例id
        :param case_template_id: 对应的模板id
        :return:
        """

        TemplateBindCaseInfo.objects.filter(case_template_id=case_template_id).exclude(
            case_id__in=bind_case_list).delete()

        for bind_id in bind_case_list:
            bind_info = self.filter(case_template_id=case_template_id, case_id=bind_id).values()
            if not bind_info:
                info = TemplateBindCaseInfo()
                info.case_template_id = case_template_id
                info.case_id = bind_id
                info.save()

class TemplateBindCaseInfo(models.Model):
    # 测试用例模板绑定用例桥表

    case_template_id = models.IntegerField(null=True, blank=True, verbose_name="测试模板id", help_text="测试模板id")
    case_id = models.IntegerField(null=True, blank=True, verbose_name="测试用例id", help_text="测试用例id")
    objects = template_bind_case_info_qs.as_manager()

    class Meta:
        verbose_name = "测试用例绑定模板桥表"
        verbose_name_plural = verbose_name
        db_table = 't_template_bind_case_info'

class TTestPointInfo(models.Model):
    class Meta:
        verbose_name = "测试点表"
        verbose_name_plural = verbose_name
        db_table = "t_test_point_info"
    point_id = models.AutoField(primary_key=True)
    point_code = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点编码", help_text="测试点编码")
    point_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点类型", help_text="测试点类型")
    point_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点名称", help_text="测试点名称")
    point_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点描述", help_text="测试点描述")
    point_regular = models.CharField(max_length=255, null=True, blank=True)
    expect_result = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点预期结果", help_text="测试点预期结果")

class TCaseBindPointInfo(models.Model):
    class Meta:
        verbose_name = "测试用例绑定测试点桥表"
        verbose_name_plural = verbose_name
        db_table = "t_case_bind_point_info"
    case_id = models.IntegerField(null=True, blank=True, verbose_name="测试用例id", help_text="测试用例id")
    point_id = models.IntegerField(null=True, blank=True, verbose_name="测试点id", help_text="测试点id")


class t_test_case_info_qs(models.query.QuerySet):
    """测试用例查询集"""

    def get_all_case_info(self, page, pageSize, **kwargs):
        """查询用户所属产品线下所有用例"""
        case_name = kwargs.get('case_name', '')
        product_name = kwargs.get('product_name', '')

        case_info_list = self.filter(test_action=product_name, case_name__contains=case_name)

        ptr = Paginator(case_info_list, pageSize)
        total_count = ptr.count
        cases = ptr.page(page)

        ret_list = [{"case_id": case.case_id,
                     "case_name": case.case_name,
                     "test_process": case.test_process,
                     "test_action": case.test_action,
                     "preset_data": case.preset_data,
                     "input_data": case.input_data,
                     "create_time": case.create_time,
                     "author": case.author} for case in cases]
        return ret_list, total_count

    def get_bind_case_info(self, page, pageSize, **kwargs):
        """
        查询对应模板下已绑定用例信息(分页)
        """
        case_name = kwargs.get('case_name', '')
        template_id = kwargs.get('template_id', 0)

        # 查询对应模板下的用例
        if template_id:
            case_id_list = TemplateBindCaseInfo.objects.get_bind_case_id(template_id)
            case_info_list = self.filter(case_id__in=case_id_list, case_name__contains=case_name).order_by('-case_id')
        else:
            raise Exception('请传入模板id!')
        ptr = Paginator(case_info_list, pageSize)
        total_count = ptr.count
        cases = ptr.page(page)

        ret_list = [{"case_id": case.case_id,
                     "case_name": case.case_name,
                     "test_process": case.test_process,
                     "case_type": case.case_type,
                     "test_action": case.test_action,
                     "point_type": case.point_type,
                     "preset_data": case.preset_data,
                     "input_data": case.input_data,
                     "eff_time": case.eff_time,
                     "exp_time": case.exp_time,
                     "create_time": case.create_time,
                     "author": case.author} for case in cases]
        return ret_list, total_count

    def get_unbind_case_info(self, page, pageSize, **kwargs):
        """查询对应模板下未绑定用例信息"""
        case_name = kwargs.get('case_name', '')
        case_template_id = kwargs.get('case_template_id', '')
        product_name = kwargs.get('product_name', '')
        bind_id_list = kwargs.get('bind_id_list', '')

        if case_template_id:
            unbind_case_info_qs = TTestCaseInfo.objects.filter(case_name__contains=case_name, test_action=product_name).exclude(case_id__in=bind_id_list).order_by('-case_id')
            ptr = Paginator(unbind_case_info_qs, pageSize)
            total_count = ptr.count
            cur_page_info = ptr.page(page)
            unbind_case_info = [{"case_id": case.case_id,
                           "case_name": case.case_name} for case in cur_page_info]

            return unbind_case_info, total_count
        else:
            return [], 0

class TTestCaseInfo(models.Model):
    """测试用例信息表"""
    class Meta:
        verbose_name = "测试用例表"
        verbose_name_plural = verbose_name
        db_table = "t_test_case_info"

    case_id = models.AutoField(primary_key=True, verbose_name="用例id")
    case_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="用例名称", help_text="用例名称")
    case_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="用例类型", help_text="用例类型")
    test_process = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试流程", help_text="测试流程")
    preset_data = models.CharField(max_length=255, null=True, blank=True, verbose_name="预置数据", help_text="预置数据")
    input_data = models.CharField(max_length=255, null=True, blank=True, verbose_name="结果数据", help_text="结果数据")
    test_action = models.CharField(max_length=255, null=True, blank=True, verbose_name="用例所属产品线", help_text="用例所属产品线")
    point_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="测试点类型", help_text="测试点类型")
    eff_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="生效时间", help_text="生效时间")
    exp_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="失效时间", help_text="失效时间")
    create_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="创建时间", help_text="创建时间")
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name="创建者", help_text="创建者")
    objects = t_test_case_info_qs.as_manager()


class TTemplateBindInfo(models.Model):
    """测试需求绑定用例模板"""
    require_id = models.IntegerField(null=False, verbose_name="测试需求id", help_text="测试需求id")
    template_id = models.IntegerField(null=False, verbose_name="模板id", help_text="模板id")
    class Meta:
        verbose_name = "测试需求绑定模板表"
        verbose_name_plural = verbose_name
        db_table = "t_template_bind_info"


class t_case_template_info(models.query.QuerySet):
    """根据模板名称查询模板信息返回分页数据"""

    def get_template_info(self, page, pageSize, **kwargs):
        """
        返回分页后的模板信息
        :param page: 当前页
        :param pageSize: 每页数量
        :param module_name: 模板名称
        :return:
        """
        module_name = kwargs.get('module_name')
        product_name = kwargs.get('product_name')
        template_list_info = self.filter(module_name__contains=module_name, module_type=product_name).order_by('-case_template_id')

        ptr = Paginator(template_list_info, pageSize)
        total_count = ptr.count
        cur_info = ptr.page(page)

        ret_info = [{"case_template_id": template.case_template_id,
                             "module_name": template.module_name,
                             "module_type": template.module_type,
                             "regular_type": template.regular_type,
                             "regular_type_flag": template.regular_type_flag,
                             "status": template.status,
                             "eff_time": template.eff_time,
                             "exp_time": template.exp_time,
                             "create_time": template.create_time,
                             "author": template.author,
                             } for template in cur_info]
        return ret_info, total_count

    def get_template_ids(self, module_type):
        """返回对应产品线的所有模板id"""
        template_info = self.filter(module_type=module_type).values()
        ids = [info['case_template_id'] for info in template_info if template_info.exists()]
        return ids


class TCaseTemplateInfo(models.Model):
    """测试用例模板管理表"""
    class Meta:
        verbose_name = "模板绑定用例信息表"
        verbose_name_plural = verbose_name
        db_table = "t_case_template_info"

    case_template_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="模板名称", help_text="模板名称")
    module_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="模板类型", help_text="模板类型")
    regular_type = models.IntegerField(null=True, blank=True)
    regular_type_flag = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, verbose_name="生效状态", help_text="生效状态")
    eff_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="生效时间", help_text="生效时间")
    exp_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="失效时间", help_text="失效时间")
    create_time = models.CharField(max_length=19, null=True, blank=True, verbose_name="创建时间", help_text="创建时间")
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name="创建用户", help_text="创建用户")
    objects = t_case_template_info.as_manager()


class t_test_check_isfocus_qs(models.query.QuerySet):
    """人工确认测试结果表自定义查询集"""
    def check_isfocus(self, value):
        """认同确认"""

        info = self.filter(offer_id=value["offer_id"],
                           session_id=value["session_id"]).values()
        if info.exists():
            self.filter(offer_id=value["offer_id"],
                        session_id=value["session_id"]).update(check_desc=value["check_desc"])
        else:
            check_info = TTestCheckIsfocus()
            check_info.prov_code = ''
            check_info.offer_id = value["offer_id"]
            check_info.batch = 1
            check_info.check_desc = value["check_desc"]
            check_info.session_id = value["session_id"]
            check_info.save()


class TTestCheckIsfocus(models.Model):
    """人工确认测试结果表"""
    class Meta:
        verbose_name = "确认测试结果表"
        verbose_name_plural = verbose_name
        db_table = "t_test_check_isfocus"
    prov_code = models.CharField(max_length=255, null=True, blank=True, verbose_name="省份代码", help_text="省份代码")
    offer_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="需求id", help_text="需求id")
    batch = models.IntegerField(null=True, blank=True, verbose_name="测试批次", help_text="测试批次")
    check_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="确认描述", help_text="确认描述")
    session_id = models.CharField(max_length=36, null=True, blank=True)
    objects = t_test_check_isfocus_qs.as_manager()


class TTestHostDataInfo(models.Model):
    host_id = models.AutoField(primary_key=True)
    host_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name="测试主机ip", help_text="测试主机ip")
    host_user = models.CharField(max_length=20, null=True, blank=True, verbose_name="登录用户", help_text="登录用户")
    host_pwd = models.CharField(max_length=128, null=True, blank=True, verbose_name="登录密码", help_text="登录密码")
    host_path = models.CharField(max_length=128, null=True, blank=True, verbose_name="主机路径", help_text="主机路径")
    exec_env = models.CharField(max_length=20, null=True, blank=True, verbose_name="主机环境类型", help_text="主机环境类型")
    is_cur_env = models.CharField(max_length=10, null=True, blank=True, verbose_name="当前主机测试", help_text="当前主机测试")
    product_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="产品名称", help_text="产品名称")

    class Meta:
        verbose_name = "测试主机管理表"
        verbose_name_plural = verbose_name
        db_table = 't_test_host_data_info'

class TTestDockerInfo(models.Model):
    container_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="容器名称", help_text="容器名称")
    exec_scripts = models.CharField(max_length=255, null=True, blank=True, verbose_name="执行命令脚本", help_text="执行命令脚本")
    product_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="产品名称", help_text="产品名称")
    program_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="容器代码目录", help_text="容器代码目录")
    local_program_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="主机代码目录", help_text="主机代码目录")
    result_log_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="容器结果目录", help_text="容器结果目录")
    local_log_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="主机结果目录", help_text="主机结果目录")
    svn_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="svn路径", help_text="svn路径")
    git_dir = models.CharField(max_length=255, null=True, blank=True, verbose_name="git路径", help_text="git路径")
    git_branch_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="git分支", help_text="git分支")
    vcs_type = models.CharField(max_length=64, null=True, blank=True, verbose_name="代码版本控制类型", help_text="代码版本控制类型")
    mark = models.CharField(max_length=255, null=True, blank=True, verbose_name="说明", help_text="说明")

    class Meta:
        verbose_name = "pytest单元全流程测试容器管理表"
        verbose_name_plural = verbose_name
        db_table = 't_test_docker_info'