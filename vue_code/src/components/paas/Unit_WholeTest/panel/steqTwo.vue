<template>
  <div>
    <template>
      <div class="steq_panel_form">
        <el-row type="flex" justify="center">
          <el-col>
            <CardBox title="选择测试用例">
              <template slot="body">
                <div class="search_box">
                  <el-input
                    placeholder="请输入用例名称"
                    suffix-icon="el-icon-search"
                    v-model="search_input.left_search"
                    style="width:219px"
                    size="small">
                  </el-input>
                  <div>
                    <el-button type="primary" plain size="mini" style="background:none;float: left"
                               @click="add_test_case">新增
                    </el-button>
                    <el-button type="primary" plain size="mini" style="background:none" @click="reset_left_search">重置
                    </el-button>
                    <el-button type="primary" size="mini" @click="left_handle_current_change(1)">查询</el-button>
                  </div>
                </div>
                <div class="search_table">
                  <el-table :data="unbind_case_table_data" border size='small' style="width: 100%"
                            @selection-change="left_selected"
                            v-loading="loading"
                            element-loading-text="更新中"
                            element-loading-spinner="el-icon-loading"
                            element-loading-background="white">
                    <el-table-column type="selection" width="30"></el-table-column>
                    <el-table-column prop="case_id" label="测试用例ID"></el-table-column>
                    <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true"></el-table-column>
                    <el-table-column prop="preset_data" label="测试容器名称" :show-overflow-tooltip="true"></el-table-column>
                    <el-table-column prop="input_data" label="执行命令" :show-overflow-tooltip="true"></el-table-column>
                    <el-table-column label="操作" width="190">
                      <template slot-scope="scope">
                        <el-button
                          type="text"
                          size="mini"
                          icon="el-icon-edit"
                          @click="handle_edit(scope.row)">
                          编辑
                        </el-button>
                        <el-button type="text" size="mini" icon="el-icon-refresh"
                                   class="my_button"
                                   @click="handle_code_update(scope.row)"
                                   v-loading="loading"
                                   element-loading-text="更新中"
                                   element-loading-spinner="el-icon-loading"
                                   element-loading-background="white">更新代码
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
                <div class="search_pagination">
                  <el-pagination
                    @size-change="left_handle_size_change"
                    @current-change="left_handle_current_change"
                    :current-page.sync="left_current_page"
                    :page-sizes="[5,10,15]"
                    :page-size="left_page_size"
                    layout="sizes, prev, pager, next"
                    :total="unbind_case_total_count">
                  </el-pagination>
                </div>
              </template>
            </CardBox>
          </el-col>
          <el-col :span="2">
            <div class="search_option">
              <el-button type="primary" icon="el-icon-arrow-right" @click="handle_bind"></el-button>
              <el-button icon="el-icon-arrow-left" @click="handle_unbind"></el-button>
            </div>
          </el-col>
          <el-col>
            <CardBox title="确认绑定">
              <template slot="body">
                <div class="search_box">
                  <el-input
                    placeholder="请输入用例名称"
                    suffix-icon="el-icon-search"
                    v-model="search_input.right_search"
                    style="width:219px"
                    size="small">
                  </el-input>
                  <div>
                    <el-button type="primary" plain size="mini" style="background:none" @click="right_reset_search">
                      重置
                    </el-button>
                    <el-button type="primary" size="mini" @click="right_search">查询</el-button>
                  </div>
                </div>
                <div class="search_table">
                  <div v-if="right_search_flag">
                    <el-table
                      :data="search_bind_case_table_data.slice((right_current_page-1)*right_page_size, right_current_page*right_page_size)"
                      border size='small' style="width: 100%" @selection-change="right_selected"
                      v-loading="loading"
                      element-loading-text="更新中"
                      element-loading-spinner="el-icon-loading"
                      element-loading-background="white">
                      <el-table-column type="selection" width="30"></el-table-column>
                      <el-table-column prop="case_id" label="用例ID"></el-table-column>
                      <el-table-column prop="case_name" label="用例名称" :show-overflow-tooltip="true"></el-table-column>
                      <el-table-column prop="preset_data" label="容器名称" :show-overflow-tooltip="true"></el-table-column>
                      <el-table-column prop="input_data" label="执行命令" :show-overflow-tooltip="true"></el-table-column>
                      <el-table-column label="操作" width="190">
                        <template slot-scope="scope">
                          <el-button
                            type="text"
                            size="mini"
                            icon="el-icon-edit"
                            @click="handle_edit(scope.row)">
                            编辑
                          </el-button>
                          <el-button type="text" size="mini" icon="el-icon-refresh"
                                     class="my_button"
                                     @click="handle_code_update(scope.row)">更新代码
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                    <div class="search_pagination">
                      <el-pagination
                        @size-change="right_handle_size_change"
                        @current-change="right_handle_current_change"
                        :current-page.sync="right_current_page"
                        :page-sizes="[5,10,15]"
                        :page-size="right_page_size"
                        layout="sizes, prev, pager, next"
                        :total="search_bind_case_table_data.length">
                      </el-pagination>
                    </div>
                  </div>
                  <div v-else>
                    <el-table
                      :data="bind_case_table_data.slice((right_current_page-1)*right_page_size, right_current_page*right_page_size)"
                      border size='small' style="width: 100%" @selection-change="right_selected">
                      <el-table-column type="selection" width="30"></el-table-column>
                      <el-table-column prop="case_id" label="用例ID"></el-table-column>
                      <el-table-column prop="case_name" label="用例名称" :show-overflow-tooltip="true"></el-table-column>
                      <el-table-column prop="preset_data" label="容器名称" :show-overflow-tooltip="true"></el-table-column>
                      <el-table-column prop="input_data" label="执行命令" :show-overflow-tooltip="true"></el-table-column>
                    </el-table>
                    <div class="search_pagination">
                      <el-pagination
                        @size-change="right_handle_size_change"
                        @current-change="right_handle_current_change"
                        :current-page.sync="right_current_page"
                        :page-sizes="[5,10,15]"
                        :page-size="right_page_size"
                        layout="sizes, prev, pager, next"
                        :total="bind_case_table_data.length">
                      </el-pagination>
                    </div>
                  </div>
                </div>
              </template>
            </CardBox>
          </el-col>
        </el-row>
      </div>
    </template>

    <Dialog v-bind:visible="add_case_visible" width="600" @closeDialog="close_add" title="新增测试用例">
      <div slot="con">
        <el-form :model="case_form" label-width="140px" :rules="rules" ref="case_form" size="mini">
          <el-form-item label="用例名称" prop="case_name">
            <el-input v-model="case_form.case_name" plceholder="请输入用例名称" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="执行命令" prop="input_data">
            <el-input v-model="case_form.input_data" :placeholder="placeholder" style="width: 50%"></el-input>
            <el-tooltip class="item" effect="light" placement="right-start">
              <div slot="content">{{tooltip_content}}<br>{{tooltip_content2}}</div>
              <el-button icon="el-icon-info" size="mini" type="text"></el-button>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="执行容器环境" prop="env_info">
            <el-select v-model="case_form.preset_data" placeholder="请选择用例执行容器环境">
              <el-option
                v-for="item in test_env_list"
                :key="item.id"
                :label="item.image_name"
                :value="item.image_name">
                <span>容器名称：</span>
                <span>{{ item.image_name }}</span>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" @click="handle_submit('case_form')">确认</el-button>
        </div>
      </div>
    </Dialog>

  </div>
