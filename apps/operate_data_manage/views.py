import os
import psutil
import xlrd

from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from numpy.core.fromnumeric import mean
from dateutil.parser import parse
from openpyxl import Workbook

from auto_test_platform.settings import BASE_DIR, PRODUCT_VER, PROV_NAME, CUR_BRANCH
from config_manage.models import TTestCaseInfo
from whole_process_test.models import (
    TTestTaskInfo,
    TTestInstanceInfo
)
from .serializers import *
from .models import *
from utils.deal_log import DealLog


log = DealLog()


class OperateDataViewSet(viewsets.ModelViewSet):
    """
    运营数据展示视图集
    get_product_area_list:
        查询产品落地省份列表
    get_view_info:
        运营数据视图信息: 里程碑信息，能力展示信息
    get_detail_info:
        对应省份运营数据详情信息
    """

    queryset = TTestOperateDataInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'get_product_area_list':
            return AreaListSerializer
        elif self.action == 'get_view_info':
            return ViewInfoSerializer

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

    @action(detail=False, methods=['post'], serializer_class=AreaListSerializer, url_path='get_product_area_list')
    def get_product_area_list(self, request, *args, **kwargs):
        """查询产品落地省份列表"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=ViewInfoSerializer, url_path='get_view_info')
    def get_view_info(self, request, *args, **kwargs):
        """查询测试能力信息和里程碑信息"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=ViewInfoSerializer, url_path='get_detail_info')
    def get_detail_info(self, request, *args, **kwargs):
        """查询测试能力信息和里程碑信息"""
        ret_dict = {
            'status': 0,
            'info': []
        }
        area = request.data.get('area', '')
        product_name = request.data.get('product_name', '')
        # 获取当前产品及地区有数据的月份
        month_data = TTestOperateDataInfo.objects.filter(
            prov_name=area, product_name=product_name, show_flag='是')\
            .values('operative_sub_index', 'operate_month')\
            .distinct().order_by('operate_month')
        month_dict = {}
        for data in month_data:
            if data['operative_sub_index'] not in month_dict.keys():
                month_dict[data['operative_sub_index']] = [data['operate_month']]
            else:
                month_dict[data['operative_sub_index']].append(data['operate_month'])

        info = self._get_platform(month_dict, product_name, area)
        ret_dict['info'] = info

        return Response(ret_dict, status.HTTP_200_OK)

    def _get_platform(self, month_dict, product_name, area):
        info = []
        operate_data = TTestOperateDataInfo.objects.filter(prov_name=area, product_name=product_name, show_flag='是').values('operative_sub_index').distinct()
        for data in operate_data:
            operative_sub_index = data['operative_sub_index']

            cur_month = month_dict[operative_sub_index][-1]
            last_month = month_dict[operative_sub_index][-2] if len(month_dict[operative_sub_index]) >= 2 else '0'

            cur_data = TTestOperateDataInfo.objects.filter(prov_name=area, product_name=product_name, operate_month=cur_month, operative_sub_index=operative_sub_index, show_flag='是').values()
            last_data = TTestOperateDataInfo.objects.filter(prov_name=area, product_name=product_name, operate_month=last_month,operative_sub_index=operative_sub_index, show_flag='是').values()

            units = ''
            target_value = operate_data = last_operate_data = 0
            for cur in cur_data:
                operate_data = cur['operate_data'].replace('%', '')
                units = cur['units']
                target_value = cur['target_value']
            for last in last_data:
                last_operate_data = last['operate_data'].replace('%', '')

            info.append({"unit": units,
                         "title": operative_sub_index,
                         "data": [last_operate_data, operate_data, target_value]})

        return info


