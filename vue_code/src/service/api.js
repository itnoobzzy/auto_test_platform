// api.js
import request from '../service/request'

const api = {
  // 量本使用量查询
  query_usedResult (data) {
    return request.post('query_rate_accum_info', data)
  },

  // 数据运营管理接口
  operate_data_api: {
    /***************************运营数据展示接口***********************/
    // 获取产品落地省份列表信息
    get_product_area_list (data) {
      return request.post('operate_data_show/get_product_area_list/', data)
    },
    // 获取运营数据详情
    get_view_info (data) {
      return request.post('operate_data_show/get_view_info/', data)
    },
    // 查看对应省份详情运营数据柱状图
    get_detail_info (data) {
      return request.post('operate_data_show/get_detail_info/', data)
    },
    /*****************************运营数据配置接口*******************/
    // 查询省份参数信息
    get_area_prov_list (data) {
      return request.post('operate_data_config/get_area_prov_list/', data)
    },
    // 查询运营数据配置列表信息
    get_operate_data_info (data) {
      return request.post('operate_data_config/get_operate_data_info/', data)
    },
    // 更新运营数据详情
    update_operate_data_info (data) {
      return request.post('operate_data_config/update_operate_data_info/' + data.id + '/', data)
    },
    // 运营数据收集
    get_prov_operate_data (data) {
      return request.post('operate_data_config/get_prov_operate_data/', data)
    },
    // 增加运营数据详情
    add_operate_data_info (data) {
      return request.post('operate_data_config/add_operate_data_info/', data)
    },
    // 删除运营数据详情
    delete_operate_data_info (data) {
      return request.post('operate_data_config/delete_operate_data_info/', data)
    },
    // 查询运营数据月份
    get_operate_month (data) {
      return request.post('operate_data_config/get_operate_month/', data)
    },
    // 下载批量导入模板
    download_operate_template (data) {
      return request.post('operate_data_config/download_operate_template/', data)
    },
    // 导入运营数据模板
    import_operate_data (data) {
      return request.post('operate_data_config/import_operate_data/', data)
    },
    // 导出运营数据模板
    export_operate_data (data) {
      return request.post('operate_data_config/export_operate_data/', data)
    },
  },
  // 用户登录退出
  login_out_api: {
    // 用户登录
    login (data) {
      return request.post('user/login/', data)
    },
    // 查询角色权限
    query_role_authority (data) {
      return request.post('role/query_role_authority/', data)
    }
  },
  // 系统管理接口
  system_manage_api: {
    // 查询用户菜单信息
    query_user_menu_info (data) {
      return request.post('user/query_user_menu_info/', data)
    },
    // 查询用户角色信息
    query_role_name (data) {
      return request.post('user/query_role_name/', data)
    },
    // 更新用户信息
    update_user_info (data) {
      return request.post('user/update_user_info/', data)
    },
    // 删除用户信息
    del_user_info (data) {
      return request.post('user/del_user_info/', data)
    },
    // 新增用户信息
    add_user_info (data) {
      return request.post('user/', data)
    },
    // 查询菜单信息
    query_menu_info (data) {
      return request.post('user/query_menu_info/', data)
    },
    // 更新角色权限信息
    update_role_authority (data) {
      return request.post('role/update_role_authority/', data)
    },
    // 新增角色
    add_role_authority (data) {
      return request.post('role/add_role_authority/', data)
    },
    // 查询角色id是否存在
    query_role_id(data) {
      return request.post('role/query_role_id/', data)
    },
    // 删除角色
    delete_role_authority (data) {
      return request.post('role/delete_role_authority/', data)
    }
  },
  // 测试配置管理接口
  config_manage_api: {
    // 下载操作手册
    download_operation_manual (data) {
      return request.get('config_manage/download_operation_manual')
    },
    // 需求管理表单回显
    get_require_desc_info (data) {
      return request.post('config_manage/get_require_desc_info/', data)
    },
    // 查询临时表中模板绑定的用例信息
    get_tmp_bind_case (data) {
      return request.post('config_manage/get_tmp_bind_case/', data)
    },
    // 全流程测试临时修改模板绑定用例
    tmp_bind_case_list (data) {
      return request.post('config_manage/tmp_bind_case_list/', data)
    },
    // 查询资费详情
    query_charges_info (data) {
      return request.post('config_manage/query_charges_info/', data)
    },
    // 批量导入模板下载
    download_template (data) {
      return request.get('config_manage/download_template/', data)
    },
    // 查询未绑定的测试用例
    get_template_unbind_case (data) {
      return request.post('config_manage/get_template_unbind_case/', data)
    },


    // 新增测试需求信息
    add_test_require (data) {
      return request.post('config_manage/add_test_require/', data)
    },
    // 全网测试结果
    all_test_result (data) {
      return request.post('config_manage/all_test_result/', data)
    },
    // 查看测试报告
    get_test_report (data) {
      return request.post('config_manage/get_test_report/', data)
    },
    // 人工确认测试结果
    test_author_isfocus (data) {
      return request.post('config_manage/test_author_isfocus/', data)
    },
    // 生成测试报告
    create_report (data) {
      return request.post('config_manage/create_report/', data)
    },
    // 查看账单详情或清单详情
    get_list_fedx (data) {
      return request.post('config_manage/get_list_fedx/', data)
    },
    // 界面跳转使用
    check_test_report (data) {
      return request.post('config_manage/check_test_report/', data)
    },
    // ****************************测试配置管理*************************************
    // 查询测试点
    check_point_info (data) {
      return request.post('config_manage/check_point_info/', data)
    },
    // 预期结果公式参数
    get_formula_info (data) {
      return request.post('config_manage/get_formula_info/', data)
    },
    // 新增/修改测试点
    add_point_info (data) {
      return request.post('config_manage/add_point_info/', data)
    },
    // 删除测试点
    delete_point_info (data) {
      return request.post('config_manage/delete_point_info/', data)
    },
    // 查询测试模板
    check_case_template (data) {
      return request.post('config_manage/check_case_template/', data)
    },
    // 新增测试模板
    add_template_info(data) {
      return request.post('config_manage/add_template_info/', data)
    },
    // 查询测试模板和测试用例绑定关系
    get_template_bind_case (data) {
      return request.post('config_manage/get_template_bind_case/', data)
    },
    // 新增/修改测试模板和测试用例绑定关系
    add_bind_case_list (data) {
      return request.post('config_manage/add_bind_case_list/', data)
    },
    // 删除测试模板
    delete_case_template (data) {
      return request.post('config_manage/delete_template_info/'+data.template_id + '/', data)
    },
    // 查询测试用例
    check_case_info (data) {
      return request.post('config_manage/check_case_info/', data)
    },
    // 新增测试用例
    add_case_info (data) {
      return request.post('config_manage/add_case_info/', data)
    },
    // 修改测试用例
    update_case_info (data) {
      return request.post('config_manage/update_case_info/'+data.case_id + '/', data)
    },
    // 删除测试用例
    delete_case_info (data) {
      return request.post('config_manage/delete_case_info/'+data.case_id + '/', data)
    },
    // 查询多阀值费率
    query_case_rate (data) {
      return request.post('config_manage/query_case_rate/', data)
    },
    // 更新多阀值费率
    update_case_rate (data) {
      return request.post('config_manage/update_case_rate/', data)
    },
    // 批量删除测试用例
    batch_delete_case (data) {
      return request.post('config_manage/batch_delete_case/', data)
    },
    // 一键删除测试用例
    delete_all_case (data) {
      return request.post('config_manage/delete_all_case/', data)
    },
    // 批量导入用例
    batch_import_case (data) {
      return request.post('config_manage/batch_import_case/', data)
    },
    // 批量导出用例
    batch_export_case (data) {
      return request.post('config_manage/batch_export_case/', data)
    },
    // sxdx测试结果管理绑定模板
    get_require_bind_template (data) {
      return request.post('config_manage/get_require_bind_template/', data)
    },
    // sxdx测试编辑需求提交绑定用例
    add_bind_template_list (data) {
      return request.post('config_manage/add_bind_template_list/', data)
    },
    // 主机配置管理
    query_host_data(data) {
      return request.post('config_manage/query_host_data/', data)
    },
    add_host_data(data) {
      return request.post('config_manage/add_host_data/', data)
    },
    delete_host_data(data) {
      return request.post('config_manage/delete_host_data/', data)
    },
    update_host_data(data) {
      return request.post('config_manage/update_host_data/', data)
    },
    // 测试主机连接是否正常
    test_connect (data) {
      return request.post('config_manage/test_host_data/', data)
    },
    // *****************************测试数据管理********************************
    // 查询用户数据
    query_user_data (data) {
      return request.post('config_manage/query_user_data/', data)
    },
    // 编辑用户数据
    update_user_data (data) {
      return request.post('config_manage/update_user_data/', data)
    },
    // 新增用户数据
    add_user_data (data) {
      return request.post('config_manage/add_user_data/', data)
    },
    // 删除用户数据
    delete_user_data (data) {
      return request.post('config_manage/delete_user_data/', data)
    },
    // 查询话单数据
    query_cdr_data (data) {
      return request.post('config_manage/query_cdr_data/', data)
    },
    // 编辑话单数据
    update_cdr_data (data) {
      return request.post('config_manage/update_cdr_data/', data)
    },
    // 新增话单数据
    add_cdr_data (data) {
      return request.post('config_manage/add_cdr_data/', data)
    },
    // 删除话单数据
    delete_cdr_data (data) {
      return request.post('config_manage/delete_cdr_data/', data)
    },
    //*************************单元测试配置********************
    // 增加测试用例
    add_special_case_info(data) {
      return request.post('config_manage/add_special_case_info/', data)
    },
    // 编辑测试用例
    update_special_case_info(data) {
      return request.post('config_manage/update_special_case_info/', data)
    },
    // 查询测试用例
    check_special_case_info(data) {
      return request.post('config_manage/check_special_case_info/', data)
    },
    // 查询测试用例是否存在
    check_special_case_name(data) {
      return request.post('config_manage/check_special_case_name/', data)
    },
    // 容器配置管理
    query_docker_data(data) {
      return request.post('config_manage/query_docker_data/', data)
    },
    add_docker_data(data) {
      return request.post('config_manage/add_docker_data/', data)
    },
    update_docker_data(data) {
      return request.post('config_manage/update_docker_data/', data)
    },
    delete_docker_data(data) {
      return request.post('config_manage/delete_docker_data/', data)
    },
    // 更新容器内代码
    get_docker_data(data) {
      return request.post('paas_manage/get_docker_data/', data)
    }

  },
  // 测试结果管理接口
  result_manage_api: {
    // 查询测试结果信息
    check_test_require (data) {
      return request.post('test_result_manage/check_test_require/', data)
    },
    // 查看结果详情
    query_result_detail(data) {
      return request.post('test_result_manage/query_result_detail/', data)
    },
    // 生成测试报告
    create_report(data) {
      return request.post('test_result_manage/create_report/', data)
    },
    // 删除测试结果信息
    delete_test_result (data) {
      return request.post('test_result_manage/delete_test_result/', data)
    },
  },
  // 全流程测试接口
  whole_process_test: {
    // 查询历史测试记录
    query_history_test(data) {
      return request.post('whole_process_test/query_history_test/', data)
    },
    // 生成测试任务
    create_whole_process_task(data) {
      return request.post('whole_process_test/create_whole_process_task/', data)
    },
    // 查询任务实例信息
    query_instance_info (data) {
      return request.post('whole_process_test/query_instance_info/', data)
    },
    // 开始执行全流程测试任务
    start_paas_task(data) {
      return request.post('whole_process_test/start_paas_task/', data)
    },
  },
  // 全流程测试接口
  whole_test_api: {
    // 全流程测试管理接口：生成测试实例
    whl_create_instance (data) {
      return request.post('test_manage/whl_create_instance/', data)
    },
    // 全流程测试管理接口: 查询测试实例
    whl_query_instance (data) {
      return request.post('test_manage/whl_query_instance/', data)
    },
    // 全流程测试管理接口: 执行测试实例
    whl_execute_test (data) {
      return request.post('test_manage/whl_execute_test/', data)
    },
    // **********************山西电信全流程测试********************************
    // 山西电信输入需求查询已有需求名称
    whl_query_require (data) {
      return request.post('test_manage/whl_query_require/', data)
    },
    create_instance_info (data) {
      return request.post('test_manage/create_instance_info/', data)
    },

  },
  // paas全流程测试
  paas_whole_test_api: {
    // 清理主机环境
    start_init_env_case(data) {
      return request.post('paas_manage/start_init_env_case/', data)
    },
    // 查询需求名称
    select_check_require_name(data) {
      return request.post('paas_manage/select_check_require_name/', data)
    },


    // 人工确认
    paas_task_confirm(data) {
      return request.post('paas_manage/paas_task_confirm/', data)
    },

    // PaaS测试视图
    paas_tree_view(data) {
      return request.post('paas_manage/paas_tree_view/', data)
    },
    select_check_case_code(data) {
      return request.post('paas_manage/select_check_case_code/', data)
    },
    // *********************************单元测试
    // 执行测试任务
    start_paas_special_task(data) {
      return request.post('paas_manage/start_paas_special_task/', data)
    }
  }
}

export default api
