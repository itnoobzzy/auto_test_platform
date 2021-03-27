<template>
  <div class="steq_panel_form" style="padding-bottom:50px">
    <el-row>
      <el-col :span="4">
        <AreaTitle title="测试任务编辑"></AreaTitle>
      </el-col>
      <el-col :span="10">
        <el-button type="primary"
                   style="margin: auto"
                   size="mini"
                   v-if="result_flag === false"
                   @click="start"
                   :disabled="execute_flag"
                   :title="execute_title">{{ execute_title }}
        </el-button>
        <el-button type="primary" size="mini" v-if="result_flag" @click="look_result">查看结果</el-button>
        <el-button type="primary" size="mini" @click="return_first_step" title="点击返回第一步">返回首页</el-button>
      </el-col>
    </el-row>
    <ul class="three_ul">
      <li>当前状态：{{ test_status }}</li>
      <li>已完成数：{{ finish_count }}</li>
      <li>未完成数：{{ executing_count }}</li>
    </ul>
    <div class="table">
      <el-table
        :data="tableData"
        v-loading="loading"
        element-loading-text="查询测试任务中，请稍后。。。"
        element-loading-spinner="el-icon-loading"
        element-loading-background="white"
        border
        max-height="400"
        ref="selection"
        style="width: 100%">
        <el-table-column align="center" prop="task_id" label="任务ID">
        </el-table-column>
        <el-table-column align="center" prop="test_action" label="用例ID">
        </el-table-column>
        <el-table-column align="center" prop="test_name" label="用例名称" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column align="center" prop="expect_info" label="预期和实际结果详情" :show-overflow-tooltip="true">
          <template slot-scope="scope">
            <el-tooltip class="item" effect="light" placement="right-start">
              <div slot="content" style="width: 600px">
                <div class="div-a">
                  <h2 style="text-align: center;color: blue;">预期结果</h2><br>
                  <span class="ex_cell">{{scope.row.expect_result}}</span>
                </div>
                <div class="div-b">
                  <h2 style="text-align: center;color: blue;">实际结果</h2><br>
                  <span class="ex_cell">{{scope.row.really_result}}</span>
                </div>
              </div>
              <el-button type="text" v-show="scope.row.diff_result">查看详情</el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="test_status" label="测试状态" :show-overflow-tooltip="true" align="center"></el-table-column>
        <el-table-column prop="diff_result" sortable width="125" label="是否通过" align="center"
                         :show-overflow-tooltip="true"></el-table-column>
        <el-table-column label="人工确认" align="center" :show-overflow-tooltip="true">
          <template slot-scope="scope">
            <el-radio v-if="test_status === '测试完成'" @change="pass_is(scope.$index,scope.row)"
                      v-model="scope.row.diff_result" v-for="item in pass_list" :label="item"
                      :value="item"></el-radio>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <Dialog v-bind:visible="show_result" width="1000" @closeDialog="show_result=false" title="结果详情">
      <div slot="con">
        <table class="info" style="background: #fff; height: 3rem; position: relative; bottom: 2rem" id="TableA">
          <tr>
            <th>需求名称</th>
            <td align="center" style="color: blue">
              <el-tooltip class="item" effect="dark" content="点击查看所有" placement="top-start">
                <el-button type="text" @click="filter_result('')">{{ require_name }}</el-button>
              </el-tooltip>
            </td>
            <th>通过个数</th>
            <td align="center" style="color: blue">
              <el-tooltip class="item" effect="dark" content="点击查看通过用例" placement="top-start">
                <el-button type="text" @click="filter_result('通过')">{{ result_paas }}</el-button>
              </el-tooltip>
            </td>
            <th>未通过个数</th>
            <td align="center">
              <el-tooltip class="item" effect="dark" content="点击查看未通过用例" placement="top-start">
                <el-button type="text" style="color: red" @click="filter_result('不通过')">{{ result_not_paas }}
                </el-button>
              </el-tooltip>
            </td>
            <th>操作</th>
            <td align="center" style="color: blue">
              <el-button @click="report_create" type="primary" icon="el-icon-document" size="mini"
                         :loading="rc_loading">生成报告
              </el-button>
            </td>
          </tr>
        </table>
        <el-table :data="result_table" border :header-cell-style="{background:'#5fb3f4',color:'white'}"
                  style="width: 100%; position: relative; bottom: 2rem" height="34rem">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="form_style">
                <el-form-item label="测试任务ID：">
                  <span>{{ props.row.task_id }}</span>
                </el-form-item>
                <br>
                <el-form-item label="测试用例名称：">
                  <span>{{ props.row.test_name }}</span>
                </el-form-item>
                <br>
                <el-form-item label="预期结果：">
                  <span>{{ props.row.expect_result }}</span>
                </el-form-item>
                <br>
                <el-form-item label="实际结果：">
                  <span>{{ props.row.real_result }}</span>
                </el-form-item>
                <br>
                <el-form-item label="是否通过：">
                  <span>{{ props.row.result_desc }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop="task_id" width="100" label="测试任务ID" align="center"
                           :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="test_name" width="120" label="测试用例名称" align="center"
                           :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="expect_result" width="300" label="预期结果"
                           :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="real_result" width="300" label="实际结果" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="result_desc" label="是否通过" align="center"
                           :show-overflow-tooltip="true"></el-table-column>
        </el-table>
        <div class="search_pagination tr">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="result_table_currentPage"
            :page-size="result_table_pageSize"
            :page-sizes="[5,10,15]"
            layout="sizes, prev, pager, next"
            :total="result_table_count">
          </el-pagination>
        </div>
      </div>
    </Dialog>

  </div>
</template>

<script>
  import api from "../../../../service/api";
  import {getCookie} from "../../../../service/cookie";

  export default {
    props: {
      step_one_info: {
        type: Object,
        default: () => {
        }
      },
      step_two_info: {
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
        loading: true,
        tableData: [],
        socket: '',
        execute_flag: false,
        execute_title: '开始执行',
        result_flag: false,
        test_status: "未提取到数据",

        finish_count: 0,
        executing_count: 0,

        result_paas: 0,
        result_not_paas: 0,
        rc_loading: false,
        result_type: '',
        pass_list: ["通过", "不通过"],

        show_result: false,
        result_table: [],
        result_table_pageSize: 10,
        result_table_currentPage: 1,
        result_table_count: 0,
      }
    },
    methods: {
      // websocket连接
      con_websocket(instance_id) {
        let ws = new WebSocket(
          // TODO: 部署至服务器的时候需要切换注释
          'ws://' + window.location.host + '/ws/query_status'
          // 'ws://' + '39.101.178.163:8000' + '/ws/query_status'
        )
        // ws.send(instance_id)
        console.log(ws)
        this.socket = ws
        ws.onmessage = function (e) {
          let data = JSON.parse(e.data)
          let message = data['message']
          console.log('message', message)
          func1(message)
        }
        ws.onclose = function (e) {
          console.log('websocket closed！\n',e)
          check_close_state()
        }
        ws.onopen = function (e) {
          console.log('success')
          ws.send(instance_id)
        }
        // 判断是否为全流程测试界面
        let check_route_func = function() {
          console.log('route', this.$route)
          if (this.test_status === '未完成' && this.$route.path === '/home/PaaS_wholeProcess') {
            console.log('websocket重连')
            this.con_websocket(instance_id)
          }
        }
        let check_route =  check_route_func.bind(this)
        // 动态刷新测试任务状态
        let func2 = function(message) {
          this.finish_count = message.finish_count
          this.executing_count = message.executing_count
          this.tableData = message.info
          this.test_status = message.test_status
          if (this.test_status === '未完成') {
            this.$message.info('测试中，请等候！')
          }
          else if (this.test_status === '测试完成') {
            this.$message.success('测试完成！')
            ws.close()
            this.result_flag = true
          }
        }
        let func1 = func2.bind(this)
        // 判断是否正常断开
        let check_close_state = function() {
          check_route()
        }

      },
      // 开始执行
      start() {
        this.execute_flag = true
        this.execute_title = '执行中...'
        this.con_websocket(this.instance_id)
        let data = {
          instance_id: this.instance_id,
          user_id: getCookie('user_id')
        }
        api.whole_process_test.start_paas_task(data).then(res => {
          if (res.status === 500) {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      report_create() {
        this.rc_loading = true
        let data = {
          info: this.result_table,
          user_id: getCookie('user_id'),
        }
        api.config_manage_api.create_report(data).then(response => {
          this.rc_loading = false
          this.$message.success('生成成功！！！')
          window.open(response);
        })
      },
      look_result() {
        this.result_type = ''
        this.handle_search()
      },
      // 条件过滤结果
      filter_result(result_type) {
        this.result_type = result_type
        let data = {
          page: 1,
          pageSize: 10,
          require_name: this.require_name,
          result_type: result_type,
          product_name: getCookie('product_name')
        }
        api.result_manage_api.query_result_detail(data).then(response => {
          if (response.status === 0) {
            this.result_table = response.info
            this.result_table_count = response.total_count
          }
        })
      },
      handleSizeChange(size) {
        this.result_table_pageSize = size
        this.handle_search()
      },
      handleCurrentChange(val) {
        this.result_table_currentPage = val
        this.handle_search()
      },
      handle_search() {
        this.show_result = true
        this.result_paas = 0
        this.result_not_paas = 0
        let data = {
          pageSize: this.result_table_pageSize,
          page: this.result_table_currentPage,
          require_name: this.require_name,
          result_type: this.result_type,
          product_name: getCookie('product_name')
        }
        api.result_manage_api.query_result_detail(data).then(response => {
          if (response.status === 0) {
            this.result_paas = response.info.ret_info.test_pass
            this.result_not_paas = response.info.ret_info.test_not_pass
            this.result_table = response.info.ret_info.ret_info
            this.result_table_count = response.info.total_count
          } else {
            console.log(response.info)
          }
        })
      },
      close_dialog() {
        this.visibleEdit = false
      },
      // 查询任务信息
      query_instance_info() {
        let data = {
          instance_id: this.instance_id
        }
        api.whole_process_test.query_instance_info(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info.info
            this.finish_count = response.info.finish_count
            this.executing_count = response.info.executing_count
            this.test_status = response.info.test_status
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.loading = false
        })
      },
      // 人工确认
      pass_is(index, rows) {
        let data = {
          result_desc: rows.diff_result,
          task_id: rows.task_id,
          user_id: getCookie('user_id')
        }
        api.paas_whole_test_api.paas_task_confirm(data).then(response => {
          this.$set(this.tableData, index, rows)
          this.$message.success('人工确认完成')
        })
      },
      // 父组件调用离开页面前判断socket是否关闭
      close_socket() {
        console.log('socket----', this.socket)
        if (this.test_status === '未完成') {
          this.$confirm('剩余任务未执行完毕, 是否离开该界面?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            if (this.rc_loading) {
              this.$message({
                type: 'success',
                message: '稍后可到结果管理中查看执行结果!'
              })
            }
            if (this.socket !== '') {
              this.socket.close()
            }
            this.$emit('leave_route')
          }).catch(_ => {})
        } else if (this.test_status === '测试完成') {
          this.$emit('leave_route')
        }
      },
      // 返回第一步
      return_first_step() {
        if (this.socket !== '') {
          this.socket = ''
        }
        this.$emit('return_first_step')
      }
    },
    created() {
      this.loading = true
      this.query_instance_info()
    },
    computed: {
      instance_id: function () {
        console.log('instance_id', this.step_two_info.instance_id)
        return this.step_two_info.instance_id
      },
      task_info: {
        get() {
          // this.tableData = this.step_two_info.info
          return this.step_two_info.info
        },
        set(v) {
          this.step_two_info.info = v
        }
      },
      require_name: function () {
        return this.step_one_info.instance_info.require_name
      }
    },
    watch: {
      finish_count: {
        handler(newValue, oldValue) {
          console.log('old_finish', oldValue)
          console.log('new_finish', newValue)
        },
        immediate: true
      }
    }
  }
</script>
<style lang="scss" scoped>
  .zf_box {
    color: #333;
  }

  .three_ul {
    display: flex;
    flex-wrap: wrap;

    li {
      color: #fff;
      font-size: 20px;
      background: #ffffff;
      border-radius: 6px;
      flex: 1;
      padding: 22px 0;
      text-align: center;
      box-shadow: 0px 1px 4px 0px rgba(46, 88, 247, 0.2);
      margin-top: 49px;
      margin-bottom: 24px;
      margin-right: 16px;

      &:last-child {
        margin-right: 0;
      }

      &:nth-child(1) {
        background: #7088f7
      }

      &:nth-child(2) {
        background: #6da4eb
      }

      &:nth-child(3) {
        background: #ee8878
      }
    }
  }

  .ex_cell {
    word-break: normal;
    width: auto;
    display: block;
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  .div-a {
    float: left;
    width: 50%;
    max-height: 600px;
    overflow-y: scroll;
  }

  .div-b {
    float: right;
    width: 50%;
    max-height: 600px;
    overflow-y: scroll;
  }

  .info th {
    font-weight: normal;
    font-size: 15px;
    text-align: center;
    background-color: #eee;
    border: 1px solid #ddd;
    width: 150px;
  }

  .info tr {
    line-height: 48px;
  }

  .info td {
    border: 1px solid #ddd;
    padding-left: 10px;
    width: 210px;
  }

  .form_style {
    color: #0073ff;
  }
</style>
