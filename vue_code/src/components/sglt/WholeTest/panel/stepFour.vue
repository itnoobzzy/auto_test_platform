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
        border
        max-height="400"
        ref="selection"
        style="width: 100%">
        <el-table-column align="center" prop="id" label="任务ID">
        </el-table-column>
        <el-table-column align="center" prop="test_name" label="测试用例" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column align="center" prop="test_status" label="测试状态">
        </el-table-column>
        <el-table-column align="center" prop="expect_info" label="预期结果">
        </el-table-column>
        <el-table-column align="center" prop="result_info" label="实际结果">
        </el-table-column>
        <el-table-column align="center" prop="result_desc" label="是否通过">
          <template slot-scope="scope">
            <span v-if="scope.row.result_desc > 2" style="color: red">{{scope.row.result_desc}}</span>
            <span v-else style="color: black">{{scope.row.result_desc}}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
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
      step_three_info: {
        type: Object,
        default: () => {
        }
      }
    },
    components: {
      AreaTitle: () => import('@/components/common/AreaTitle')
    },
    data() {
      return {
        tableData: [],
        socket: '',
        execute_flag: false,
        execute_title: '开始执行',
        result_flag: false,
        test_status: "未提取到数据",

        finish_count: 0,
        executing_count: 0,
      }
    },
    methods: {
      // websocket连接
      con_websocket(instance_id) {
        let ws = new WebSocket(
          'ws://' + window.location.host + '/ws/query_status'
          // 'ws://' + '172.21.4.110:8755' + '/ws/query_status'
        )
        console.log(ws)
        this.socket = ws
        ws.onmessage = function (e) {
          let data = JSON.parse(e.data)
          let message = data['message']
          console.log('message', message)
          func1(message)
        }
        ws.onclose = function (e) {
          console.log('websocket closed！')
          check_close_state()
        }
        ws.onopen = function (e) {
          console.log('success')
          ws.send(instance_id)
        }
        // 判断是否为全流程测试界面
        let check_route_func = function() {
          console.log('route', this.$route)
          if (this.test_status === '未完成' && this.$route.path === '/home/SaaS_wholeProcess') {
            console.log('websocket重连')
            this.con_websocket(instance_id)
          }
        }
        let check_route =  check_route_func.bind(this)
        // 动态刷新测试任务状态
        let func2 = function (message) {
          this.finish_count = message.finish_count
          this.executing_count = message.executing_count
          this.tableData = message.info
          this.test_status = message.test_status
          if (this.test_status === '未完成') {
            this.$message.info('测试中，请等候！')
          } else if (this.test_status === '测试完成') {
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
          user_id: getCookie('user_id'),
          user_token: getCookie('user_token')
        }
        api.whole_test_api.whl_execute_test(data).then(res => {
          if (res.status === 0) {
            this.result_flag = true
          } else if (res.status === -1) {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      look_result() {
        this.$router.push({
          path: '/result/all_net_test_result',
          query: {
            offer_id: this.offer_id
          }
        })
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
            if (this.execute_flag) {
              this.$message({
                type: 'success',
                message: '稍后可到结果管理中查看执行结果!'
              })
            }
            if (this.socket !== '') {
              this.socket.close()
            }
            this.$emit('leave_route', true)
          }).catch(_ => {})
        } else if (this.test_status === '测试完成') {
          this.$emit('leave_route', true)
        }
      },
    },
    mounted() {
      this.query_instance_info()
    },
    computed: {
      offer_id: function () {
        return this.step_one_info.form.fee_code.toString()
      },
      instance_id: function () {
        console.log('instance_id', this.step_three_info.instance_id)
        return this.step_three_info.instance_id
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
</style>