class OperateDataConfigViewSet(viewsets.ModelViewSet):
    """
    运营数据配置管理视图集
    get_area_prov_list:
        得到运营数据省份参数信息
    get_operate_data_info:
        获取运营数据配置列表信息
    update_operate_data_info:
        更新运营数据配置
    """
    queryset = TTestOperateDataInfo.objects.all()

    xlsxBook = None

    def get_serializer_class(self):
        if self.action == 'get_area_prov_list':
            return AreaProvListSerializer
        elif self.action == 'get_operate_data_info':
            return OperateConfigListSerializer
        elif self.action == 'update_operate_data_info':
            return OperateConfigInfoSerializer

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

    def _handle_update_or_add(self, request, *args, **kwargs):
        """
        更新或者新增数据
        更新需要根据action定义查询字段，传入instance
        """
        if self.action == 'update_operate_data_info':
            self.lookup_field = 'id'
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            if self.action == 'update_operate_data_info':
                self.perform_update(serializer)
            else:
                self.perform_create(serializer)
            ret_dict['info'] = '编辑成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=AreaProvListSerializer, url_path='get_area_prov_list')
    def get_area_prov_list(self, request, *args, **kwargs):
        """得到运营数据省份参数信息"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=OperateConfigListSerializer, url_path='get_operate_data_info')
    def get_operate_data_info(self, request, *args, **kwargs):
        """获取运营数据配置列表信息"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=OperateConfigInfoSerializer,
            queryset=TTestOperateDataInfo.objects.all(),
            url_path='update_operate_data_info/(?P<id>\d+)')
    def update_operate_data_info(self, request, *args, **kwargs):
        """获取运营数据配置列表信息"""
        return self._handle_update_or_add(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='get_prov_operate_data')
    def get_prov_operate_data(self, request, *args, **kwargs):
        """运营数据收集"""
        ret_dict = {
            'status': 0,
            'info': '收集成功'
        }
        product_name = request.data.get('product_name', '')
        # 当月月份
        cur_month = time.strftime('%Y-%m', time.localtime(time.time()))
        # 测试用例数
        case_num = Paginator(TTestCaseInfo.objects.filter(case_type=product_name), 1).count
        # 自动化测试次数
        instance_num = Paginator(TTestInstanceInfo.objects.filter(start_time__contains=cur_month, product_name=product_name), 1).count
        # 测试用例执行次数
        task_num = Paginator(TTestTaskInfo.objects.filter(begin_time__contains=cur_month, product_name=product_name), 1).count
        # 测试用例平均耗时
        use_time_info = TTestTaskInfo.objects.filter(begin_time__contains=cur_month, product_name=product_name).exclude(begin_time='').exclude(end_time='').values('begin_time', 'end_time')
        use_time_list = [(parse(_['end_time']) - parse(_['begin_time'])).seconds for _ in use_time_info]
        user_time = mean(use_time_list) if use_time_list else 0
        use_time = '%.2f' % (user_time / 60)

        # 接口能力调用次数
        use_num = Paginator(TTestRecordDataInfo.objects.filter(cur_month=cur_month), 1).count

        # 错误日志行数
        err_num = int(os.popen("sed -n '/%s/p' %s/*.log | awk '/ERROR/' | wc -l" % (BASE_DIR, cur_month)).read())

        # TODO： 数据暂时写死后期可以使用执行脚本判断
        program_status = '正常'
        # cpu状态
        cpu_percent = psutil.cpu_percent()
        # 内存状态
        memory_percent = psutil.virtual_memory().percent
        # 磁盘状态
        disk_percent = psutil.disk_usage('/').percent

        operative_list = ['测试能力' for _ in range(4)] + ['性能效率'] + ['运行环境' for _ in range(5)]
        operative_sub_list = ['测试用例数', '自动化测试次数', '测试用例执行次数', '接口能力调用次数', '测试用例平均耗时', '错误日志条数', '应用系统状态', 'CPU状态', '内存状态', '磁盘状态']
        operate_desc_list = ['系统支持的测试用例数量', '自动化测试使用次数', '测试用例执行次数', '接口能力调用次数', '每个测试用例执行时间', '错误日志信息，出现错误日志预警', '进程运行状态，进程异常预警', 'CPU使用率低于75%，达到75%预警', '内存使用率低于80%，达到80%预警', '磁盘使用率低于80%，达到80%预警']
        operate_data_list = [case_num, instance_num, task_num, use_num, use_time, err_num, program_status, cpu_percent, memory_percent, disk_percent]
        units_list = ['个', '次', '次', '次', '分钟', '条', '', '%', '%', '%']
        product_name_list = [product_name for _ in range(len(units_list))]

        list(map(create_operate_data, operative_list, operative_sub_list, operate_desc_list, operate_data_list, units_list, product_name_list))
        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add_operate_data_info')
    def add_operate_data_info(self, request, *args, **kwargs):
        """新增运营数据"""
        operate_info = request.data.get('operate_info', [])
        for operate in operate_info:
            product_name = operate['product_name']
            product_ver = PRODUCT_VER.get(product_name, '')
            data = TTestOperateDataInfo()
            data.product_name = product_name
            data.operate_month = operate['operate_month']
            data.prov_name = PROV_NAME if CUR_BRANCH != 'PaaS' else '%s %s' % (product_name, product_ver)
            data.prov_type = operate['prov_type']
            data.operative_index = operate['operative_index']
            data.operative_sub_index = operate['operative_sub_index']
            data.operate_desc = operate['operate_desc']
            data.operate_data = operate['operate_data']
            data.product_ver = product_ver
            data.units = operate['units']
            data.show_flag = operate['target_value']
            data.target_value = operate['show_flag']
            data.save()
        return Response({'status': 0, 'info': '新增成功'}, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='delete_operate_data_info')
    def delete_operate_data_info(self, request, *args, **kwargs):
        """删除运营数据"""
        id = request.data.get('id')
        TTestOperateDataInfo.objects.filter(id=id).delete()
        return Response({'status': 0, 'info': '新增成功'}, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='get_operate_month')
    def get_operate_month(self, request, *args, **kwargs):
        """查询已有月份运营数据"""
        data_info = TTestOperateDataInfo.objects.filter().values('operate_month').distinct().order_by('-operate_month')
        info = [{'value': data['operate_month'], 'label': data['operate_month']} for data in data_info]
        return Response({'status': 0, 'info': info}, status.HTTP_200_OK)

    def _write_sheet(self):
        self.xlsxBook = Workbook()
        sheet1 = self.xlsxBook.create_sheet('sheet1', 0)
        sheet1['A1'] = '产品名称'
        sheet1['B1'] = '版本号'
        sheet1['C1'] = '月份'
        sheet1['D1'] = '运营省份'
        sheet1['E1'] = '省份类型'
        sheet1['F1'] = '运营数据类型'
        sheet1['G1'] = '运营数据名称'
        sheet1['H1'] = '运营数据描述'
        sheet1['I1'] = '当月运营数据值'
        sheet1['J1'] = '是否展示'
        sheet1['K1'] = '单位'
        sheet1['L1'] = '当月运营数据目标值'
        return sheet1

    @action(detail=False, methods=['post'], url_path='download_operate_template')
    def download_operate_template(self, request, *args, **kwargs):
        """下载运营数据导入模板"""
        file_name = 'operate.xlsx'
        path = BASE_DIR + '/static/' + file_name
        self._write_sheet()
        self.xlsxBook.save(path)

        return HttpResponse('./static/{}'.format(file_name))

    @action(detail=False, methods=['post'], url_path='import_operate_data')
    def import_operate_data(self, request, *args, **kwargs):
        """导入运营数据"""
        FILES = request.FILES.get("file", None)
        file = xlrd.open_workbook(file_contents=FILES.read())

        table = file.sheet_by_index(0)

        try:
            nrows = table.nrows
            for row in range(1, nrows):
                data = TTestOperateDataInfo()
                data.product_name = table.cell_value(row, 0)
                data.product_ver = table.cell_value(row, 1)
                data.operate_month = str(table.cell_value(row, 2)).replace('.0', '')
                data.prov_name = table.cell_value(row, 3)
                data.prov_type = table.cell_value(row, 4)
                data.operative_index = table.cell_value(row, 5)
                data.operative_sub_index = table.cell_value(row, 6)
                data.operate_desc = table.cell_value(row, 7)
                data.operate_data = str(table.cell_value(row, 8)).replace('.0', '')
                data.show_flag = table.cell_value(row, 9)
                data.units = table.cell_value(row, 10)
                data.target_value = table.cell_value(row, 11)

                data.save()

            return Response({"status": 0, "info": "操作成功"}, status.HTTP_200_OK)
        except Exception as e:
            log.error(f'导入运营数据失败：{e}')
            return HttpResponse({"status": -2, "info": str(e)}, status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='export_operate_data')
    def export_operate_data(self, request, *args, **kwargs):
        """导出运营数据"""
        file_name = 'operate.xls'
        path = BASE_DIR + '/static/' + file_name
        sheet1 = self._write_sheet()
        operate_month = request.data.get('operate_month', '')
        operate_data = TTestOperateDataInfo.objects.filter(operate_month__contains=operate_month).values()

        index = 2
        for data in operate_data:
            sheet1['A%s' % index] = data['product_name']
            sheet1['B%s' % index] = data['product_ver']
            sheet1['C%s' % index] = data['operate_month']
            sheet1['D%s' % index] = data['prov_name']
            sheet1['E%s' % index] = data['prov_type']
            sheet1['F%s' % index] = data['operative_index']
            sheet1['G%s' % index] = data['operative_sub_index']
            sheet1['H%s' % index] = data['operate_desc']
            sheet1['I%s' % index] = data['operate_data']
            sheet1['J%s' % index] = data['show_flag']
            sheet1['K%s' % index] = data['units']
            sheet1['L%s' % index] = data['target_value']
            index += 1
        self.xlsxBook.save(path)

        return HttpResponse('./static/{}'.format(file_name))

def create_operate_data(operative_index, operative_sub_index, operate_desc, operate_data, units, product_name):
    """保存运营数据"""
    # 当月月份
    cur_month = time.strftime('%Y-%m', time.localtime(time.time()))
    product_ver = PRODUCT_VER.get(product_name, '')
    prov_name = PROV_NAME if CUR_BRANCH != 'PaaS' else '%s %s' % (product_name, product_ver)
    TTestOperateDataInfo.objects.filter(prov_name=prov_name, operative_index=operative_index,
                                        operative_sub_index=operative_sub_index,
                                        operate_month=cur_month).delete()

    data = TTestOperateDataInfo()
    data.product_name = product_name
    data.product_ver = product_ver
    data.operate_month = cur_month
    data.prov_name = prov_name
    data.prov_type = 1 if CUR_BRANCH == 'PaaS' else 2
    data.operative_index = operative_index
    data.operative_sub_index = operative_sub_index
    data.operate_desc = operate_desc
    data.operate_data = operate_data
    data.show_flag = '是'
    data.units = units
    data.target_value = ''
    data.save()
