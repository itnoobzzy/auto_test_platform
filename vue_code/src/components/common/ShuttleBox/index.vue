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
                <el-button type="primary" plain size="small" style="background:none" @click="reset_left_search">重置</el-button>
                <el-button type="primary" size="small" @click="flush_left">查询</el-button>
              </div>
            </div>
            <div class="search_table">
              <el-table :data="unbind_case_table_data" border size='small' style="width: 100%"
                        @selection-change="left_selected">
                <el-table-column type="selection" width="30"></el-table-column>
                <el-table-column prop="case_id" label="测试用例ID" width="100px"></el-table-column>
                <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true"></el-table-column>
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
                <el-button type="primary" plain size="small" style="background:none" @click="right_reset_search">重置</el-button>
                <el-button type="primary" size="small" @click="right_search">查询</el-button>
              </div>
            </div>
            <div class="search_table">
              <div v-if="right_search_flag">
                <el-table
                  :data="search_bind_case_table_data.slice((right_current_page-1)*right_page_size, right_current_page*right_page_size)"
                  border size='small' style="width: 100%" @selection-change="right_selected">
                  <el-table-column type="selection" width="30"></el-table-column>
                  <el-table-column prop="case_id" label="测试用例ID" width="100px"></el-table-column>
                  <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true"></el-table-column>
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
                  <el-table-column prop="case_id" label="测试用例ID" width="100px"></el-table-column>
                  <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true"></el-table-column>
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

<script>
  import {getCookie} from "../../../service/cookie";
  import api from "../../../service/api";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox')
    },
    props: {
      template_id: {
        type: Number,
        default: 0
      },
      // 区分是否为全流程测试绑定模板中的修改绑定用例
      submit_type: {
        type: String,
        default: ''
      }
    },
    data() {
      return {
        id: 0,
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
      // 查询未绑定的用例（左边列表）和已绑定用例（右边列表）
      handle_search() {
        let data = {
          case_template_id: this.id,
          case_name: this.search_input.left_search,
          page: this.left_current_page,
          pageSize: this.left_page_size,
          product_name: getCookie('product_name'),
        };
        api.config_manage_api.get_template_bind_case(data).then(response => {
          if (response.status === 0) {
            this.unbind_case_total_count = response.info.total_count
            this.unbind_case_table_data = response.info.ret_info.unbind_info
            this.bind_case_table_data = response.info.ret_info.bind_info.sort(function (a, b) {
              return b.case_id - a.case_id
            })
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
        this.flush_left()
      },
      left_handle_current_change(val) {
        this.left_current_page = val
        this.flush_left()
      },
      // 重置左边查询
      reset_left_search() {
        this.search_input.left_search = ''
        this.flush_left()
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
      // 刷新左边未绑定用例
      flush_left() {
        let bind_case_id_list = []
        this.bind_case_table_data.forEach(item => {
          bind_case_id_list.push(item.case_id)
        })
        let data = {
          bind_id_list: bind_case_id_list,
          case_name: this.search_input.left_search,
          page: this.left_current_page,
          pageSize: this.left_page_size,
          case_template_id: this.id,
          user_id: getCookie('user_id'),
          product_name: getCookie('product_name')
        }
        api.config_manage_api.get_template_unbind_case(data).then(response => {
          if (response.status === 0) {
            this.unbind_case_total_count = response.info.total_count
            this.unbind_case_table_data = response.info.ret_info.unbind_info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 左边勾选
      left_selected(val) {
        this.left_select_case = val
      },
      // 将左边选中的内容拼接到右边表格中并刷新表格
      handle_bind() {
        this.bind_case_table_data = this.bind_case_table_data.concat(this.left_select_case).sort(function (a, b) {
          return b.case_id - a.case_id
        })
        // 如果右边为查询界面
        if (this.right_search_flag) {
          this.search_bind_case_table_data = this.search_bind_case_table_data.concat(this.left_select_case).sort(function (a, b) {
            return b.case_id - a.case_id
          })
        }
        this.left_current_page = 1
        this.flush_left()
        this.right_handle_current_change(1)
      },
      // 右边勾选
      right_selected(val) {
        this.right_select_case = val
      },
      // 将右边的数组拼接到左边所有列表，并且刷新表格
      handle_unbind() {
        this.remove_right_selected(this.right_select_case)
        this.flush_left()
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
      // 确认
      handle_submit() {
        let bind_list = []
        this.bind_case_table_data.forEach(item => {
          bind_list.push(item.case_id)
        })

        let data = {
          case_template_id: this.id,
          bind_case_list: bind_list,
        }
        // 全流程绑定模板将对应的用例保存至临时表
        if (this.submit_type === 'tem_bind') {
          // 调用父组件的方法将修改后的绑定信息传递过去
          let tmp_bind_list = []
          this.bind_case_table_data.forEach(item => {
            tmp_bind_list.push(item.case_id)
          })
          this.$emit('tmp_save', tmp_bind_list)
        }
        // 用例管理
        else {
          api.config_manage_api.add_bind_case_list(data).then(response => {
            if (response.status === 0) {
              this.$message.success('绑定测试用例成功！')
            }else {
              this.$message.error('系统异常，请联系管理员！')
            }
          })
        }
      }
    },
    watch: {
      template_id: {
        handler(newValue, oldValue) {
          this.id = newValue
          if (newValue !== oldValue && newValue !== 0 && this.submit_type === 'bind_case') {
            this.handle_search()
          }
        },
        immediate: true
      },
    },
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
