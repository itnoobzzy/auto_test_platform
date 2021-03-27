import codecs
from django.db import models
from django.core.paginator import Paginator

from config_manage.models import TTestCaseInfo


class t_test_require_info_qs(models.query.QuerySet):
    """测试结果信息自定义查询集"""
    def get_test_result_info(self, page, pageSize, **kwargs):
        """降序返回所有测试任务的测试结果"""
        product_name = kwargs.get('product_name', '')
        require_name = kwargs.get('require_name', '')
        test_status = kwargs.get('test_status', '')

        result_info = self.filter(require_source=product_name,
                                  require_name__contains=require_name,
                                  test_status__contains=test_status).order_by('-test_date')
        ptr = Paginator(result_info, pageSize)
        total_count = ptr.count
        cur_info = ptr.page(page)
        info = [{'require_id': key.require_id,
                  'require_name': key.require_name,
                  'require_source': key.require_source,
                  'test_people': key.test_claim,
                  'test_date': key.test_date,
                  'test_status': key.test_status} for key in cur_info]

        return info, total_count


class TTestRequireInfo(models.Model):
    """测试结果信息表"""
    require_id = models.AutoField(primary_key=True)
    require_name = models.CharField(max_length=64, null=False, blank=False, verbose_name="测试名称")
    offer_id = models.CharField(max_length=64, null=True)
    offer_name = models.CharField(max_length=256, null=True)
    require_source = models.CharField(max_length=64, null=False, blank=False, verbose_name="产品线名称")
    test_claim = models.CharField(max_length=256, null=False, verbose_name="测试人员")
    test_date = models.CharField(max_length=19, null=False, blank=False, verbose_name="测试时间")
    test_status = models.CharField(max_length=16, null=False, blank=False, verbose_name="测试状态")
    require_file_desc = models.CharField(max_length=512, null=True)
    objects = t_test_require_info_qs.as_manager()

    class Meta:
       db_table = "t_test_require_info"
       verbose_name = "测试结果信息表"


class TResultFileInfo(models.Model):
    """预期结果和实际结果文件信息"""
    class Meta:
        db_table = "t_test_result_file_info"
        verbose_name = "获取测试结果文件信息"

    task_id = models.IntegerField()
    file_type = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)


class t_test_instance_info_qs(models.query.QuerySet):
    """测试实例信息表自定义查询集"""
    def get_instance_info(self, offer_id):
        """根据offer_id查询实例信息"""
        return self.filter(offer_id=offer_id).exclude(end_time='').values().order_by('-end_time') or ''

    def save_data(self, save_id=None, **kwargs):
        db = self.model()
        print(db)
        for key, value in kwargs.items():
            setattr(db, key, value)
        db.save()
        return getattr(db, save_id)


class TTestInstanceInfo(models.Model):
    """测试实例信息表"""
    instance_id = models.AutoField(primary_key=True, verbose_name="任务实例id")
    session_id = models.CharField(max_length=36, null=True)
    offer_id = models.CharField(max_length=64, null=False, blank=False, verbose_name="产品名称")
    start_time = models.CharField(max_length=19, null=False, blank=False, verbose_name="任务开始时间")
    end_time = models.CharField(max_length=19, null=False, blank=False, verbose_name="任务结束时间")
    test_people = models.CharField(max_length=19, null=False, blank=False, verbose_name="测试人员")
    product_name = models.CharField(max_length=128, null=False, blank=False, verbose_name="所属产品线")
    objects = t_test_instance_info_qs.as_manager()

    class Meta:
        db_table = "t_test_instance_info"
        verbose_name = "测试实例信息表"


