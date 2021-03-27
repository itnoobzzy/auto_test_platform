import os
import time
import uuid

from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from config_manage.models import TTemplateBindInfo
from auto_test_platform.settings import BASE_DIR
from .serializers import *
from .models import *
from utils.deal_log import DealLog
from utils.deal_doc import DocxCaseInfo
from core.deal_paas_task import DealPaaSTask

log = DealLog()


class QueryInstanceInfo:
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.finish = 0
        self.total = 0
        self.test_status = '测试完成'
        self.result_infos = []
        self.info = {}

    def _get_test_action(self, case_id):
        """查询用例所属产品线"""
        test_action = ''
        case_info = TTestCaseInfo.objects.filter(case_id=case_id).values('test_action')
        for case in case_info:
            test_action = case['test_action']
        return test_action

    def _read_result(self, file_type, file_path, result_dict):
        """
        从结果文件中读取结果信息
        :param file_type: 结果文件类型：预期结果文件，实际结果文件，文件描述
        :param file_path: 结果文件路径
        :param result_dict:
        :return:
        """
        if file_type != 'result_desc':
            value = ''
            if file_path:
                value = codecs.open(file_path, encoding='gbk', errors='ignore').read()
            result_dict[file_type] = value
        else:
            result_dict[file_type] = file_path

    def _query_result_info(self, task_id, tmp_info):
        """
        查询任务结果信息
        :param task_id: 任务id
        :param tmp_info:
        :return:
        """
        result_dict = {"result_desc": "", "expect_result": "", "real_result": ""}

        result_info = TResultFileInfo.objects.filter(task_id=task_id).values()

        # 读取文件获得预期结果和实际结果
        for result in result_info:
            file_type = result['file_type']
            file_path = result['file_path']
            self._read_result(file_type, file_path, result_dict)

        tmp_info['diff_result'] = result_dict['result_desc']
        tmp_info['really_result'] = result_dict['real_result']
        tmp_info['expect_result'] = result_dict['expect_result']

        self.result_infos.append(tmp_info)

    def get_instance_info(self):
        """查询任务实例信息"""
        instance_id = self.instance_id
        task_infos = TTestTaskInfo.objects.filter(instance_id=instance_id).values()
        self.total = len(task_infos)
        for task_info in task_infos:
            tmp_info = dict()
            task_id = task_info['task_id']
            tmp_info['task_id'] = task_id
            tmp_info['test_name'] = task_info['test_name']
            tmp_info['test_action'] = self._get_test_action(task_info['case_id'])

            if task_info['end_time']:
                tmp_info['test_status'] = '已完成'
                self.finish += 1
            else:
                tmp_info['test_status'] = '未测试'
                self.test_status = '未完成'
            self._query_result_info(task_id, tmp_info)

        self.info['info'] = self.result_infos
        self.info['finish_count'] = self.finish
        self.info['executing_count'] = self.total - self.finish
        self.info['test_status'] = self.test_status
        return self.info


