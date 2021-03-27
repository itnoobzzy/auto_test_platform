<template>
  <div class="steq_panel_form" style="padding-bottom:108px">
    <AreaTitle title="编辑费率"></AreaTitle>
    <div class="tr mgt-25">
      <el-button type="primary" plain size="small" style="background:none" @click="handle_flush">刷新</el-button>
      <el-button type="primary" size="small" @click="show_null_rate">空值</el-button>
    </div>
    <div class="table">
      <div v-if="show_null_flag">
        <el-table
          :data="null_rate_table_data.slice((null_current_page-1)*null_page_size, null_current_page*null_page_size)"
          border
          ref="selection"
          v-loading="loading"
          style="width: 100%;margin-top:10px"
          element-loading-text="跳转中，请稍等。。。"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)">
          <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true" align="center">
          </el-table-column>
          <el-table-column prop="serv_type" label="业务类型" align="center">
          </el-table-column>
          <el-table-column prop="visit_county" label="漫游国家代码" align="center">
          </el-table-column>
          <el-table-column prop="other_party_head" label="拨打对端国家" align="center">
          </el-table-column>
          <el-table-column prop="rate_threshold" label="套内免费资源" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套内免费资源</span>
              <br>
              <el-button @click.prevent.stop="edit('1')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template slot-scope="scope">
              <el-input clearable size="mini" v-model="scope.row.rate_threshold"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="plan_in_rate" label="套内费率" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套内费率</span>
              <br>
              <el-button @click="edit('2')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template scope="scope">
              <el-input clearable size="mini" v-model="scope.row.plan_in_rate"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit_rate}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="plan_out_rate" label="套外费率" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套外费率</span>
              <br>
              <el-button @click="edit('3')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template scope="scope">
              <el-input clearable size="mini" v-model="scope.row.plan_out_rate"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit_rate}}</span>
            </template>
          </el-table-column>
        </el-table>
        <div class="search_pagination">
          <el-pagination
            @size-change="handle_size_change"
            @current-change="handle_current_change"
            :current-page.sync="null_current_page"
            :page-sizes="[5,10,15]"
            :page-size="null_page_size"
            layout="sizes, prev, pager, next"
            :total="null_rate_table_data.length">
          </el-pagination>
        </div>
      </div>
      <div v-else>
        <el-table
          :data="rate_table_data.slice((current_page-1)*page_size, current_page*page_size)"
          border
          ref="selection"
          v-loading="loading"
          style="width: 100%;margin-top:10px"
          element-loading-text="跳转中，请稍等。。。"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)">
          <el-table-column prop="case_name" label="测试用例名称" :show-overflow-tooltip="true" align="center">
          </el-table-column>
          <el-table-column prop="serv_type" label="业务类型" align="center">
          </el-table-column>
          <el-table-column prop="visit_county" label="漫游国家代码" align="center">
          </el-table-column>
          <el-table-column prop="other_party_head" label="拨打对端国家" align="center">
          </el-table-column>
          <el-table-column prop="rate_threshold" label="套内免费资源" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套内免费资源</span>
              <br>
              <el-button @click.prevent.stop="edit('1')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template slot-scope="scope">
              <el-input clearable size="mini" v-model="scope.row.rate_threshold"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="plan_in_rate" label="套内费率" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套内费率</span>
              <br>
              <el-button @click="edit('2')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template scope="scope">
              <el-input clearable size="mini" v-model="scope.row.plan_in_rate"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit_rate}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="plan_out_rate" label="套外费率" align="center">
            <template slot="header" slot-scope="header_scope">
              <span>套外费率</span>
              <br>
              <el-button @click="edit('3')" type="text" size="mini" icon="el-icon-edit">批量编辑</el-button>
            </template>
            <template scope="scope">
              <el-input clearable size="mini" v-model="scope.row.plan_out_rate"
                        style="width: 100px !important;"></el-input>
              <span style="display: inline-block;  line-height: 31px; font-size: 12px ">{{scope.row.date}}{{scope.row.showUnit_rate}}</span>
            </template>
          </el-table-column>
        </el-table>
        <div class="search_pagination">
          <el-pagination
            @size-change="handle_size_change"
            @current-change="handle_current_change"
            :current-page.sync="current_page"
            :page-sizes="[5,10,15]"
            :page-size="page_size"
            layout="sizes, prev, pager, next"
            :total="rate_table_data.length">
          </el-pagination>
        </div>
      </div>

    </div>

    <Dialog :visible.sync="edit_flag" width="640" :title="'批量修改' + click_name" @closeDialog="edit_flag=false">
      <div slot="con">
        {{ click_name }}:
        <el-input
          placeholder="请输入内容"
          v-model="inner_fee"
          clearable
          style="width:225px"
        ></el-input>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" plain @click="edit_flag = false">取消</el-button>
          <el-button type="primary" @click="pl_ok">确认</el-button>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script>
  import api from "../../../../service/api";
  import {getCookie} from "../../../../service/cookie";
  import {Loading} from 'element-ui';

  export default {
    props: {
      step_two_info: {
        type: Object,
        default: () => {
        }
      },
      step_one_info: {
        type: Object,
        default: () => {
        }
      }
    },
    components: {
      AreaTitle: () => import('@/components/common/AreaTitle'),
      Dialog: () => import('@/components/common/Dialog')
    },
    data() {
      return {
        page_size: 10,
        current_page: 1,
        // 空值table
        null_page_size: 10,
        null_current_page: 1,
        show_null_flag: false,
        null_rate_table_data: [],
        null_rate_index_list: [],
        loading: false,
        // 批量编辑弹窗名
        click_name: '',
        edit_flag: false,
        inner_fee: '',

        loading_create_task: false
      }
    },
    methods: {
      // 分页
      handle_size_change(size) {
        this.show_null_flag === true ? this.null_page_size = size : this.page_size = size
      },
      handle_current_change(val) {
        this.show_null_flag === true ? this.null_current_page = size : this.current_page = val
      },
      // 获取空值table并删除原table中的空值对象
      show_null_rate() {
        this.null_rate_table_data = this.rate_table_data.filter((item) => {
          if (item.plan_in_rate === '' || item.plan_out_rate === '' || item.rate_threshold === '') {
            this.null_rate_index_list.push(item.case_id)
          }
          return item.plan_in_rate === '' || item.plan_out_rate === '' || item.rate_threshold === ''
        })
        this.show_null_flag = true
        this.null_rate_index_list.forEach(case_id => {
          for (let i = 0; i < this.rate_table_data.length; i++) {
            if (this.rate_table_data[i].case_id === case_id) {
              this.rate_table_data.splice(i, 1)
            }
          }
        })
        this.null_rate_index_list = []
      },
      // 刷新表格:合并修改完的null_rate_table_data与删除完空值的rate_table_data
      handle_flush() {
        this.rate_table_data = this.null_rate_table_data.concat(this.rate_table_data)
        this.show_null_flag = false
        this.null_rate_table_data = []
        this.handle_current_change(1)
      },
      // 增加单位
      add_unit() {
        for (let i = 0; i < this.rate_table_data.length; i++) {
          if (this.rate_table_data[i].serv_type === 'voice') {
            this.rate_table_data[i].serv_type = '语音'
            this.rate_table_data[i].showUnit = '分钟'
            this.rate_table_data[i].showUnit_rate = '厘/分钟'
          } else if (this.rate_table_data[i].serv_type === 'data') {
            this.rate_table_data[i].serv_type = '流量'
            this.rate_table_data[i].showUnit = 'KB'
            this.rate_table_data[i].showUnit_rate = '厘/KB'
          } else if (this.rate_table_data[i].serv_type === 'sms') {
            this.rate_table_data[i].serv_type = '短信'
            this.rate_table_data[i].showUnit = '条'
            this.rate_table_data[i].showUnit_rate = '厘/条'
          }
        }
      },
      // 批量编辑
      edit(op) {
        switch (op) {
          case '1':
            this.click_name = '套内免费资源'
            break
          case '2':
            this.click_name = '套内费率'
            break
          case '3':
            this.click_name = '套外费率'
            break
        }
        this.inner_fee = ''
        this.edit_flag = true
      },
      // 编辑完费率后确定
      pl_ok() {
        if (this.show_null_flag === true) {
          for (let i = 0; i < this.null_rate_table_data.length; i++) {
            if (this.click_name === '套内免费资源') {
              this.null_rate_table_data[i].rate_threshold = this.inner_fee
            } else if (this.click_name === '套内费率') {
              this.null_rate_table_data[i].plan_in_rate = this.inner_fee
            } else if (this.click_name === '套外费率') {
              this.null_rate_table_data[i].plan_out_rate = this.inner_fee
            }
          }
        } else {
          for (let i = 0; i < this.rate_table_data.length; i++) {
            if (this.click_name === '套内免费资源') {
              this.rate_table_data[i].rate_threshold = this.inner_fee
            } else if (this.click_name === '套内费率') {
              this.rate_table_data[i].plan_in_rate = this.inner_fee
            } else if (this.click_name === '套外费率') {
              this.rate_table_data[i].plan_out_rate = this.inner_fee
            }
          }
        }
        this.inner_fee = ''
        this.edit_flag = false
      },
      // 更新费率
      update_rate() {
        this.handle_flush()
        for (let i = 0; i < this.rate_table_data.length; i++) {
          if (this.rate_table_data[i].plan_in_rate === '' || this.rate_table_data[i].plan_in_rate === null || this.rate_table_data[i].plan_in_rate === undefined) {
            this.$message.warning('套内费率存在空值，请筛选出空值并修改！')
            return false
          }
          if (this.rate_table_data[i].plan_out_rate === '' || this.rate_table_data[i].plan_out_rate === null || this.rate_table_data[i].plan_out_rate === undefined) {
            this.$message.warning('套外费率存在空值，请筛选出空值并修改！')
            return false
          }
          if (this.rate_table_data[i].rate_threshold === '' || this.rate_table_data[i].rate_threshold === null || this.rate_table_data[i].rate_threshold === undefined) {
            this.$message.warning('套内免费源存在空值，请筛选出空值并修改！')
            return false
          }
        }
        this.loading = true
        let data = {
          test_list: this.rate_table_data
        }
        api.config_manage_api.update_case_rate(data).then(res => {
          this.loading = false
          if (res.status === 0) {
            this.create_test_task()
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 生成测试任务
      create_test_task() {
        let loadingInstance1 = Loading.service({ fullscreen: true })
        let case_id_list = []
        this.rate_table_data.forEach((item) => {
          case_id_list.push(item.case_id)
        })
        let data = {
          user_id: getCookie('user_id'),
          case_id_list: case_id_list,
          offer_id: this.require_info.form.fee_code,
          test_numbers: this.require_info.instance_info.test_numbers
        }
        api.whole_test_api.whl_create_instance(data).then(response => {
          if (response.status === 0) {
            let ret_info = {}
            ret_info.instance_id = response.info.instance_id
            this.$emit('next_step', 'step_three', ret_info)
          } else {
            this.$message.error('生成测试任务失败，请联系系统管理员！')
          }
          loadingInstance1.close()
        })
      },
    },
    computed: {
      rate_table_data: {
        get() {
          return this.step_two_info.rate_info
        },
        set(v) {
          this.step_two_info.rate_info = v
        }
      },
      require_info: function () {
        return this.step_one_info
      },
    },
    mounted() {
      this.add_unit()
    }
  }
</script>
<style lang="scss" scoped>
  .check_box {
    padding: 14px 12px;
    background: #f8f9fc;
    border-radius: 8px;
    margin-top: 12px;
  }
</style>
