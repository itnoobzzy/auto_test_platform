<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10">
          <el-row type="flex">
            <el-col :span="6">
              <el-form-item label="资费代码">
                <el-input
                  size="small"
                  clearable
                  v-model="search_input.offer_id"
                  placeholder="请输入资费代码">
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item>
                <el-button
                  type="primary"
                  size="small"
                  plain
                  @click="reset_search"
                  style="background:none">重置
                </el-button>
                <el-button type="primary" size="small" @click="handle_search">查询</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <template slot="body">
        <div class="table_desc">
          <p>名称：{{ require_info }}</p>
          <p>
            需求描述：{{ require_desc }}
          </p>
        </div>
        <div class="table">
          <el-table
            :data="all_test_table_data"
            element-loading-text="拼命加载中"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="test_date" label="测试时间">
            </el-table-column>
            <el-table-column prop="pass_cont" label="通过"></el-table-column>
            <el-table-column prop="not_pass_cont" label="不通过"></el-table-column>
            <el-table-column prop="session_id" align="center" label="session_id" v-if="false"></el-table-column>
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button type="text" @click="cat_report(scope.row)">查看测试报告</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page.sync="all_test_current_page"
              :page-size="all_test_page_size"
              :page-sizes="[5,10,15]"
              layout="sizes, prev, pager, next"
              :total="all_test_total_count">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>

    <Dialog
      :visible="seeReport"
      width="1025"
      @closeDialog="seeReport = false"
      title="测试报告结果">
      <div slot="con">
        <div class="table_desc">
          <p>
            描述：{{ offer_name }}
          </p>
        </div>
        <div class="table">
          <el-table
            :data="report_table_data"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="case_name" label="测试用例名称">
              <template slot-scope="scope">
                <el-popover placement="bottom" width="300" trigger="hover">
                  <el-table :data="scope.row.test_point" class="popber_table" size="small">
                    <el-table-column
                      property="point_name"
                      label="测试点名称"
                      width="190"
                    ></el-table-column>
                    <el-table-column
                      property="diff"
                      label="结果描述"
                    ></el-table-column>
                  </el-table>
                  <p slot="reference">{{ offer_name }}</p>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column prop="test_result" label="用例测试结果">
              <template slot-scope="scope">
                <p class="res_status">
                  <i class="el-icon-circle-check" style="color: lime" v-if="scope.row.test_result==='通过'"></i>
                  <i class="el-icon-circle-close" style="color: red" v-if="scope.row.test_result==='不通过'"></i>
                  {{scope.row.test_result}}
                </p>
              </template>
            </el-table-column>
            <el-table-column label="查看用例测试结果" width="150">
              <template slot-scope="scope">
                <el-button type="text" @click="cat_detail_result(scope.row)">用例测试结果详情</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handleSizeChange2"
              @current-change="handleCurrentChange2"
              :current-page.sync="report_current_page"
              :page-size="report_page_size"
              :page-sizes="[5,10,15]"
              layout="sizes, prev, pager, next"
              :total="report_total_count">
            </el-pagination>
          </div>
        </div>
        <p class="conclusion">
          测试报告结论：
          <span style="color: yellowgreen">{{ test_conclusion.report_conclusion }}</span><br><br>
        </p>
        <div class="text_callback">
          <div>
            请对测试情况进行确认：
            <el-radio-group v-model="radio">
              <el-radio :label="1">通过</el-radio>
              <el-radio :label="2">不通过</el-radio>
            </el-radio-group>
          </div>
          <el-button
            type="primary"
            size="mini"
            style="background:#1677FF"
            @click="check_result_flag = true">确认
          </el-button>
        </div>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" class="import-btn" :loading="rc_loading" icon="el-icon-folder-add" @click="exportReport">导出测试报告</el-button>
        </div>
      </div>
    </Dialog>

    <Dialog
      :visible="check_result_flag"
      width="250"
      @closeDialog="check_result_flag = false"
      message-title="操作提示"
      :modal="false"
      top="30vh">
      <div slot="con">
        请问是否确认提交？
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button
            type="primary"
            plain
            size="small"
            style="padding:8px 30px"
            @click="check_result_flag = false">取消
          </el-button>
          <el-button
            type="primary"
            size="small"
            style="padding:8px 30px"
            @click="author_check">确认
          </el-button>
        </div>
      </div>
    </Dialog>

    <Dialog
      :visible="case_detail_flag"
      width="911"
      @closeDialog="case_detail_flag = false"
      title="测试用例详情">
      <div slot="con">
        <div class="table">
          <el-table
            :data="case_detail_table_data"
            border
            @row-click="rowClick"
            ref="PrcTable"
            style="width: 100%"
            align="center">
            <el-table-column type="expand">
              <template slot-scope="scope">
                <el-table :data="scope.row.test_point">
                  <el-table-column align="center" :label=scope.row.point_type>
                    <el-table-column property="point_name" label="测试点名称"></el-table-column>
                    <el-table-column property="expect_info" label="预期结果"></el-table-column>
                    <el-table-column property="result_info" label="实际结果"></el-table-column>
                    <el-table-column property="diff" label="结果描述">
                      <template slot-scope="scope">
                        <span v-if="scope.row.diff !== '通过'" style="color: red">{{scope.row.diff}}</span>
                        <span v-else style="color: black">{{scope.row.diff}}</span>
                      </template>
                    </el-table-column>
                  </el-table-column>
                </el-table>
              </template>
            </el-table-column>
            <el-table-column prop="case_name" label="测试用例名称">
            </el-table-column>
            <el-table-column prop="msisdn" label="手机号"></el-table-column>
            <el-table-column prop="test_result" label="结果">
              <template slot-scope="scope">
                <span v-if="scope.row.test_result !== '通过'" style="color: red">{{scope.row.test_result}}</span>
                <span v-else style="color: black">{{scope.row.test_result}}</span>
              </template>
            </el-table-column>
            <el-table-column label="查看详情" width="300">
              <template slot-scope="scope">
                <el-button type="text" @click="cat_list_detail(scope.row, 0)">清单详情</el-button>
                <el-button type="text" @click="cat_list_detail(scope.row, 1)">账单详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div style="padding-bottom:30px">
          <p class="conclusion" style="margin:48px 0 0 0">
            测试用例结论：{{ test_conclusion.case_conclusion }}
          </p>
        </div>
      </div>
    </Dialog>

    <Dialog :visible="cdr_flag"
            width="911"
            @closeDialog="cdr_flag = false"
            :title="'清单详情'">
      <div slot="con">
        <div class="table pdb-30">
            <el-table
              :data="list_table_data"
              border
              ref="selection"
              style="width: 100%">
              <el-table-column v-for="(item, index) in dynamic_column" :key="index" :label="item.chn_name"
                               align="center">
                <template slot-scope="scope">
                  {{ scope.row.field_info[index].value}}
                </template>
              </el-table-column>
            </el-table>
        </div>
      </div>
    </Dialog>

    <Dialog :visible="acc_flag"
            width="911"
            @closeDialog="acc_flag = false"
            :title="'账单详情'">
      <div slot="con">
        <div class="table pdb-30">
            <el-table
              :data="list_table_data"
              border
              ref="selection"
              style="width: 100%">
              <el-table-column prop="duration"  label="累积量" align="center"></el-table-column>
              <el-table-column prop="offerFee"  label="套餐内费用" align="center"></el-table-column>
              <el-table-column prop="offerOutFee"  label="详单总费用(厘)" align="center"></el-table-column>
              <el-table-column prop="totalFee"  label="本期消费总额" align="center"></el-table-column>
            </el-table>
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
        instance_id: '',
        session_id: '',
        // 资费代码
        offer_id: '',
        // 需求名称
        require_info: '',
        // 需求描述
        require_desc: '',
        // 查询内容
        search_input: {
          offer_id: ''
        },
        // 全网测试首页界面表格显示
        all_test_table_data: [],
        all_test_current_page: 1,
        all_test_page_size: 10,
        all_test_total_count: 0,
        // 测试报告
        seeReport: false,
        report_table_data: [],
        report_current_page: 1,
        report_page_size: 10,
        report_total_count: 0,
        offer_name: '',
        // 人工确认
        radio: 1,
        check_result_flag: false,
        // 测试用例详情
        case_detail_flag: false,
        case_detail_table_data: [],
        case_detail_desc_info: '',
        // 清单详情或者账单详情
        cdr_flag: false,
        acc_flag: false,
        list_table_data: [],
        // 结论
        test_conclusion: {
          report_conclusion: '',
          case_conclusion: ''
        },
        // 导出测试报告按钮
        rc_loading: false,

      }
    },
    methods: {
      // 查询
      handle_search() {
        if (!this.search_input.offer_id) {
          this.$message.warning('请输入资费id查询')
        }
        let data = {
          pageSize: this.all_test_page_size,
          page: this.all_test_current_page,
          offer_id: this.search_input.offer_id,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.all_test_result(data).then(response => {
          if (response.status === 0) {
            this.require_info = "测试需求单"
            this.require_desc = response.info[0].require_name
            this.offer_name = response.info[0].offer_name
            this.all_test_table_data = response.info
            this.all_test_total_count = response.total_count
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        });

      },
      // 重置搜索
      reset_search() {
        this.search_input.offer_id = this.offer_id
        this.handle_search()
      },
      // 全网测试结果分页
      handleSizeChange(size) {
        this.all_test_page_size = size
        this.handle_search()
      },
      handleCurrentChange(val) {
        this.all_test_current_page = val
        this.handle_search()
      },
      // 测试报告分页
      handleSizeChange2(size) {
        this.report_page_size = size
        this.get_report_result()
      },
      handleCurrentChange2(val) {
        this.report_current_page = val
        this.get_report_result()
      },
      // 查看测试报告
      cat_report(row) {
        this.session_id = row.session_id
        this.instance_id = row.instance_id
        this.seeReport = true
        this.get_report_result()
      },
      // 获取测试报告结果信息
      get_report_result() {
        let data = {
          instance_id: this.instance_id,
          pageSize: this.report_page_size,
          page: this.report_current_page,
        }
        api.config_manage_api.get_test_report(data).then(response => {
          if (response.status === 0) {
            this.offer_name = response.info.offer_name
            this.report_table_data = response.info.case_user_info
            this.report_total_count = response.info.total_count
            this.test_conclusion.report_conclusion = response.info.test_conclusion
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 人工确认报告结果
      author_check() {
        let check_desc = ''
        this.radio === 1 ? check_desc = "确认通过" : "确认未通过"
        let data = {
          offer_id: this.offer_id,
          session_id: this.session_id,
          check_desc: check_desc
        }
        api.config_manage_api.test_author_isfocus(data).then(response => {
          if (response.status === 0) {
            this.$message.success('确认成功！')
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.check_result_flag = false
        })
      },
      // 查看用例测试结果详情
      cat_detail_result(row) {
        this.case_detail_flag = true
        let data = {
          task_id: row.task_id,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.get_test_report(data).then(response => {
          if (response.status === 0) {
            this.case_detail_table_data = response.info
            this.test_conclusion.case_conclusion = response.test_conclusion
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      rowClick() {
        this.$refs.PrcTable.toggleRowExpansion();
      },

      cat_list_detail(row, flag) {
        let data = {
          task_id: row.task_id,
          msisdn: row.msisdn,
          flag: flag,
        }
        flag === 0 ? this.cdr_flag = true : this.acc_flag = true
        api.config_manage_api.get_list_fedx(data).then(response => {
          if (response.status === 0) {
            this.list_table_data = response.info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 导出测试报告
      exportReport () {
        this.rc_loading = true
        let data = {
          info: this.report_table_data,
          offer_name: this.offer_name,
          user_id:getCookie('user_id')
        }
        api.config_manage_api.create_report(data).then(res => {
          if (res.status === -4){
            alert('非法请求')
            this.$router.push('/')
          } else {
            this.rc_loading = false
            console.log('导出测试报告',res)
            window.open(res)
          }
        })
      },
    },
    computed: {
      dynamic_column: function () {
        if (this.list_table_data.length > 0) {
          return this.list_table_data[0].field_info
        } else {
          return []
        }
      }
    },
    mounted() {
      // console.log(this.$route)
      if (this.$route.query.hasOwnProperty('offer_id')) {
        this.offer_id = this.$route.query.offer_id
        this.search_input.offer_id = this.$route.query.offer_id
        this.handle_search()
      }
    }
  }
</script>
<style lang="scss" scoped>
  .table_desc {
    font-size: 16px;
    display: flex;
    padding: 12px 0;
    color: #333;

    p {
      margin-right: 80px;
    }
  }

  .res_status {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;

    .pass {
      width: 22px;
      height: 22px;
      display: block;
      margin-right: 6px;
      background: url(~@/assets/images/pic/pass.png) no-repeat center center/100% 100%;
    }
  }

  .conclusion {
    color: #2e58f7;
    font-size: 14px;
    padding-left: 32px;
    position: relative;
    margin: 28px 0 40px 0;

    &::before {
      content: "";
      width: 24px;
      height: 24px;
      position: absolute;
      left: 0;
      top: 50%;
      display: block;
      background: url(~@/assets/images/pic/jielun.png) no-repeat center center/100% 100%;
      margin-top: -12px;
    }
  }

  .text_callback {
    padding: 5px 20px;
    background: rgba(102, 102, 102, 0.05);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .upload_over {
    font-size: 16px;
    text-align: center;
    padding-bottom: 19px;

    img {
      display: block;
      margin: 0 auto;
      margin-bottom: 20px;
      width: 42px;
    }
  }

  .clear_text {
    color: #333;
    font-size: 14px;
    margin: 16px 0 8px 0;
  }

  .popber_shadow {
    padding: 12px 20px;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.10);
  }
</style>
