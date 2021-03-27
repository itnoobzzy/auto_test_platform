<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="测试模板名称">
            <el-input placeholder="请输入测试模板名称" clearable v-model="search_input.template_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="template_reset_search">重置
            </el-button>
            <el-button type="primary" size="small" @click="template_handle_search">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <div slot="extral">
        <el-button type="primary" size="mini" plain @click="add_template_info">新增</el-button>
      </div>
      <template slot="body">
        <div class="table mgt-10">
          <el-table
            :data="template_table_data"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="module_name" label="测试模板名称"></el-table-column>
            <el-table-column prop="author" label="创建人"></el-table-column>
            <el-table-column prop="create_time" label="创建时间"></el-table-column>
            <el-table-column label="操作" width="270">
              <template slot-scope="scope">
                <el-button size="mini" type="text" @click="bind_case(scope.row.case_template_id)"
                           icon="el-icon-paperclip" style="color: blue">绑定用例
                </el-button>
                <el-button size="mini" type="text" @click="cat_case_detail(scope.row.case_template_id)"
                           icon="el-icon-view">查看详情
                </el-button>
                <el-button @click="delete_template(scope.row)" type="text" size="mini"
                           icon="el-icon-delete"
                           style="color: red"> 移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="template_handle_size_change"
              @current-change="template_handle_current_change"
              :current-page.sync="template_current_page"
              :page-sizes="[5,10,15]"
              :page-size="template_page_size"
              layout="sizes, prev, pager, next"
              :total="template_total_count">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>

    <Dialog :visible="bind_case_flag" width="1028" title="绑定测试用例" @closeDialog="close_bind_case">
      <div slot="con">
        <ShuttleBox v-bind:template_id.sync="template_id" submit_type="bind_case" ref="bind_case"></ShuttleBox>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" plain @click="reset_bind_case">重置</el-button>
          <el-button type="primary" @click="submit_bind_case">确认</el-button>
        </div>
      </div>
    </Dialog>

    <Dialog :visible="cat_case_flag" width="1028" title="绑定用例详情" @closeDialog="close_cat_case">
      <div slot="con">
        <el-row>
          <el-col>
            <div class="search_box">
              <el-input
                placeholder="请输入用例名称"
                suffix-icon="el-icon-search"
                v-model="search_input.cat_case_name"
                style="width:219px"
                size="small">
              </el-input>
              <div class="mgl-30">
                <el-button type="primary" plain size="mini" style="background:none" @click="cat_case_reset">重置
                </el-button>
                <el-button type="primary" size="mini" @click="cat_case_search">查询</el-button>
              </div>
            </div>
            <div class="table mgt-10">
              <el-table
                :data="cat_case_table_data"
                border
                ref="selection"
                style="width: 100%"
                align="center">
                <el-table-column prop="case_name" label="测试用例名称" align="center"></el-table-column>
                <el-table-column prop="test_process" label="测试脚本描述" align="center"></el-table-column>
                <el-table-column prop="preset_data" label="预期结果脚本" align="center"></el-table-column>
                <el-table-column prop="input_data" label="实际结果脚本" align="center"></el-table-column>
              </el-table>
              <div class="search_pagination tr">
                <el-pagination
                  @size-change="cat_case_handle_size_change"
                  @current-change="cat_case_handle_current_change"
                  :current-page.sync="cat_case_current_page"
                  :page-sizes="[5, 10, 15]"
                  :page-size="cat_case_page_size"
                  layout="sizes, prev, pager, next"
                  :total="cat_case_total_count">
                </el-pagination>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </Dialog>


    <Dialog v-bind:visible="edit_template_visible" width="600" @closeDialog="edit_template_visible=false"
            :title="'模板' + edit_template_title">
      <div slot="con">
        <el-form :model="template_form" label-width="140px" :rules="rules" ref="template_form">
          <el-form-item label="模板名称" prop="module_name">
            <el-input
              placeholder="请输入测试模板名称"
              v-model="template_form.module_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" @click="edit_template_submit('template_form')">确认</el-button>
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
      Dialog: () => import('@/components/common/Dialog'),
      ShuttleBox: () => import('@/components/common/ShuttleBox')
    },
    data() {
      return {
        // 查询搜索内容
        search_input: {
          template_name: '',
          case_name: '',
          cat_case_name: ''
        },
        // 测试模板表格
        template_table_data: [],
        template_page_size: 10,
        template_current_page: 1,
        template_total_count: 0,
        // 绑定用例
        bind_case_flag: false,
        template_id: '',
        // 查看用例详情
        cat_case_flag: false,
        cat_case_table_data: [],
        cat_case_page_size: 10,
        cat_case_current_page: 1,
        cat_case_total_count: 0,

        // 编辑模板
        edit_template_title: '',
        edit_template_visible: false,
        template_form: {
          case_template_id: '',
          module_name: ''
        },
        rules: {
          case_name: [{required: true, message: '测试用例名称不能为空', trigger: 'change'}],
          test_process: [{required: true, message: '测试过程不能为空', trigger: 'change'}],
          preset_data: [{required: true, message: '预置结果脚本路径不能为空', trigger: 'change'}],
          input_data: [{required: true, message: '实际结果脚本路径不能为空', trigger: 'change'}],
          module_name: [{required: true, message: '测试模板名称不能为空'}],
        }
      }
    },
    methods: {
      // 测试模板查询
      template_handle_search() {
        let data = {
          page: this.template_current_page,
          pageSize: this.template_page_size,
          module_name: this.search_input.template_name,
          product_name: getCookie('product_name'),
          user_id: getCookie('user_id')
        }
        api.config_manage_api.check_case_template(data).then(response => {
          if (response.status === 0) {
            this.template_table_data = response.info.ret_info
            this.template_total_count = response.info.total_count
          } else {
            let errors = response.errors.non_field_errors
            errors.forEach(item => {
              this.$message.error(item)
            })
          }
        })
      },
      template_reset_search() {
        this.search_input.template_name = ''
        this.template_handle_search()
      },
      // 测试模板分页
      template_handle_current_change(val) {
        this.template_current_page = val
        this.template_handle_search()
      },
      template_handle_size_change(size) {
        this.template_page_size = size
        this.template_handle_search()
      },
      // 删除模板
      delete_template(row) {
        console.log(row)
        this.$confirm('是否确定删除该模板？', '提示', {type: "warning"}).then(_ => {
          let data = {
            template_id: row.case_template_id,
            user_name: getCookie('user_name'),
            module_type: getCookie('product_name')
          }
          api.config_manage_api.delete_case_template(data).then(response => {
            if (response.status === 0) {
              this.$message.success("删除成功")
              this.template_handle_current_change(1)
            } else {
              let errors = response.errors.non_field_errors
              errors.forEach(item => {
                this.$message.error(item)
              })
            }
          })
        })
      },
      // 新增测试模板
      add_template_info() {
        this.edit_template_title = '新增'
        this.case_form.module_name = ''
        this.case_form.case_template_id = ''
        this.edit_template_visible = true
        try {
          this.$refs['template_form'].resetFields()
        }catch (e) {
          console.log('ok')
        }
      },
      // 绑定测试用例
      bind_case(template_id) {
        this.template_id = template_id
        this.bind_case_flag = true
      },
      close_bind_case() {
        this.bind_case_flag = false
      },
      // 绑定测试用例弹窗重置
      reset_bind_case() {
        this.$refs.bind_case.handle_reset()
      },
      // 提交绑定测试用例
      submit_bind_case() {
        this.$refs.bind_case.handle_submit()
        this.bind_case_flag = false
      },
      // 查看测试用例详情
      cat_case_detail(row) {
        this.template_id = row
        this.cat_case_flag = true
        this.cat_case_search()
      },
      // 查看测试用例详情查询
      cat_case_search() {
        let data = {
          template_id: this.template_id,
          page: this.cat_case_current_page,
          pageSize: this.cat_case_page_size,
          case_name: this.search_input.cat_case_name,
          user_id: getCookie('user_id'),
          product_name: getCookie('product_name'),
        }
        api.config_manage_api.check_case_info(data).then(response => {
          if (response.status === 0) {
            this.cat_case_total_count = response.info.total_count
            this.cat_case_table_data = response.info.ret_info
          } else {
            let errors = response.errors.non_field_errors
            errors.forEach(item => {
              this.$message.error(item)
            })
          }
        })
      },
      // 查看用例详情分页
      cat_case_handle_current_change(val) {
        this.cat_case_current_page = val
        this.cat_case_search()
      },
      cat_case_handle_size_change(size) {
        this.cat_case_page_size = size
        this.cat_case_search()
      },
      // 查看测试用例搜索重置
      cat_case_reset() {
        this.search_input.cat_case_name = ''
        this.cat_case_current_page = 1
        this.cat_case_search()
      },

      // 新增模板提交
      edit_template_submit(form_name) {
        this.$refs[form_name].validate((valid) => {
          if (valid) {
            let data = {
              module_name: this.template_form.module_name,
              case_template_id: this.template_form.case_template_id,
              module_type: getCookie('product_name'),
              user_name: getCookie('user_name')
            }
            api.config_manage_api.add_template_info(data).then(response => {
              if (response.status === 0) {
                this.edit_template_visible = false
                this.$message.success('新增模板成功！')
              } else {
                let errors = response.errors.non_field_errors
                errors.forEach(item => {
                  this.$message.error(item)
                })
              }
              this.template_handle_current_change(1)
            })
          }
        })
      },

      // 关闭查看用例详情
      close_cat_case() {
        this.cat_case_flag = false
        this.search_input = {
          template_name: '',
          case_name: '',
          cat_case_name: ''
        }
      }
    },
    mounted() {
      this.template_current_page = 1
      this.template_handle_search()
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
