<template>
  <div>
    <el-form
      ref="form"
      :rules="rules"
      :model="form"
      :inline="true"
      label-width="150px"
      class="steq_panel_form">
      <el-row>
        <el-col :span="24" style="text-align: center">
          <el-form-item label="测试名称" prop="require_name">
            <el-input placeholder="请输入测试名称" clearable v-model="form.require_name" size="mini"></el-input>
          </el-form-item>
          <el-form-item label="测试时间">
            <el-date-picker
              v-model="form.test_date"
              align="right"
              type="date"
              size="mini"
              placeholder="选择日期"
              :picker-options="pickerOptions">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="mini" @click="handle_search">查询</el-button>
          </el-form-item>
        </el-col>
        <div style="
            position:fixed;
            border-radius:15px;
            right:10px;
            bottom:50%;
            background:rgba(204,200,255,0.6);
            cursor: pointer;
            writing-mode:tb-rl;">
          <span @click="download_op">&emsp;操作手册下载&emsp;<i class="el-icon-thumb"></i>&emsp; </span>
        </div>
      </el-row>
      <el-row>
        <CardBox title="历史测试结果" height="100%" marginT="20">
          <template slot="body">
            <div class="table mgt-10">
              <el-table
                :data="tableData"
                border
                ref="selection"
                style="width: 100%"
                align="center">
                <el-table-column prop="require_name" label="测试名称"></el-table-column>
                <el-table-column prop="test_man" label="测试人员"></el-table-column>
                <el-table-column prop="test_date" label="测试时间"></el-table-column>
              </el-table>
              <div class="search_pagination tr">
                <el-pagination
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :current-page.sync="currentPage"
                  :page-size="pageSize"
                  :page-sizes="[5,10,15]"
                  layout="sizes, prev, pager, next"
                  :total="total_count">
                </el-pagination>
              </div>
            </div>
          </template>
        </CardBox>
      </el-row>
    </el-form>
  </div>
</template>

<script>
  import {getCookie} from "../../../../service/cookie";
  import api from "../../../../service/api";

  export default {
    components: {
      Dialog: () => import('@/components/common/Dialog'),
      CardBox: () => import('@/components/common/CardBox'),

    },
    data() {
      return {

        // 历史测试结果
        tableData: [],
        currentPage: 1,
        pageSize: 10,
        total_count: 0,

        // 时间选择
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          },
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },

        title: '',
        // 输入需求表单
        form: {
          require_name: '',
          test_date: '',
          user_id: getCookie('user_id')
        },
        rules: {
          require_name: [
            {required: true, message: '请输入测试名称', trigger: 'blur'}
          ]
        },
        instance_info: {
          require_name: ''
        }
      }
    },
    methods: {
      // 分页
      handleSizeChange(size) {
        this.pageSize = size
        this.handle_search()
      },
      handleCurrentChange(val) {
        this.currentPage = val
        this.handle_search()
      },
      // 查询历史测试记录
      handle_search() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            let data = {
              page: this.currentPage,
              pageSize: this.pageSize,
              require_name: this.form.require_name,
              test_date: this.form.test_date,
              product_name: getCookie('product_name')
            }
            api.whole_process_test.query_history_test(data).then(response => {
              if (response.status === 0) {
                this.tableData = response.info.ret_info
                this.total_count = response.info.total_count
              } else {
                this.$message.error('系统异常，请联系管理员！')
              }
            })
          }
        })
      },
      // 校验表单
      confirm_form(form_name) {
        this.$refs[form_name].validate((valid) => {
          if (valid) {
            let ret_info = {}
            this.instance_info.require_name = this.form.require_name
            ret_info.instance_info = this.instance_info
            this.$emit('next_step', 'step_one', ret_info)
          }
        })
      },
      // 操作手册下载
      download_op() {
        api.config_manage_api.download_operation_manual().then(res => {
          window.open(res)
        }).catch(_ => {
          this.$message.error('文档不存在，或有其他错误，请联系管理员处理！！！')
        })
      },
    },
    watch: {
      $route() {
        this.title = this.$route.meta.title
      }
    },
  }
</script>
<style lang="scss" scoped>
  .info {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
  }

  .info th {
    font-size: 15px;
    background-color: #E1FFFF;
    text-align: center;
    padding-left: 10px;
    font-weight: bold;
    border: 1px solid #ddd;
    width: 150px;
  }

  .info tr {
    line-height: 25px;
  }

  .info td {
    background-color: #E1FFFF;
    text-align: center;
    border: 1px solid #ddd;
    padding-left: 10px;
    width: 210px;
  }

  .line_three {
    padding: 18px 10px;

    .info {
      font-size: 14px;
      display: flex;
      align-items: center;

      p {
        margin-right: 40px;
      }
    }

    .info_line {
      margin-top: 8px;
      text-align: center;

      &_item {
        border: 1px solid #e5ecf2;
        border-bottom: none;
        padding: 10px 0;
      }
    }
  }

  .feecontents {
    text-align: center;
    position: absolute;
    width: 122%;
    left: -150px;
  }
</style>
