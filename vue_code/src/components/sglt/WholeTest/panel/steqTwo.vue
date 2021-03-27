<template>
  <div>
    <template>
      <div class="steq_panel_form">
        <el-row type="flex" justify="center">
          <el-col>
            <CardBox title="选择测试模板">
              <template slot="body">
                <div class="search_box">
                  <el-input
                    placeholder="请输入模板名称"
                    suffix-icon="el-icon-search"
                    v-model="search_input.left_search"
                    style="width:219px"
                    size="small">
                  </el-input>
                  <div>
                    <el-button type="primary" plain size="small" style="background:none" @click="reset_left_search">重置</el-button>
                    <el-button type="primary" size="small" @click="left_handle_current_change(1)">查询</el-button>
                  </div>
                </div>
                <div class="search_table">
                  <el-table :data="unbind_template_table_data"
                            border size='small'
                            style="width: 100%"
                            v-loading="loading_query_rate"
                            element-loading-text="跳转中，请稍等。。。"
                            element-loading-spinner="el-icon-loading"
                            v-loading.fullscreen.lock="loading_query_rate"
                            element-loading-background="rgba(0, 0, 0, 0.8)"
                            @selection-change="left_selected">
                    <el-table-column type="selection" width="30"></el-table-column>
                    <el-table-column prop="case_template_id" label="测试模板ID" width="100"></el-table-column>
                    <el-table-column prop="module_name" label="测试模板名称" :show-overflow-tooltip="true"></el-table-column>
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
                    :total="unbind_template_total_count">
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
                    placeholder="请输入模板名称"
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
                      :data="search_bind_template_table_data.slice((right_current_page-1)*right_page_size, right_current_page*right_page_size)"
                      border size='small' style="width: 100%" @selection-change="right_selected">
                      <el-table-column type="selection" width="30"></el-table-column>
                      <el-table-column prop="case_template_id" label="测试模板ID" width="100"></el-table-column>
                      <el-table-column prop="module_name" label="测试模板名称" :show-overflow-tooltip="true"></el-table-column>
                    </el-table>
                    <div class="search_pagination">
                      <el-pagination
                        @size-change="right_handle_size_change"
                        @current-change="right_handle_current_change"
                        :current-page.sync="right_current_page"
                        :page-sizes="[5,10,15]"
                        :page-size="right_page_size"
                        layout="sizes, prev, pager, next"
                        :total="search_bind_template_table_data.length">
                      </el-pagination>
                    </div>
                  </div>
                  <div v-else>
                    <el-table
                      :data="bind_template_table_data.slice((right_current_page-1)*right_page_size, right_current_page*right_page_size)"
                      border size='small' style="width: 100%" @selection-change="right_selected">
                      <el-table-column type="selection" width="30"></el-table-column>
                      <el-table-column prop="case_template_id" label="测试模板ID" width="100"></el-table-column>
                      <el-table-column prop="module_name" label="测试模板名称" :show-overflow-tooltip="true"></el-table-column>
                    </el-table>
                    <div class="search_pagination">
                      <el-pagination
                        @size-change="right_handle_size_change"
                        @current-change="right_handle_current_change"
                        :current-page.sync="right_current_page"
                        :page-sizes="[5,10,15]"
                        :page-size="right_page_size"
                        layout="sizes, prev, pager, next"
                        :total="bind_template_table_data.length">
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
  </div>
</template>

<script>
import {getCookie} from "../../../../service/cookie";
import api from "../../../../service/api";