class TestResultViewSet(viewsets.ModelViewSet):
    """
    测试结构视图集
    check_test_require:
        查询测试结果信息
    query_result_detail:
        查询结果详情信息
    create_report:
        生成测试报告
    delete_test_result:
        删除测试结果
    """
    queryset = TTestRequireInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'check_test_require':
            return TestResultListSerializer
        elif self.action == 'query_result_detail':
            return ResultDetailSerializer

    def _handle_get_list(self, request, *args, **kwargs):
        """查询列表数据"""
        serializer = self.get_serializer(data=request.data)
        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            ret_dict['info']['ret_info'] = serializer.validated_data['list_info']
            ret_dict['info']['total_count'] = serializer.validated_data['total_count']
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def _add_table_2(self, doc, task_id_list, end_time, test_people):
        """测试列表表格"""
        task_num = 1
        for task_id in task_id_list:
            test_list_info = TTestTaskInfo.objects.get_test_list_info(task_id)

            doc.write_table(task_num, 0, '{}'.format(task_num))
            doc.write_table(task_num, 1, '{}'.format(test_list_info[0]))
            doc.write_table(task_num, 2, '{}'.format(test_list_info[1]))
            doc.write_table(task_num, 3, '{}'.format(test_list_info[2]))
            doc.write_table(task_num, 4, '{}'.format(end_time))
            doc.write_table(task_num, 5, '{}'.format(test_people))
            task_num += 1

    def _add_table_3(self, doc, task_id_list, test_people, end_time):
        """测试报告表格"""
        test_num = 1
        for task_id in task_id_list:
            info_dict = TTestTaskInfo.objects.get_test_report_info(task_id)

            doc.add_table("3.%s. %s" % (test_num, info_dict.get('case_name', '')))
            doc.write_table(0, 1, 'PaaS{}'.format(task_id))
            doc.write_table(0, 3, '{}'.format(test_people))
            doc.write_table(1, 1, "V1.0")
            doc.write_table(2, 1, "{}".format(info_dict.get('test_action', '')))
            doc.write_table(2, 3, info_dict['case_name'])
            doc.write_table(3, 1, "验证" + " " + info_dict.get('case_name', '') + " " + "是否正确")
            doc.write_table(4, 1, info_dict.get('case_type', '') + " 运行正常")
            doc.write_table(5, 1, info_dict.get('test_process', ''))
            for data in info_dict['expect_info_list']:
                try:
                    doc.write_table(6, 1, data)
                except:
                    doc.write_table(6, 1, '特殊字符无法处理')
            for data in info_dict['result_info_list']:
                try:
                    doc.write_table(7, 1, data)
                except:
                    doc.write_table(7, 1, '特殊字符无法处理')
            for data in info_dict['conclusion_info_list']:
                doc.write_table(8, 1, data)
            doc.write_table(9, 1, test_people)
            doc.write_table(9, 3, end_time[:10])
            test_num += 1

    @action(detail=False, methods=['post'], serializer_class=TestResultListSerializer, url_path='check_test_require')
    def check_test_require(self, request, *args, **kwargs):
        """查询结果信息列表"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TestResultListSerializer, url_path='query_result_detail')
    def query_result_detail(self, request, *args, **kwargs):
        """查询结果详情"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post', 'get'], url_path='create_report')
    def create_report(self, request, *args, **kwargs):
        """生成测试报告"""
        task_id_list = [data['task_id'] for data in request.data.get('info')]
        # TODO linux
        os.system(f'mkdir {BASE_DIR}/report_file')

        end_time, test_name, test_people, instance_id = TTestTaskInfo.objects.get_test_conclusion_info(task_id_list[0])

        path = BASE_DIR + '/report_file/{}出厂测试报告.docx'.format(instance_id)

        if not os.path.exists(path):
            task_id_list = TTestTaskInfo.objects.get_task_id_list(instance_id)
            task_id_num = len(task_id_list)
            test_pass_num = len(TResultFileInfo.objects.filter(task_id__in=task_id_list, file_type='result_desc', file_path='通过'))

            doc = DocxCaseInfo(path)

            doc.add_table_1("1. 测试结论")
            doc.write_table(1, 0, '{}'.format(task_id_num))
            doc.write_table(1, 1, '{}'.format(test_pass_num))
            doc.write_table(1, 2, '{}'.format(task_id_num - test_pass_num))
            doc.write_table(1, 3, '{}'.format(end_time))
            doc.write_table(1, 4, '{}'.format(test_people))

            doc.add_table_2("2. 测试列表", task_id_num + 1)
            self._add_table_2(doc, task_id_list, end_time, test_people)

            doc.add_table_3("3. 测试报告")
            self._add_table_3(doc, task_id_list, test_people, end_time)

            doc.save()
        os.system('cp %s %s/static/%s出厂测试报告.docx' % (path, BASE_DIR, test_name))
        return HttpResponse(f'./static/{test_name}出厂测试报告.docx')

    @action(detail=False, methods=['post'], url_path='delete_test_result')
    def delete_test_result(self, request, *args, **kwargs):
        """删除测试结果"""
        ret_dict = {
            'status': 0,
            'info': '删除成功'
        }

        require_id = request.data.get('require_id', 0)
        # 删除测试需求绑定的模板信息
        TTemplateBindInfo.objects.filter(require_id=require_id).delete()
        # 删除测试需求信息
        TTestRequireInfo.objects.filter(require_id=require_id).delete()
        log.info("测试结果删除成功")
        return Response(ret_dict, status.HTTP_200_OK)


