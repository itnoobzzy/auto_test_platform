import Vue from 'vue'
import Router from 'vue-router'

import layout from "../components/common/layout/layout";
import Login from "../components/common/login/login";
// 测试点
import test_point from "../components/common/TestPoint/test_point";
// 测试模板
import test_template from "../components/common/TestCase/test_template";
// 测试用例
import test_case from "../components/common/TestCase/test_case";
// 批量配置
import batch_config from "../components/common/BatchConfig/batch_config";
// 用户管理
import user_manage from "../components/common/UserManage/user_manage";
// 角色管理
import roles_manage from "../components/common/UserManage/roles_manage";
// 用户数据管理
import user_data from "../components/common/UserData/user_data";
// 话单数据管理
import cdr_data from "../components/common/CdrData/cdr_data";
// 全网测试结果
import all_net_test_result from "../components/common/AllNetTestResult/all_net_test_result";
// 运营数据
import operate_data_config from "../components/common/OperateData/operate_data_config";
import show_all_data from "../components/common/OperateData/show_all_data";
import show_operate_data from "../components/common/OperateData/show_operate_data";
// 主机管理
import host_config from "../components/common/HostConfig/host_config";
// 容器配置管理
import container_config from "../components/common/ContainerConfig/container_config";
// sglt
import sglt_DemandTest from "../components/sglt/DemandTest/sglt_DemandTest";
import sglt_process_test from "../components/sglt/WholeTest/sglt_process_test";
// paas
import paas_DemandTest from "../components/paas/DemandTest/paas_DemandTest";
import paas_process_test from "../components/paas/WholeTest/paas_process_test";
import paas_test_view from "../components/paas/TestView/paas_test_view";
import unit_process_test from "../components/paas/Unit_WholeTest/unit_process_test";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Login,
      name: 'login'
    },
    {
      path: '/test_point',
      component: layout,
      meta: {title: '测试点管理'},
      children: [{
        path: '',
        component: test_point,
        name: 'test_point',
        meta: {title: '测试点管理'},
      }]
    },
    {
      path: '/test_template',
      component: layout,
      meta: {title: '测试模板管理'},
      children: [{
        path: '',
        component: test_template,
        name: 'test_template',
        meta: {title: '测试模板管理'},
      }]
    },
    {
      path: '/test_case',
      component: layout,
      meta: {title: '测试用例管理'},
      children: [{
        path: '',
        component: test_case,
        name: 'test_case',
        meta: {title: '测试用例管理'},
      }]
    },
    {
      path: '/batch_config',
      component: layout,
      meta: {title: '批量配置管理'},
      children: [{
        path: '',
        component: batch_config,
        name: 'batch_config',
        meta: {title: '批量配置管理'},
      }]
    },
    {
      path: '/host_config',
      component: layout,
      meta: {title: '主机配置管理'},
      children: [{
        path: '',
        component: host_config,
        name: 'host_config',
        meta: {title: '主机配置管理'},
      }]
    },
    {
      path: '/container_config',
      component: layout,
      meta: {title: '容器配置管理'},
      children: [{
        path: '',
        component: container_config,
        name: 'container_config',
        meta: {title: '容器配置管理'},
      }]
    },
    {
      path: '/user',
      component: layout,
      meta: {title: '用户管理'},
      children: [{
        path: '',
        component: user_manage,
        name: 'user_manage',
        meta: {title: '用户管理'},
      }]
    },
    {
      path: '/role',
      component: layout,
      meta: {title: '角色管理'},
      children: [{
        path: '',
        component: roles_manage,
        name: 'roles_manage',
        meta: {title: '角色管理'},
      }]
    },
    {
      path: '/user_data',
      component: layout,
      meta: {title: '用户数据管理'},
      children: [{
        path: '',
        component: user_data,
        name: 'user_data',
        meta: {title: '用户数据管理'},
      }]
    },
    {
      path: '/cdr_data',
      component: layout,
      meta: {title: '话单数据管理'},
      children: [{
        path: '',
        component: cdr_data,
        name: 'cdr_data',
        meta: {title: '话单数据管理'},
      }]
    },
    // 全网测试结果
    {
      path: '/home',
      component: layout,
      meta: {title: '测试结果详情'},
      children: [{
        path: '/result/all_net_test_result',
        component: all_net_test_result,
        name: 'all_net_test_result',
        meta: {title: '测试结果详情'}
      }]
    },
    // 运营数据配置
    {
      path: '/home',
      component: layout,
      children: [{
        path: '/operate_data_config',
        component: operate_data_config,
        name: 'operate_data_config',
        meta: {title: '运营数据配置'}
      }]
    },
    // 运营数据展示
    {
      path: '/home',
      component: layout,
      children: [{
        path: '/show_operate_data',
        component: show_operate_data,
        name: 'show_operate_data',
        meta: {title: '运营数据展示'}
      },
      {
        path: '/show_operate_data/detail',
        component: show_all_data,
        name: 'show_all_data',
        meta: {title: '运营数据详情'}
      }]
    },
    /********************************sglt***********************/
    {
      path: '/home',
      component: layout,
      meta: {title: '全流程测试'},
      children: [{
        path: '/home/sglt_wholeProcess',
        component: sglt_process_test,
        name: 'sglt_wholeProcess',
        meta: {title: 'SaaS全流程测试'}
      }]
    },
    {
      path: '/home/sglt_DemandUp',
      component: layout,
      meta: {title: '测试结果管理'},
      children: [{
        path: '',
        component: sglt_DemandTest,
        name: 'sglt_DemandTest',
        meta: {title: '测试结果管理'},
      }]
    },
    /********************************paas***********************/
    {
      path: '/home',
      component: layout,
      meta: {title: '全流程测试'},
      children: [{
        path: '/home/paas_wholeProcess',
        component: paas_process_test,
        name: 'paas_wholeProcess',
        meta: {title: 'PaaS全流程测试'}
      }]
    },
    {
      path: '/home',
      component: layout,
      meta: {title: '测试结果管理'},
      children: [{
        path: '/home/paas_DemandUp',
        component: paas_DemandTest,
        name: 'paas_DemandTest',
        meta: {title: '测试结果管理'},
      }]
    },
    {
      path: '/home',
      component: layout,
      meta: {title: '测试视图'},
      children: [{
        path: '/home/paas_test_view',
        component: paas_test_view,
        name: 'paas_test_view',
        meta: {title: '测试视图'},
      }]
    },
    /******************************单元全流程测试*********************************/
    {
      path: '/home',
      component: layout,
      meta: {title: '单元全流程测试'},
      children: [{
        path: '/home/unit_wholeProcess',
        component: unit_process_test,
        name: 'unit_wholeProcess',
        meta: {title: '单元全流程测试'}
      }]
    },

  ]
})
