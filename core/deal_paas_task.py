#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : deal_paas_task.py
# @Author: itnoobzzy
# @Date  : 2021/3/22
# @Desc  : 处理paas测试任务
import time, os
import subprocess
import codecs
import configparser

from auto_test_platform.settings import SCRIPT_PATH, RUN_SCRIPT_SHELL
from whole_process_test.models import (
    TResultFileInfo,
    TTestInstanceInfo,
    TTestTaskInfo,
    TTestRequireInfo,
)
from config_manage.models import (
    TTestCaseInfo,
    TCaseTemplateInfo,
    TemplateBindCaseInfo
)
from utils.deal_ssh import SSHConnection
from utils.deal_log import DealLog

log = DealLog()


class DealPaaSTask:
    """
    处理 paas 测试任务
    """

    def __init__(self, request):
        """
        cur_time： 测试开始时间
        product_name：用户所属产品线
        test_flow：测试流程描述
        instance_id：任务实例id
        require_name：测试名称
        host_path：任务执行所在主机环境
        :param request: 请求对象
        """
        self.cur_time = ''
        self.product_name = request.data.get('product_name', '')
        self.test_flow = ''
        self.instance_id = request.data.get('instance_id', '')
        self.require_name = ''
        self.host_path = ''
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        self.ssh = SSHConnection(host=cf.get("ssh_host","host"), username=cf.get("ssh_host","user"), pwd=cf.get("ssh_host","pwd"))

    def _pre_test(self):
        """测试前准备"""
        # 检查测试主机是否存在存放测试脚本的目录
        self.cur_time = time.strftime('%Y/%m', time.localtime(time.time()))
        if not os.path.exists(f'{SCRIPT_PATH}/{self.cur_time}'):
            os.system(f'mkdir -p {SCRIPT_PATH}/{self.cur_time}')
        # 查询出测试需求的名称
        ins_info = TTestInstanceInfo.objects.filter(instance_id=self.instance_id).values()
        for ins in ins_info:
            self.require_name = ins['offer_id']

    def _get_task_info(self):
        """获取任务信息, 并更新任务开始时间"""
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        task_info = TTestTaskInfo.objects.filter(instance_id=self.instance_id).values('task_id', 'case_id')
        TTestInstanceInfo.objects.filter(instance_id=self.instance_id).update(start_time=start_time)

        return task_info

    def _deal_test(self, task_id, test_sh, expect_sh, module_name):
        """
        处理任务测试
        :param task_id: 任务id
        :param test_sh: 测试脚本git路径
        :param expect_sh: 预期结果脚本git路径
        :param module_name: 测试模板名称
        
        out_filename: 测试脚本输出内容文件名
        exp_filename: 预期结果内容文件名
        sh_filename: 测试脚本输出内容文件名
        """
        out_filename = '%s/%s/%s.out' % (SCRIPT_PATH, self.cur_time, task_id)
        exp_filename = '%s/%s/%s.exp' % (SCRIPT_PATH, self.cur_time, task_id)
        sh_filename = '%s/%s/%s.txt' % (SCRIPT_PATH, self.cur_time, task_id)
        # 创建对应任务的空文件
        # 从git克隆获取测试脚本，并复制测试脚本至指定目录
        # 指定获取测试结果文件sh_filename
        # 指定获取预期结果文件exp_filename
        # 指定执行测试脚本结果文件out_filename
        # 执行脚本超时时间为30s
        os.system('touch %s %s %s' % (out_filename, exp_filename, sh_filename))
        timeout = 30
        self._get_test_sh(test_sh, expect_sh, sh_filename, exp_filename)
        self._execute_sh(sh_filename, out_filename, timeout)

        # 比对结果得出测试结论
        result_desc = self._get_test_result(out_filename, exp_filename, module_name)

        self._save_test_result(task_id, out_filename, exp_filename, result_desc)

    def _execute_sh(self, sh_filename, out_filename, timeout):
        """
        执行测试脚本
        :param sh_filename: 测试脚本文件
        :param out_filename: 超时文件
        :param timeout: 超时时间
        :return:
        """
        try:
            p = subprocess.Popen('sh %s %s %s' % (RUN_SCRIPT_SHELL, sh_filename, out_filename), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
            t_beginning = time.time()
            while True:
                if p.poll() is not None:
                    break
                seconds_passed = time.time() - t_beginning
                if timeout and seconds_passed > timeout:
                    p.terminate()
                    raise TimeoutError()
                time.sleep(0.1)
        except Exception:
            log.info('测试脚本%s执行超时' % sh_filename)
            with open(out_filename, 'w') as f:
                f.write("overtime")

    def _get_test_sh(self, test_sh, expect_sh, sh_filename, exp_filename):
        """
        从git上克隆测试脚本并cp到指定目录下
        :param test_sh: 获取实际结果测试脚本路径,master分支test_hello文件夹下的test_hello测试脚本
            git@github.com:itnoobzzy/auto_test_scripts_rep.git@master-test_hello-test_hello.sh
        :param expect_sh: 获取预期结果脚本路径，master分支test_hello文件夹下的expect_hello.sh 预期结果脚本
            git@github.com:itnoobzzy/auto_test_scripts_rep.git@master-test_hello-expect_hello.sh
        :param sh_filename: 测试脚本cp到指定目录下
        :param exp_filename: 预期结果脚本cp到指定目录下
        :return:
        """
        if 'git' in test_sh:
            self._git_clone(test_sh, sh_filename)
            self._git_clone(expect_sh, exp_filename)
            return True
        # TODO: 暂时只支持git管理测试脚本
        else:
            log.info('用例脚本路径配置有误，未检测到git')
            return False

    def _git_clone(self,sh_path , file_name):
        """
        从git上拉去测试脚本并移动到指定目录下
        :param get_path: 脚本对应git路径
            git@github.com:itnoobzzy/auto_test_scripts_rep.git@master-test_hello-test_hello.sh
            @master-test_hello-test_hello.sh (master分支下test_hello文件夹下的test_hello.sh脚本)
        :param file_name: 需要cp至的文件名
        :return:
        """
        # git_path： git路径；branch：分支；rep_name: 仓库名称; dir：文件夹；script_name：脚本文件名称；
        try:
            git_path ='git@' + sh_path.split('@')[1]
            rep_name = sh_path.split('@')[1].split('/')[1].split('.')[0]
            branch = sh_path.split('@')[2].split('-')[0]
            dir = sh_path.split('@')[2].split('-')[1]
            script_name = sh_path.split('@')[2].split('-')[2]
        except Exception as e:
            log.warning(f'测试脚本或预期结果脚本git信息获取失败，请检查用例配置路径是否正确: {e}')
        else:
            try:
                stdout = self.ssh.cmd(f"cd {SCRIPT_PATH};rm -rf {rep_name};git clone {git_path};git checkout {branch}")

            except Exception as e:
                log.warning(f'git脚本拉取失败：{e}')
            else:
                os.system(f"cp {SCRIPT_PATH}/{rep_name}/{dir}/{script_name} {file_name}")

        return file_name

    def _get_test_result(self, out_filename, exp_filename, module_name):
        """
        获取测试脚本执行结果，
        :param out_filename: 测试脚本执行结果文件名
        :param exp_filename: 预期结果文件名
        :param module_name:  模板名称
        :return:
        """
        real_result = codecs.open(out_filename, encoding='gbk', errors='ignore').read()
        expect_result = codecs.open(exp_filename, encoding='gbk', errors='ignore').read()

        if expect_result.replace("\r", "").replace("\n", "") == real_result.replace("\r", "").replace("\n", ""):
            result_desc = '通过'
        else:
            result_desc = '不通过'

        return result_desc

    def _save_test_result(self, task_id, out_filename, exp_filename, result_desc):
        """
        保存该任务测试结果
        :param task_id: 任务id
        :param out_filename: 实际结果文件
        :param exp_filename: 预期结果文件
        :param result_desc:  结果描述
        :return:
        """
        TResultFileInfo.objects.filter(task_id=task_id).delete()
        real_info = TResultFileInfo()
        real_info.task_id = task_id
        real_info.file_type = 'real_result'
        real_info.file_path = out_filename
        real_info.save()

        expect_info = TResultFileInfo()
        expect_info.task_id = task_id
        expect_info.file_type = 'expect_result'
        expect_info.file_path = exp_filename
        expect_info.save()

        expect_info = TResultFileInfo()
        expect_info.task_id = task_id
        expect_info.file_type = 'result_desc'
        expect_info.file_path = result_desc
        expect_info.save()

        TTestTaskInfo.objects.filter(task_id=task_id).update(
            end_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def _get_case_info(self, task):
        """获取任务用例信息"""
        # 测试脚本
        test_sh = ''
        # 预期结果脚本
        expect_sh = ''
        # 用例对应模板id
        case_template_id = ''
        # 模板名称
        module_name = ''

        task_id = task['task_id']
        case_id = task['case_id']
        TTestTaskInfo.objects.filter(task_id=task_id).update(
            begin_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        case_info = TTestCaseInfo.objects.filter(case_id=case_id).values('preset_data', 'input_data')
        for case in case_info:
            test_sh = case['input_data']
            expect_sh = case['preset_data']

        bind_info = TemplateBindCaseInfo.objects.filter(case_id=case_id).values('case_template_id').distinct()
        for bind in bind_info:
            case_template_id = bind['case_template_id']
        template_info = TCaseTemplateInfo.objects.filter(case_template_id=case_template_id).values('module_name')
        for template in template_info:
            module_name = template['module_name']

        return task_id, test_sh, expect_sh, module_name

    def _end_test(self):
        """测试结束，将测试需求状态改为已测试"""
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        TTestRequireInfo.objects.filter(require_name=self.require_name).update(test_status='已测试')
        TTestInstanceInfo.objects.filter(instance_id=self.instance_id).update(end_time=end_time)

    def start_test(self):
        """
        对外提供测试接口
        :return:
        """
        # 测试前准备，检查脚本路径是否存在
        self._pre_test()

        # 获取测试任务信息，多条测试任务，一个用例对应一条任务
        task_info = self._get_task_info()
        for task in task_info:
            # 获取每条任务的用例信息
            task_id, test_sh, expect_sh, module_name = self._get_case_info(task)
            # 处理测试任务
            self._deal_test(task_id, test_sh, expect_sh, module_name)
        # 结束测试
        self._end_test()
