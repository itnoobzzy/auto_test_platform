<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="测试用例名称">
            <el-input placeholder="请输入测试用例名称" clearable v-model="search_input.case_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="reset_search">重置
            </el-button>
            <el-button type="primary" size="small" @click="handle_search">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <div slot="extral">
        <el-button type="primary" size="mini" plain @click="handle_add">新增</el-button>
      </div>
      <template slot="body">
        <div class="table mgt-10">
          <el-table
            :data="table_data"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="case_name" label="测试用例名称" ></el-table-column>
            <el-table-column prop="test_process" label="测试流程描述" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="preset_data" label="预置数据git路径" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="input_data" label="测试脚本git路径" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="author" label="创建者"></el-table-column>
            <el-table-column prop="test_action" label="所属产品线"></el-table-column>
            <el-table-column prop="create_time" label="创建时间"></el-table-column>
            <el-table-column label="操作" width="270">
              <template slot-scope="scope">
                <el-button size="mini" type="text" @click="handle_edit(scope.row)"
                           icon="el-icon-edit">编辑
                </el-button>
                <el-button @click="handle_delete(scope.row)" type="text" size="mini"
                           icon="el-icon-delete"
                           style="color: red"> 移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handle_size_change"
              @current-change="handle_current_change"
              :current-page.sync="current_change"
              :page-sizes="[5,10,15]"
              :page-size="page_size"
              layout="sizes, prev, pager, next"
              :total="total_count">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>

    <Dialog v-bind:visible="edit_case_visible" width="600" @closeDialog="edit_case_visible=false"
            :title="'用例' + edit_case_title">
      <div slot="con">
        <el-form :model="case_form" label-width="140px" :rules="rules" ref="case_form">
          <el-form-item label="测试用例名称" prop="case_name">
            <el-input
              placeholder="请输入测试用例名称"
              v-model="case_form.case_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试过程描述" prop="test_process">
            <el-input
              placeholder="请输入测试过程"
              v-model="case_form.test_process"
              style="width:225px"
              type="textarea"
            ></el-input>
          </el-form-item>
          <el-form-item label="预置数据脚本" prop="preset_data">
            <el-input
              type="textarea"
              placeholder="获取预置结果的脚本路径"
              v-model="case_form.preset_data"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="实际结果脚本" prop="input_data">
            <el-input
              type="textarea"
              placeholder="获取实际结果的脚本路径"
              v-model="case_form.input_data"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="所属产品线" prop="test_action">
            <el-input
              :disabled="true"
              placeholder="用例所属产品线"
              v-model="case_form.test_action"
              style="width:225px"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" @click="edit_case_submit('case_form')">确认</el-button>
        </div>
      </div>
    </Dialog>

  </div>
</template>