export default {
  components: {
    CardBox: () => import('@/components/common/CardBox')
  },
  data () {
    return {
      loading_query_rate: false,
      // 等待2秒等待费率查询完毕
      timer: '',
      //查询
      search_input: {
        left_search: '',
        right_search: ''
      },
      right_search_flag: false,
      // 未绑定模板表格
      unbind_template_table_data: [],
      unbind_template_total_count: 0,
      left_page_size: 10,
      left_current_page: 1,
      left_total_count: 0,
      // 已绑定模板表格
      bind_template_table_data: [],
      search_bind_template_table_data: [],
      right_page_size: 10,
      right_current_page: 1,
      right_total_count: 0,
      // 左边选中列表数据
      left_select_template: [],
      // 右边选中列表数据
      right_select_case: [],
      // 绑定模板信息
      bind_template_info: [],
      // 确保所有模板都已查询完毕
      next_step_flag: false,
    }
  },
  methods: {
    // 查询未绑定的模板（左边列表)
    handle_search() {
      let data = {
        module_name: this.search_input.left_search,
        page: this.left_current_page,
        pageSize: this.left_page_size,
        user_id: getCookie('user_id')
      };
      api.config_manage_api.check_case_template(data).then(response => {
        if (response.status === 0) {
          this.unbind_template_total_count = response.total_count
          this.unbind_template_table_data = response.info
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
      this.search_bind_template_table_data = []
      this.bind_template_table_data.forEach(item => {
        if (item.module_name.indexOf(this.search_input.right_search) > -1) {
          this.search_bind_template_table_data.push(item)
        }
      })
      this.right_current_page = 1
      this.right_search_flag = true
    },
    // 右边重置
    right_reset_search() {
      this.right_search_flag = false
      this.search_bind_template_table_data = []
      this.search_input.right_search = ''
      this.right_current_page = 1
    },
    // 左边勾选
    left_selected(val) {
      this.left_select_template = val
    },
    // 将左边选中的内容拼接到右边表格中并刷新表格
    handle_bind() {
      let bind_id_list = []
      this.bind_template_table_data.forEach(item => {
        bind_id_list.push(item.case_template_id)
      })
      let tmp_list = this.left_select_template.filter(item => {
        return bind_id_list.indexOf(item.case_template_id) < 0
      })
      this.bind_template_table_data = this.bind_template_table_data.concat(tmp_list).sort(function (a, b) {
        return b.case_template_id - a.case_template_id
      })
      // 如果右边为查询界面
      let search_bind_id_list = []
      this.search_bind_template_table_data.forEach(item => {
        search_bind_id_list.push(item.case_template_id)
      })
      let tmp_list2 = this.left_select_template.filter(item => {
        return search_bind_id_list.indexOf(item.case_template_id) < 0
      })
      if (this.right_search_flag) {
        this.search_bind_template_table_data = this.search_bind_template_table_data.concat(tmp_list2).sort(function (a, b) {
          return b.template_id - a.template_id
        })
      }
      // this.left_current_page = 1
      this.right_handle_current_change(1)
      // 查询对应模板id下的绑定的用例信息
      let template_id_list = []
      this.bind_template_table_data.forEach(item => {
        template_id_list.push(item.case_template_id)
      })
      this.get_case_id_list(template_id_list)
    },

    // 查询对应模板id下绑定的用例信息
    get_case_id_list(id_list) {
      for (let i = 0, len = id_list.length; i < len; i++) {
        let push_flag = this.bind_template_info.find(item => {
          return item.template_id === id_list[i]
        })
        if (push_flag === undefined) {
          let case_id_list = []
          let data = {
            case_template_id: id_list[i],
            page: 1,
            pageSize: 3,
            user_id: getCookie('user_id'),
          }
          api.config_manage_api.get_template_bind_case(data).then(response => {
            if (response.status === 0) {
              response.info.bind_info.forEach(item => {
                case_id_list.push(item.case_id)
              })
              this.bind_template_info.push({
                'template_id': id_list[i],
                'case_id_list': case_id_list
              })
            }
            console.log(this.bind_template_info.length - 1, i)
            if (this.bind_template_info.length - 1 === i) {
              this.next_step_flag = true
            }
          });
        }
      }
    },

    // 查询用例下的费率
    get_case_rate(offer_id) {
      this.loading_query_rate = true
      this.timer = setInterval(() => {
        console.log(this.next_step_flag)
        if (this.next_step_flag) {
          clearInterval(this.timer)
        }
      }, 1000)
      if (this.next_step_flag === true) {
        let data = {
          offer_id: offer_id,
          bind_template_info: this.bind_template_info,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.query_case_rate(data).then(response => {
          if (response.status === 0) {
            let ret_info = {}
            ret_info.rate_info = response.info
            this.$emit('next_step', 'step_two', ret_info)
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.loading_query_rate = false
        })
      }
    },

    // 右边勾选
    right_selected(val) {
      this.right_select_case = val
    },
    // 移除选中绑定模板并刷新右边表格
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
      this.bind_template_table_data = this.bind_template_table_data.diff(right_selected)
      // 如果右边为查询的内容，同时删除查询数组中对应的元素
      if (this.right_search_flag) {
        this.search_bind_template_table_data = this.bind_template_table_data.diff(right_selected)
      }
      // 同时删除bind_template_info中对应的
      right_selected.forEach(item => {
        let _index = this.bind_template_info.findIndex(function (i) {
          return i.template_id === item.case_template_id
        })
        this.bind_template_info.splice(_index, 1)
      })
    },

  },
  mounted() {
    this.left_handle_current_change(1)
  },
  beforeDestroy() {
    clearInterval(this.timer)
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
