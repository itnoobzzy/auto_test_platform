from django.db import models
from django.core.paginator import Paginator


class TTestOperateDataInfoQs(models.query.QuerySet):
    """运营数据信息查询集"""

    def get_all_product_info(self, product_name, prov_name):
        """
        获取对应运营省份产品名称的产品信息
        :param product_name: 产品名称
        :param prov_name: 运营省份
        :return:
        """
        info = self.filter(product_name__contains=product_name, prov_name__contains=prov_name).values('product_name', 'prov_name').distinct()
        product_info = [{'product_name': _['product_name'], 'area': _['prov_name']} for _ in info]
        return product_info

    def get_product_name_list(self):
        """获取所有产品名称列表"""
        operate_data = self.filter().values('product_name').distinct()
        product_name_list = [operate['product_name'] for operate in operate_data]
        return product_name_list

    def get_operate_data(self, product_name, *args):
        """
        根据产品名称查询运营数据信息
        :param product_name: 产品名称
        :param args: 返回的产品信息字段
        :return:
        """
        return self.filter(product_name=product_name).values(*args).distinct() or []

    def get_area_prov_info(self, product_name):
        """
        获取对应省份的运营参数信息
        :param product_name:
        :return:
        """
        param_list = []
        prov_data = self.filter(product_name=product_name).values('prov_name').distinct()
        operate_data = self.get_operate_data(product_name, 'operative_index', 'operate_desc',
                                             'operative_sub_index', 'units')

        prov_list = list({operate['prov_name'] for operate in prov_data}) or []

        for operate in operate_data:
            operate_dict = dict()
            operative_index = operate['operative_index']
            operate_desc = operate['operate_desc']
            operative_sub_index = operate['operative_sub_index']
            units = operate['units']

            add_sign = '0'
            for data in param_list:
                if operative_index == data['param_name']:
                    data['subparam_info'].append(
                        {"operative_sub_index": operative_sub_index, "operate_desc": operate_desc, 'units': units})
                    add_sign = '1'

            if add_sign == '0':
                operate_dict['param_name'] = operative_index
                operate_dict['subparam_info'] = [
                    {"operative_sub_index": operative_sub_index, "operate_desc": operate_desc, 'units': units}]
                param_list.append(operate_dict)

        return param_list, prov_list

    def get_operate_data_list_info(self, page, pageSize, **kwargs):
        """获取运营数据列表信息"""
        # 用户所属产品线
        product_name = kwargs.get('product_name', '')
        # 运营省份
        prov_name = kwargs.get('prov_name', '')
        # 月份
        operate_month = kwargs.get('operate_month', '')
        # 运营数据类型
        operative_index = kwargs.get('operative_index', '')

        data_info = self.filter(
            product_name__contains=product_name,
            prov_name__contains=prov_name,
            operate_month__contains=operate_month,
            operative_index__contains=operative_index)

        ptr = Paginator(data_info, pageSize)
        total_count = ptr.count
        data_info = ptr.page(page)
        data_list = []
        for data in data_info:
            data_list.append({"id": data.id,
                              "product_name": data.product_name,
                              "operate_month": data.operate_month,
                              "prov_name": data.prov_name,
                              "prov_type": data.prov_type,
                              "product_ver": data.product_ver,
                              "operative_index": data.operative_index,
                              "operative_sub_index": data.operative_sub_index,
                              "operate_data": data.operate_data,
                              "operate_desc": data.operate_desc,
                              'units': data.units,
                              'target_value': data.target_value,
                              'show_flag': data.show_flag})

        return data_list, total_count

class TTestOperateDataInfo(models.Model):
    """运营数据信息"""
    PROV_TYPE = (
        (1, "PaaS产品"),
        (2, "SaaS产品"),
    )
    product_name = models.CharField(max_length=128, null=False, verbose_name="产品名称", help_text="产品名称")
    operate_month = models.CharField(max_length=10, null=False, verbose_name="数据所属月份", help_text="数据所属月份")
    prov_name = models.CharField(max_length=64, null=False, verbose_name="运营省份", help_text="省份类型")
    prov_type = models.IntegerField(choices=PROV_TYPE, null=False, verbose_name="省份类型", help_text="省份类型")
    operative_index = models.CharField(max_length=64, null=False, verbose_name="展示参数名称", help_text="展示参数名称")
    operative_sub_index = models.CharField(max_length=128, blank=True, null=True, verbose_name="展示子参数名称", help_text="展示子参数名称")
    operate_desc = models.CharField(max_length=256, blank=True, null=True, verbose_name="展示子参数描述", help_text="展示子参数描述")
    operate_data = models.CharField(max_length=64, null=False, verbose_name="展示子参数值", help_text="展示子参数值")
    show_flag = models.CharField(max_length=5, blank=True, null=True, verbose_name="是否展示", help_text="是否展示")
    units = models.CharField(max_length=10, blank=True, null=True, verbose_name="子参数单位", help_text="子参数单位")
    product_ver = models.CharField(max_length=256, blank=True, null=True, verbose_name="产品版本号", help_text="产品版本号")
    target_value = models.CharField(max_length=20, blank=True, null=True, verbose_name="当月目标值", help_text="当月目标值")
    objects = TTestOperateDataInfoQs.as_manager()

    class Meta:
        verbose_name = "运营数据配置信息表"
        verbose_name_plural = "运营数据配置信息表"
        db_table = 't_test_operate_data_info'


class TTestOperateViewInfo(models.Model):
    product_name = models.CharField(max_length=128, null=False, verbose_name="产品名称", help_text="产品名称")
    prov_name = models.CharField(max_length=64, null=False, verbose_name="运营省份", help_text="运营省份")
    prov_type = models.CharField(max_length=64, null=False, verbose_name="省份类型", help_text="省份类型")
    prov_flag = models.CharField(max_length=20, null=False, verbose_name="省份推广状况", help_text="省份推广状况")
    flag_update_time = models.CharField(max_length=20, null=False, verbose_name="更新时间", help_text="省份推广状况更新时间")
    milepost_desc = models.CharField(max_length=1024, blank=True, null=True, verbose_name="里程碑描述", help_text="里程碑描述")
    milepost_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="里程碑日期", help_text="里程碑日期")
    notes = models.CharField(max_length=256, blank=True, null=True, verbose_name="说明", help_text="说明")

    class Meta:
        verbose_name = "运营数据视图信息表"
        verbose_name_plural = "运营数据视图信息表"
        db_table = 't_test_operate_view_info'


class TTestRecordDataInfo(models.Model):
    """
    测试记录信息
    """
    function = models.CharField(max_length=100, null=False)
    desc = models.CharField(max_length=100, null=False)
    cur_month = models.CharField(max_length=30, null=False,  verbose_name="当月测试次数", help_text="当月测试次数")
    use_times = models.CharField(max_length=30, null=False,  verbose_name="接口使用次数", help_text="接口使用次数")

    class Meta:
        verbose_name = "测试次数记录信息表"
        verbose_name_plural = "测试次数记录信息表"
        db_table = 't_test_record_data_info'