</template>

<script>
  import {getCookie} from "../../../../service/cookie";
  import api from "../../../../service/api";
  import {Loading} from "element-ui";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox'),
      Dialog: () => import('@/components/common/Dialog'),
    },
    data() {
      // 动态校验测试名称是否已经存在
      let check_case_name = (result, value, callback) => {
        let data = {
          user_id: getCookie("user_id"),
          case_name: this.case_form.case_name,
          test_type: '单元测试'
        }
        api.config_manage_api.check_special_case_name(data).then(response => {
          if (response.status === 0) {
            if (response.info && this.title==='新增') {
              callback(new Error('该用例名称已存在，请更换！'))
            } else {
              callback()
            }
          }
        })
      }
      return {
        title: '',
        // 新增测试用例
        add_case_visible: false,
        // 编辑测试用例
        test_env_list: [],
        case_form: {
          case_id: '',
          case_name: '',
          input_data: '',
          preset_data: ''
        },
        placeholder: '',
        tooltip_content: '提示',
        tooltip_content2: '',
        rules: {
          case_name: [
            {required: true, message: '请输入用例名称', trigger: 'blur'},
            {validator: check_case_name, trigger: 'change'},
          ],
          input_data: [
            {required: true, message: '请输入测试命令', trigger: 'blur'}
          ]
        },
        // 更新代码
        loading: false,
        //查询
        search_input: {
          left_search: '',
          right_search: ''
        },
        right_search_flag: false,
        // 未绑定用例表格
        unbind_case_table_data: [],
        unbind_case_total_count: 0,
        left_page_size: 10,
        left_current_page: 1,
        left_total_count: 0,
        // 已绑定用例表格
        bind_case_table_data: [],
        search_bind_case_table_data: [],
        right_page_size: 10,
        right_current_page: 1,
        right_total_count: 0,
        // 左边选中列表数据
        left_select_case: [],
        // 右边选中列表数据
        right_select_case: [],
      }
    },
    methods: {
      // 代码更新
      handle_code_update(row) {
        console.log(row)
        this.loading = true
        let data = {
          user_id: getCookie('user_id'),
          image_name: row.preset_data,
          program_dir: row.program_dir,
          local_program_dir: row.local_program_dir,
          vcs_type: row.vcs_type,
          svn_dir: row.svn_dir,
          git_dir: row.git_dir,
          git_branch_name: row.git_branch_name
        }
        api.config_manage_api.get_docker_data(data).then(response => {
          if (response.status === 0) {
            this.$message.success('容器内代码更新成功！')
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.loading = false
        })
      },
      // 查询未绑定的用例（左边列表)
      handle_search() {
        let data = {
          case_name: this.search_input.left_search,
          page: this.left_current_page,
          pageSize: this.left_page_size,
          user_id: getCookie('user_id'),
          test_type: '单元测试'
        };
        api.config_manage_api.check_special_case_info(data).then(response => {
          if (response.status === 0) {
            this.unbind_case_total_count = response.total_count
            this.unbind_case_table_data = response.info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        });
      },
      // 分页
      right_handle_size_change(size) {
        this.right_page_size = size
      },
      right_handle_current_change(val) {
        this.right_current_page = val
      },
      left_handle_size_change(size) {
        this.left_page_size = size
        this.handle_search()
      },
      left_handle_current_change(val) {
        this.left_current_page = val
        this.handle_search()
      },
      // 重置左边查询
      reset_left_search() {
        this.search_input.left_search = ''
        this.left_handle_current_change(1)
      },
      // 右边查询
      right_search() {
        this.search_bind_case_table_data = []
        this.bind_case_table_data.forEach(item => {
          if (item.case_name.indexOf(this.search_input.right_search) > -1) {
            this.search_bind_case_table_data.push(item)
          }
        })
        this.right_current_page = 1
        this.right_search_flag = true
      },
      // 右边重置
      right_reset_search() {
        this.right_search_flag = false
        this.search_bind_case_table_data = []
        this.search_input.right_search = ''
        this.right_current_page = 1
      },
      // 左边勾选
      left_selected(val) {
        this.left_select_case = val
      },
      // 将左边选中的内容拼接到右边表格中并刷新表格
      handle_bind() {
        // 过滤已绑定的用例
        let bind_case_id_list = []
        this.bind_case_table_data.forEach(item => {
          bind_case_id_list.push(item.case_id)
        })
        let tmp_list = this.left_select_case.filter(item => {
          return bind_case_id_list.indexOf(item.case_id) < 0
        })

        this.bind_case_table_data = this.bind_case_table_data.concat(tmp_list).sort(function (a, b) {
          return b.case_id - a.case_id
        })
        // 如果右边为查询界面
        let search_bind_case_id_list = []
        this.search_bind_case_table_data.forEach(item => {
          search_bind_case_id_list.push(item.case_id)
        })
        let tmp_list2 = this.left_select_case.filter(item => {
          return search_bind_case_id_list.indexOf(item.case_id) < 0
        })
        if (this.right_search_flag) {
          this.search_bind_case_table_data = this.search_bind_case_table_data.concat(tmp_list2).sort(function (a, b) {
            return b.case_id - a.case_id
          })
        }
        this.right_handle_current_change(1)
      },
      // 生成测试任务
      create_test_task(require_name) {
        let id_list = []
        this.bind_case_table_data.forEach(item => {
          id_list.push(item.case_id)
        })
        console.log('case_id_list', id_list)
        let loadingInstance1 = Loading.service({fullscreen: true})
        let data = {
          product_name: getCookie('product_name'),
          user_name: getCookie('user_name'),
          id_list: id_list,
          require_name: require_name
        }
        api.whole_process_test.create_whole_process_task(data).then(response => {
          if (response.status === 0) {
            let ret_info = {}
            ret_info.instance_id = response.info.instance_id
            ret_info.info = response.info
            this.$emit('next_step', 'step_two', ret_info)
          } else {
            this.$message.error('生成测试任务失败，请联系系统管理员！')
          }
          loadingInstance1.close()
        })
      },
      // 右边勾选
      right_selected(val) {
        this.right_select_case = val
      },
      // 移除选中绑定用例并刷新右边表格
      handle_unbind() {
        this.remove_right_selected(this.right_select_case)
        this.right_handle_current_change(1)
      },
      // 删除右边选中的数组
      remove_right_selected(right_selected) {
        Array.prototype.diff = function (array) {
          return this.filter(function (i) {
            return array.indexOf(i) < 0
          })
        }
        this.bind_case_table_data = this.bind_case_table_data.diff(right_selected)
        // 如果右边为查询的内容，同时删除查询数组中对应的元素
        if (this.right_search_flag) {
          this.search_bind_case_table_data = this.bind_case_table_data.diff(right_selected)
        }
      },
      // 单元全流程测试新增测试用例
      add_test_case() {
        this.title = '新增'
        this.case_form = {
          case_id: '',
          case_name: '',
          preset_data: '',
          input_data: ''
        }
        this.add_case_visible = true
      },
      // 编辑用例
      handle_edit(row) {
        this.title = '编辑'
        this.case_form = {
          case_id: row.case_id,
          case_name: row.case_name,
          preset_data: row.preset_data,
          input_data: row.input_data
        }
        console.log(row)
        console.log(this.case_form)
        this.add_case_visible = true
      },
      close_add() {
        this.$refs['case_form'].resetFields()
        this.add_case_visible = false
      },
      // 编辑用例提交
      handle_submit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let data = {
              case_id: this.case_form.case_id,
              case_name: this.case_form.case_name,
              input_data: this.case_form.input_data,
              user_id: getCookie('user_id'),
              test_type: '单元测试',
              preset_data: this.case_form.preset_data
            }
            switch (this.title) {
              case "新增":
                api.config_manage_api.add_special_case_info(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success('增加成功！')
                    this.left_handle_current_change(1)
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                  }
                })
                break
              case "编辑":
                api.config_manage_api.update_special_case_info(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success('编辑成功！')
                    this.left_handle_current_change(1)
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                  }
                })
                break
            }
            this.add_case_visible = false
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      // 查询容器环境列表
      get_test_env_list() {
        let data = {
          user_id: getCookie('user_id')
        };
        api.config_manage_api.query_docker_data(data).then(response => {
          if (response.status === 0) {
            this.test_env_list = response.info
          } else {
            this.$message.error('查询容器环境列表失败！')
          }
        });
      }
    },
    mounted() {
      this.left_handle_current_change(1)
      this.get_test_env_list()
    }
  }
</script>

<style lang="scss" scoped>
  .search_box {
    padding: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .search_option {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;

    button {
      width: 30px;
      height: 30px;
      padding: 0;
      margin-left: 0;
      margin-bottom: 5px;
    }
  }
</style>
<style lang="scss">
  .search_table {
    .el-table--border th,
    .el-table--border td {
      border-right: none !important
    }

    .el-table .cell {
      padding: 0 0 0 10px;
    }

    .el-table th .cell {
      font-size: 14px;
      color: #666666;
    }

    .el-table td .cell {
      font-size: 13px;
      color: #333333;
    }
  }
</style>