<script>
  import {getCookie} from "../../../service/cookie";
  import api from "../../../service/api";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox'),
      Dialog: () => import('@/components/common/Dialog')
    },
    data() {
      return {
        // 查询搜索内容
        search_input: {
          case_name: '',
        },
        // 测试用例表格
        table_data: [],
        page_size: 10,
        current_change: 1,
        total_count: 0,

        // 编辑用例
        edit_case_title: '',
        edit_case_visible: false,
        case_form: {
          case_id: '',
          case_name: '',
          test_action: '',
          test_process: '',
          preset_data: '',
          input_data: '',
          author: ''
        },

        rules: {
          case_name: [{required: true, message: '测试用例名称不能为空', trigger: 'change'}],
          test_process: [{required: true, message: '测试过程不能为空', trigger: 'change'}],
          preset_data: [{required: true, message: '预置结果脚本路径不能为空', trigger: 'change'}],
          input_data: [{required: true, message: '实际结果脚本路径不能为空', trigger: 'change'}],
        }
      }
    },
    methods: {
      // 测试用例查询
      handle_search() {
        let data = {
          page: this.current_change,
          pageSize: this.page_size,
          case_name: this.search_input.template_name,
          test_action: getCookie('product_name')
        }
        api.config_manage_api.check_case_info(data).then(response => {
          if (response.status === 0) {
            this.table_data = response.info.ret_info
            this.total_count = response.info.total_count
          } else {
            let errors = response.errors.non_field_errors
            errors.forEach(item => {
              this.$message.error(item)
            })
          }
        })
      },
      reset_search() {
        this.search_input.case_name = ''
        this.handle_search()
      },
      // 测试用例分页
      handle_current_change(val) {
        this.current_change = val
        this.handle_search()
      },
      handle_size_change(size) {
        this.page_size = size
        this.handle_search()
      },
      // 删除用例
      handle_delete(row) {
        console.log(row)
        if (row.author !== getCookie('user_name')) {
          this.$message.warning('不能删除他人创建的用例！')
          return false
        }
        this.$confirm('可能存在模板绑定该用例，是否删除？', '提示', {type: "warning"}).then(_ => {
          let data = {
            case_id: row.case_id,
            test_action: getCookie('product_name'),
            author: getCookie('user_name'),
          }
          api.config_manage_api.delete_case_info(data).then(response => {
            if (response.status === 0) {
              this.$message.success('测试用例删除成功！')
              this.handle_current_change(1)
            } else {
              let errors = response.errors.non_field_errors
              errors.forEach(item => {
                this.$message.error(item)
              })
            }
          })
        })
      },

      // 编辑用例
      handle_edit(row) {
        this.edit_case_title = '编辑'
        this.edit_case_visible = true
        this.case_form.case_name = row.case_name
        this.case_form.test_process = row.test_process
        this.case_form.preset_data = row.preset_data
        this.case_form.input_data = row.input_data
        this.case_form.case_id = row.case_id
        this.case_form.test_action = row.test_action
        this.case_form.author = row.author
        this.case_form.case_id = row.case_id
      },
      // 新增用例
      handle_add() {
        this.edit_case_title = '新增'
        this.edit_case_visible = true
        try {
          this.case_form.test_action = getCookie('product_name')
          this.case_form.author = getCookie('user_name')
          this.$refs['case_form'].resetFields()
        }catch (e) {
          this.case_form.case_name = ''
          this.case_form.test_process = ''
          this.case_form.input_data = ''
          this.case_form.input_data = ''
          this.case_form.preset_data = ''
          this.case_form.case_id = ''
        }
      },
      // 编辑用例提交
      edit_case_submit(form_name) {
        this.$refs[form_name].validate((valid) => {
          if (valid) {
            let data = {
              case_id: this.case_form.case_id,
              case_name: this.case_form.case_name,
              test_action: this.case_form.test_action,
              test_process: this.case_form.test_process,
              preset_data: this.case_form.preset_data,
              input_data: this.case_form.input_data,
              author: this.case_form.author
            }
            switch (this.edit_case_title) {
              case "新增":
                api.config_manage_api.add_case_info(data).then(response => {
                  if (response.status === 0) {
                    this.edit_case_visible = false
                    this.$message.success('测试用例新增成功！')
                  } else {
                    let errors = response.errors.non_field_errors
                    errors.forEach(item => {
                      this.$message.error(item)
                    })
                  }
                  this.handle_current_change()
                })
                break;
              case "编辑":
                api.config_manage_api.update_case_info(data).then(response => {
                  if (response.status === 0) {
                    this.edit_case_visible = false
                    this.$message.success('测试用例编辑成功！')
                  } else {
                    let errors = response.errors.non_field_errors
                    errors.forEach(item => {
                      this.$message.error(item)
                    })
                  }
                  this.handle_current_change()
                })
                break;
            }
          }
        })
      },

    },
    mounted() {
      this.current_change = 1
      this.handle_search()
    }
  }
</script>
<style lang="scss" scoped>
  .search_box {
    padding: 20px 0;
    display: flex;
    align-items: center;
  }

  .tips_pos {
    font-size: 14px;
    color: #2e58f7;
    margin-left: 10px;
  }

  .mc_msg {
    padding: 16px;
    position: absolute;
    right: -21vw;
    top: 0;
    z-index: 2099;
    width: 199px;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.15);

    .close {
      color: #ddd;
      position: absolute;
      right: -9.5px;
      top: -9.5px;
      font-size: 20px;
      background: #fff;
      border-radius: 9.5px;
      width: 16px;
      height: 16px;
    }

    &_title {
      font-size: 14px;
      color: #333;
      margin-bottom: 14px;
    }

    p {
      color: #666666;
      font-size: 14px;
      line-height: 1.5;
    }
  }

  .color-zi {
    color: #8b8fff;
    display: inline-block;
    margin-right: 4px;
  }
</style>
