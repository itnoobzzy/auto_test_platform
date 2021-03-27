import xlrd
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import *
from .models import *
from utils.deal_excel import DealExcel
from utils.deal_log import DealLog
from auto_test_platform.settings import BASE_DIR


log = DealLog()


class TemplateCaseViewSet(viewsets.ModelViewSet):
    """
    模板用例视图集
    check_case_template:
        返回模板列表信息
    check_case_info:
        返回用例列表信息
    update_case_info：
        更新用例信息
    add_case_info：
        增加用例
    delete_case_info:
        删除用例
    update_template_info:
        更新模板信息
    add_template_info:
        新增模板
    delete_template_info:
        删除模板
    get_template_bind_case:
        获取模板绑定用例信息
    get_template_unbind_case:
        获取模板未绑定用例信息
    """
    queryset = TCaseTemplateInfo.objects.all()
    insert_case_num = 0
    insert_template_num = 0

    def get_serializer_class(self):
        """根据访问动作获取序列化类"""
        if self.action == 'check_case_template':
            return TemplateListSerializer
        elif self.action == 'check_case_info':
            return CaseListSerializer
        elif self.action == 'update_case_info' or self.action == 'add_case_info' or self.action == 'delete_case_info':
            return CaseInfoSerializer
        elif self.action == 'update_template_info' or self.action == 'add_template_info' or self.action == 'delete_template_info':
            return TemplateInfoSerializer
        elif self.action == 'get_template_bind_case':
            return TemplateBindCaseInfoSerializer
        elif self.action == 'get_template_unbind_case':
            return TemplateUnBindCaseInfoSerializer
        return TemplateInfoSerializer

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
        if self.action == 'update_case_info':
            self.lookup_field = 'case_id'
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        elif self.action == 'update_template_info':
            self.lookup_field = 'case_template_id'
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)

        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            if self.action == 'update_case_info':
                self.perform_update(serializer)
            else:
                self.perform_create(serializer)
            ret_dict['info'] = '编辑成功'
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def _handle_delete(self, request, *args, **kwargs):
        """删除列表数据"""
        if self.action == 'delete_case_info':
            self.lookup_field = 'case_id'
        else:
            self.lookup_field = 'case_template_id'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        ret_dict = {
            'status': 0,
            'info': {}
        }
        if serializer.is_valid(raise_exception=False):
            self.perform_destroy(instance)
            ret_dict['info'] = "删除成功"
        else:
            ret_dict['errors'] = serializer.errors
            ret_dict['status'] = 400

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        add_info = serializer.save()
        if self.action == 'add_case_info':
            # 如果是新增用例，就得同时在模板绑定用例的桥表中新增对应数据
            self._handle_case_bind_template(add_info)

    def _handle_case_bind_template(self, case_info):
        """
            如果是新增用例,在用例表新增后就得同时在模板绑定用例的桥表中新增,
        """
        case_template_id = self.request.data.get('case_template_id')
        bind_info = {
            'case_template_id': case_template_id,
            # 'case_template_id': 2318,
            'case_id': case_info.case_id
        }
        TemplateBindCaseInfo.objects.create(**bind_info)

    def perform_destroy(self, instance):
        """如果是删除模板需要将模板表和模板绑定用例的桥表对应的也删除"""
        try:
            # 获取不到模板id的话说明是删除用例
            template_id = instance.case_template_id
        except Exception:
            # 同时删除模板用例桥表中包含该用例的数据
            TemplateBindCaseInfo.objects.filter(case_id=instance.case_id).delete()
            # 删除测试用例
            instance.delete()
        else:
            TemplateBindCaseInfo.objects.filter(case_template_id=template_id).delete()
            TCaseTemplateInfo.objects.filter(case_template_id=template_id).delete()

    def _get_export_info(self, template_id, product_name):
        """
        查询需要导出的用模板例信息
        :param template_id: 模板id
        :param product_name: 模板所属产品线名称
        :return:
        """
        template_info = TCaseTemplateInfo.objects.filter(case_template_id=template_id, module_type=product_name).values()
        template_name = ''
        module_type = ''
        for template in template_info:
            template_name = template['module_name']
            module_type = template['module_type']
        case_info_list = TemplateBindCaseInfo.objects.get_bind_case_info(template_id)

        return template_name, module_type, case_info_list

    def _handle_write(self, sheet, index, template_name, case_info_list, module_type):
        """excel sheet写入数据"""
        sheet['A%s' % index] = template_name
        for case_info in case_info_list:
            sheet['B%s' % index] = case_info['case_name']
            sheet['C%s' % index] = module_type
            sheet['D%s' % index] = case_info['case_num']
            sheet['E%s' % index] = case_info['input_data']
            sheet['F%s' % index] = case_info['preset_data']
            index += 1
        log.info(f'paas_index:{index}')
        log.info(f'case_info_list:{case_info_list}')
        if len(case_info_list) >= 2:
            sheet.merge_cells(f'A{(index - len(case_info_list))}:A{index-1}')
        return index

    def _get_sheet(self, title, index, sheet_header=None):
        """构造Excel sheet对象"""
        # 构造表头
        sheet_header = sheet_header
        if not sheet_header:
            sheet_header = {
                'A1': '测试模板',
                'B1': '测试用例',
                'C1': '产品名称',
                'D1': '测试用例ID',
                'E1': '测试脚本路径',
                'F1': '预期结果路径'
            }
        sheet = self.deal_excel.create_sheet(title, index, **sheet_header)
        return sheet

    def _deal_row_list(self, rows, row_list):
        """处理行获取的行数据"""
        if rows not in row_list:
            if row_list:
                if rows[-1] not in row_list[-1]:
                    row_list.append(rows)
            else:
                row_list.append(rows)

    def _get_row_list(self, file, index):
        """获取行数据列表"""
        table = file.sheet_by_index(index)
        nrows = table.nrows
        log.info(f'有效行数:{nrows}')
        merged = table.merged_cells
        log.info(f'合并单元格:{merged}')
        row_list = []
        for row_index in range(1, nrows):
            rows = []
            for (rlow, rhight, clow, chigh) in merged:
                if (rhight > row_index >= rlow and chigh > 0 >=clow):
                    rows = [i for i in range(row_index, rhight)]
            if not rows:
                rows.append(row_index)
            self._deal_row_list(rows, row_list)
        log.info(f'row_list:{row_list}')
        return row_list
    
    def _insert_template_table(self, template_name, module_type, user_name):
        """插入模板表"""
        save_data = {
            'module_name': template_name,
            'module_type': module_type,
            'author': user_name
        }
        template_info = TCaseTemplateInfo.objects.create(**save_data)
        template_id = template_info.case_template_id
        return template_id

    def _insert_bind_table(self, case_id, template_id):
        """插入桥表数据"""
        case_bind_info = TemplateBindCaseInfo.objects.filter(case_template_id=template_id, case_id=case_id).values()
        if not case_bind_info:
            save_data = {
                'case_template_id': template_id,
                'case_id': case_id
            }
            TemplateBindCaseInfo.objects.create(**save_data)

    def _insert_case_table(self, table, row, template_id, module_type, user_name):
        """插入用例表"""
        self.insert_case_num = 1
        case_name = table.cell_value(row, 1)
        case_num = table.cell_value(row, 3)
        input_data = table.cell_value(row, 4)
        preset_data = table.cell_value(row, 5)

        case_info = TTestCaseInfo.objects.filter(case_name=case_name).values()

        if case_info:
            try:
                case_id = case_info[0]['case_id']
            except IndexError:
                case_id = case_info[0][0]
        else:
            save_data = {
                'case_name': case_name,
                'case_type': module_type,
                'preset_data': preset_data,
                'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                'author': user_name,
                'input_data': input_data,
                'test_action': case_num
            }
            case_id = TTestCaseInfo.objects.create(**save_data).case_id

            self.insert_case_num += 1

        # 插入桥表数据
        self._insert_bind_table(case_id, template_id)

    def _insert_table(self, rows, table, user_name):
        """将表格获取的行数据插入表"""
        # 需要插入的模板数据数量
        self.insert_template_num = 1

        template_name = table.cell_value(rows[0], 0)
        module_type = table.cell_value(rows[0], 2)
        log.info('template_name:%s, %s' % (template_name, type(template_name)))
        template_info = TCaseTemplateInfo.objects.filter(module_name=template_name).values()

        if template_info:
            try:
                template_id = template_info[0]['case_template_id']
            except IndexError:
                template_id = template_info[0][0]
        else:
            template_id = self._insert_template_table(template_name, module_type, user_name)
            self.insert_template_num += 1
        for row in rows:
            self._insert_case_table(table, row, template_id, module_type, user_name)


    @action(detail=False, methods=['post'], serializer_class=TemplateListSerializer, url_path='check_case_template')
    def check_case_template(self, request, *args, **kwargs):
        """查询模板列表"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TemplateInfoSerializer,
            queryset=TCaseTemplateInfo.objects.all(), url_path='update_template_info/(?P<case_template_id>\d+)')
    def update_template_info(self, request, *args, **kwargs):
        """更新模板信息"""
        return self._handle_update_or_add(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TemplateInfoSerializer,
            queryset=TCaseTemplateInfo.objects.all(), url_path='add_template_info')
    def add_template_info(self, request, *args, **kwargs):
        """新增模板信息"""
        return self._handle_update_or_add(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TemplateInfoSerializer,
            queryset=TCaseTemplateInfo.objects.all(),
            url_path='delete_template_info/(?P<case_template_id>\d+)')
    def delete_template(self, request, *args, **kwargs):
        """删除模板信息"""
        return self._handle_delete(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TemplateBindCaseInfoSerializer,
            url_path='get_template_bind_case')
    def get_template_bind_case(self, request, *args, **kwargs):
        """获取模板以绑定用例和未绑定用例信息"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=TemplateUnBindCaseInfoSerializer,
            url_path='get_template_unbind_case')
    def get_template_unbind_case(self, request, *args, **kwargs):
        """查询未绑定用例信息"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='add_bind_case_list')
    def add_bind_case_list(self, request, **kwargs):
        """
        绑定用例接口
        :param request: 请求request
        :param kwargs:
        :return:
        """
        ret_dict = {
            'status': 0,
            'info': ''
        }
        # 新的绑定用例id列表和对应模板id(必须传)
        bind_case_list = request.data.get('bind_case_list', [])
        case_template_id = request.data.get('case_template_id', '')
        if not case_template_id:
            ret_dict['status'] = 400
            ret_dict['info'] = '需要传递模板id'
        else:
            TemplateBindCaseInfo.objects.add_bind_case_info(bind_case_list, case_template_id)
            ret_dict['info'] = '绑定用例成功！'
        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['post', 'get'], url_path='batch_export_case')
    def batch_export_case(self, request, **kwargs):
        """
        批量配置接口
        :param request: 请求request
        :param kwargs:
        :return:
        """
        # template_id_list 如果为空就是导出所有模板，否则就导出指定模板
        template_id_list = request.data.get('template_id_list', [])
        # product_name 产品线名称必须传
        product_name = request.data.get('product_name', '')

        if not template_id_list:
            template_id_list = TCaseTemplateInfo.objects.get_template_ids(product_name)

        # 获取写入信息
        # 构造sheet:
        # sheet_header 为表列头（第一行）
        # sheet 名称为产品名称， 位置为0
        # 在写入构造好的sheet的时候，传入index作为从第2行开始写入,
        # case_info_list 有多少就写入多少行
        index = 2
        self.deal_excel = DealExcel()
        for template_id in template_id_list:
            template_name, module_type, case_info_list = self._get_export_info(template_id, product_name)
            sheet_header = {
                'A1': '测试模板',
                'B1': '测试用例',
                'C1': '产品名称',
                'D1': '测试用例ID',
                'E1': '测试脚本路径',
                'F1': '预期结果路径'
            }
            sheet = self._get_sheet(product_name, 0, sheet_header)
            index = self._handle_write(sheet, index, template_name, case_info_list, module_type)
        file_name = 'test.xls'
        #TODO self.deal_excel.save(BASE_DIR + '/static/' +file_name)
        # windows: 情况下
        self.deal_excel.save(BASE_DIR + '/static/' +file_name)

        return HttpResponse('./static/' + file_name)

    @action(detail=False, methods=['post'], url_path='batch_delete_case')
    def batch_delete_case(self, request, **kwargs):
        """
        批量删除模板接口
        :param request: 请求request
        :param kwargs:
        :return:
        """
        ret_dict = {
            'status': 0,
            'info': '删除成功！'
        }
        # template_id_list 如果为空就是删除所有模板，否则就删除指定模板
        template_id_list = request.data.get('template_id_list', [])
        # product_name 产品线名称必须传
        product_name = request.data.get('product_name', '')
        if not product_name:
            ret_dict['status'] = 400
            ret_dict['info'] = '请传入产品名称！'
        else:
            # 删除模板表中的数据
            TCaseTemplateInfo.objects.filter(case_template_id__in=template_id_list).delete()
            # 删除桥表中关于模板的数据
            case_bind_info = TemplateBindCaseInfo.objects.filter(case_template_id__in=template_id_list).values()
            case_bind_list = [case['case_id'] for case in case_bind_info]
            TemplateBindCaseInfo.objects.filter(case_template_id__in=template_id_list).delete()
            # 有可能被删除模板下的用例被未删除的其他模板绑定，需要过滤需要删除的用例列表
            other_bind_info = TemplateBindCaseInfo.objects.filter(case_id__in=case_bind_list).values()
            other_bind_list = [other['case_id'] for other in other_bind_info]
            delete_case_list = [case_id for case_id in case_bind_list if case_id not in other_bind_list]
            # 删除用例表中的数据
            TTestCaseInfo.objects.filter(case_id__in=delete_case_list).delete()
            # 删除测试用例绑定测试点表
            TCaseBindPointInfo.objects.filter(case_id__in=delete_case_list).delete()

        return Response(ret_dict, status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'post'], url_path='download_template')
    def download_template(self, request, **kwargs):
        """下载导入模板"""
        file_name = 'case.xlsx'
        self.deal_excel = DealExcel()
        self._get_sheet('导入模板', 0)
        # TODO linux要使用 /
        self.deal_excel.save(BASE_DIR + '/static/' +file_name)

        return HttpResponse('./static/' +file_name)

    @action(detail=False, methods=['post', 'get'], url_path='batch_import_case')
    def batch_import_case(self, request, **kwargs):
        """批量导入功能"""
        ret_dict = {
            'status': 0,
            'info': ''
        }
        FILES = request.FILES['file']
        user_name = request.data.get('user_name', '')
        file = xlrd.open_workbook(file_contents=FILES.read())

        row_list = self._get_row_list(file, 0)
        table = file.sheet_by_index(0)
        for rows in row_list:
            self._insert_table(rows, table, user_name)

        return Response(ret_dict, status.HTTP_200_OK)

    #######################################################################################################
    ###################### 测试用例管理接口 ##################################################################

    @action(detail=False, methods=['post'], serializer_class=CaseListSerializer, url_path='check_case_info')
    def check_case_info(self, request, *args, **kwargs):
        """查询用例列表"""
        return self._handle_get_list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=CaseInfoSerializer,
            queryset=TTestCaseInfo.objects.all(), url_path='update_case_info/(?P<case_id>\d+)')
    def update_case_info(self, request, *args, **kwargs):
        """更新用例信息"""
        return self._handle_update_or_add(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=CaseInfoSerializer,
            queryset=TTestCaseInfo.objects.all(), url_path='add_case_info')
    def add_case_info(self, request, *args, **kwargs):
        """新增用例信息"""
        return self._handle_update_or_add(request, *args, **kwargs)

    @action(detail=False, methods=['post'], serializer_class=CaseInfoSerializer,
            queryset=TTestCaseInfo.objects.all(),
            url_path='delete_case_info/(?P<case_id>\d+)')
    def delete_case_info(self, request, *args, **kwargs):
        """删除用例信息"""
        return self._handle_delete(request, *args, **kwargs)