class t_test_task_info_qs(models.query.QuerySet):
    """测试结果信息表查询集"""

    def get_task_id_list(self, instance_id):
        """获取对应实例id下的所有任务id"""
        task_info = self.filter(instance_id=instance_id).values('task_id')
        task_id_list = [info['task_id'] for info in task_info]
        return task_id_list

    def get_test_conclusion_info(self, task_id):
        """得到测试报告结论信息：结束时间、产品名称、测试人员"""
        data_info = self.filter(task_id=task_id).values().distinct()
        for data in data_info:
            instance_id = data['instance_id']
            end_time = data['end_time']
            ins_info = TTestInstanceInfo.objects.filter(instance_id=instance_id).values('offer_id')
            offer_id = ins_info[0].get('offer_id', '')
            test_people = ins_info[0].get('test_people', '')
            require_info = TTestRequireInfo.objects.filter(require_name=offer_id).values('require_source', 'test_claim')
            product_name = require_info[0].get('require_source', '')

        return end_time, product_name, test_people, instance_id

    def get_test_list_info(self, task_id):
        """查询生成测试报告测试列表信息"""
        task_info = self.filter(task_id=task_id).values()
        test_action = case_name = ''
        for task in task_info:
            case_id = task['case_id']
            case_info = TTestCaseInfo.objects.filter(case_id=case_id).values()
            for case in case_info:
                test_action = case['test_action']
                case_name = case['case_name']

        result_info = TResultFileInfo.objects.filter(task_id=task_id, file_type='result_desc').exclude(file_path='通过')
        test_pass = '不通过' if result_info else '通过'

        return test_action, case_name, test_pass

    def _get_special_test_result(self, field_code, field_value, expect_info_list, result_info_list, conclusion_info_list):
        """获取特殊测试结果，单元测试结果"""
        if field_code == 'expect_result':
            real_result = codecs.open(field_value, encoding='gbk', errors='ignore').read()
            expect_info_list.append('通过')
            result_info_list.append(real_result)
        elif field_code == 'result_desc':
            conclusion_info_list.append(field_value)

    def _get_test_report(self, task_id, expect_info_list, result_info_list, conclusion_info_list, point_type):
        result_info = TResultFileInfo.objects.filter(task_id=task_id).values()
        for result in result_info:
            field_code = result['file_type']
            field_value = result['file_path']
            if point_type == '单元测试':
                self._get_special_test_result(field_code, field_value, expect_info_list, result_info_list, conclusion_info_list)
            else:
                if field_code == 'expect_result':
                    expect_result = codecs.open(field_value, encoding='gbk', errors='ignore').read()
                    expect_info_list.append(expect_result)
                elif field_code == 'real_result':
                    real_result = codecs.open(field_value, encoding='gbk', errors='ignore').read()
                    result_info_list.append(real_result)
                elif field_code == 'result_desc':
                    conclusion_info_list.append(field_value)

    def get_test_report_info(self, task_id):
        """查询测试报告报告信息"""
        ret_dic = {}
        task_info = self.filter(task_id=task_id).values()
        test_action = case_name = case_type = test_process = point_type = ''
        for task in task_info:
            case_id = task['case_id']
            case_info = self.filter(case_id=case_id).values()
            for case in case_info:
                test_action = case.get('test_action', '')
                case_name = case.get('case_name', '')
                case_type = case.get('case_type', '')
                test_process = case.get('test_process', '')
                point_type = case.get('point_type', '')

        expect_info_list = list()
        result_info_list = list()
        conclusion_info_list = list()
        self._get_test_report(task_id, expect_info_list, result_info_list, conclusion_info_list, point_type)

        ret_dic['test_action'] = test_action
        ret_dic['case_name'] = case_name
        ret_dic['case_type'] = case_type
        ret_dic['test_process'] = test_process
        ret_dic['conclusion_info_list'] = conclusion_info_list
        ret_dic['expect_info_list'] = expect_info_list
        ret_dic['result_info_list'] = result_info_list
        return ret_dic


class TTestTaskInfo(models.Model):
    """测试任务信息表"""
    task_id = models.AutoField(primary_key=True)
    instance_id = models.IntegerField(null=False, verbose_name="任务实例id")
    test_name = models.CharField(max_length=255, null=True, verbose_name="测试名称")
    begin_time = models.CharField(max_length=19, null=True, verbose_name="任务开始时间")
    end_time = models.CharField(max_length=19, null=True, verbose_name="任务结束时间")
    case_id = models.IntegerField(null=False, verbose_name="用例id")
    product_name = models.CharField(max_length=128)
    objects = t_test_task_info_qs.as_manager()

    class Meta:
       db_table = "t_test_task_info"
       verbose_name = "测试任务信息表"