class WholeProcessTestViewSet(viewsets.ModelViewSet):
    """
    全流程测试视图集
    query_history_test:
        查询历史测试记录
    create_whole_process_task:
        生成全流程测试任务
    query_instance_info:
        查询任务实例信息
    """

    queryset = TTestRequireInfo.objects.all()

    def _create_instance_info(self, product_name, user_name, require_name, id_list):
        """
        生成任务实例信息， 返回实例id
        :param product_name: 产品名称
        :param require_name: 测试名称
        :param id_list: 绑定用例id列表
        :param user_name: 用户名称
        :return:
        """
        # 删除相同测试名称的历史测试记录
        # 包括测试需求信息表和任务实例信息表
        TTestRequireInfo.objects.filter(require_name=require_name).delete()
        TTestInstanceInfo.objects.filter(offer_id=require_name).delete()

        # 往测试需求信息表中和实例信息表中插入数据
        info = TTestRequireInfo()
        info.require_name = require_name
        info.offer_id = ''
        info.offer_name = ''
        info.require_source = product_name
        info.test_claim = user_name
        info.test_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info.require_file_desc = ''
        info.test_status = '未测试'
        info.save()

        ins_info = TTestInstanceInfo()
        ins_info.session_id = uuid.uuid1().hex
        ins_info.offer_id = require_name
        ins_info.test_people = user_name
        ins_info.product_name = product_name
        ins_info.save()
        instance_id = ins_info.instance_id

        # 查询任务用例信息
        case_id_list = id_list
        case_info = TTestCaseInfo.objects.filter(case_id__in=case_id_list).values()
        for task in case_info:
            # 创建task_info，生成task_id
            task_info = TTestTaskInfo()
            task_info.instance_id = instance_id
            task_info.test_name = task["case_name"]
            task_info.case_id = task["case_id"]
            task_info.product_name = product_name
            task_info.save()
        return instance_id

    @action(detail=False, methods=['post'], url_path='query_history_test')
    def query_history_test(self, request, *args, **kwargs):
        """查询历史测试记录"""
        ret_dict = {
            'status': 0,
            'info': {}
        }
        require_name = request.data.get('require_name', '')
        test_date = request.data.get('test_date', '')
        product_name = request.data.get('product_name', '')
        page = request.data.get('page', 1)
        pageSize = request.data.get('pageSize', 1)

        require_info = TTestRequireInfo.objects.filter(require_name__contains=require_name,
                                                          require_source=product_name,
                                                          test_date__contains=test_date).values().distinct()

        ptr = Paginator(require_info, pageSize)
        total_count = ptr.count
        require = ptr.page(page)

        info = [{
            'require_name': _['require_name'],
            'test_date': _['test_date'],
            'test_people': _['test_claim']
        } for _ in require]

        ret_dict['info']['ret_info'] = info
        ret_dict['info']['total_count'] = total_count

        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='create_whole_process_task')
    def create_whole_process_task(self, request, *args, **kwargs):
        """生成全流程测试任务"""
        ret_dict = {
            'status': 0,
            'info': {}
        }

        require_name = request.data.get('require_name', '')
        id_list = request.data.get('id_list', [])
        product_name = request.data.get('product_name', '')
        user_name = request.data.get('user_name', '')

        instance_id = self._create_instance_info(product_name, user_name, require_name, id_list)

        ret_dict['info']['instance_id'] = instance_id
        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='query_instance_info')
    def query_instance_info(self, request, *args, **kwargs):
        """查询任务实例信息"""
        ret_dict = {
            'status': 0, 
            'info': {}
        }

        instance_id = request.data.get('instance_id', 0)
        try:
            info = QueryInstanceInfo(instance_id).get_instance_info()
        except Exception as e:
            log.info(f'查询任务实例信息异常：{e}')
        else:
            ret_dict['info'] = info
        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='start_paas_task')
    def start_paas_task(self, request, *args, **kwargs):
        """开始执行paas任务测试"""
        ret_dict = {
            'status': 0,
            'info': {}
        }
        try:
            deal_test = DealPaaSTask(request)
            deal_test.start_test()
        except Exception as e:
            log.info(f'全流程测试异常：{e}')
            ret_dict['status'] = 500
            ret_dict['info'] = '全流程测试异常'
        return Response(ret_dict, status.HTTP_200_OK)

