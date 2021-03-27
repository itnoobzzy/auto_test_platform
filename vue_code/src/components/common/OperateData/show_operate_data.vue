<template>
  <div>
    <el-row  style="margin: 1rem 1rem 1rem 0">
      <h3>测试能力情况</h3>
    </el-row>
    <el-row :gutter="15" justify="center" type="flex">
      <el-col :span="4">
        <el-card shadow="always" :body-style="card_body_style" class="card1">
          <div v-if="!loading">
            <p>测试用例数量</p>
            <div class="card_span">
              <span>当月{{test_case_count}}个</span>
              <span>上月{{last_test_case_count}}个</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="always" :body-style="card_body_style" class="card2">
          <div v-if="!loading">
            <p>全流程测试次数</p>
            <div class="card_span">
              <span>当月{{whole_test_times}}次</span>
              <span>上月{{last_whole_test_times}}次</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="always" :body-style="card_body_style" class="card3">
          <div v-if="!loading">
            <p>测试用例执行次数</p>
            <div class="card_span">
              <span>当月{{test_case_execute_times}}次</span>
              <span>上月{{last_test_case_execute_times}}次</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="always" :body-style="card_body_style" class="card4">
          <div v-if="!loading">
            <p>接口能力调用次数</p>
            <div class="card_span">
              <span>当月{{api_call_times}}个</span>
              <span>上月{{last_api_call_times}}个</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="always" :body-style="card_body_style" class="card5">
          <div v-if="!loading">
            <p>全国商务落地情况</p>
            <div class="card_span">
              <span>当月{{business_landing_times}}个</span>
              <span>上月{{last_business_landing_times}}个</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row style="margin-top: 1rem">
      <el-col :span="12">
        <div v-if="!loading">
          <h3>里程碑</h3>
          <div class="timeline">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in milestone"
                :key="index"
                placement="top"
                color="#72b2d8"
                :timestamp="activity.date">
                <div style="background: whitesmoke;width: 90%">{{activity.milepost_desc}}</div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="china_map" v-loading="loading"
             element-loading-text="数据加载中...请等待..."
             element-loading-spinner="el-icon-loading"
             element-loading-background="white">
          <h3>产品落地信息</h3>
          <div style="margin: 1rem 1rem">
            <el-row>
              产品名称：
              <el-input v-model="input_product_name" placeholder="请输入产品名称" size="mini" style="width: auto"></el-input>
            </el-row>
            <el-row style="margin: 1rem 1rem 1rem 0">
              <div>
                落地省份：
                <el-input v-model="input_area" placeholder="请输入落地省份" size="mini" style="width: auto"></el-input>
                <div style="float: right">
                  <el-button type="primary" size="mini" @click="get_product_list">查询</el-button>
                  <el-button type="info" size="mini" @click="reset_search">重置</el-button>
                </div>
              </div>
            </el-row>

          </div>
          <el-table
            :data="tableData"
            style="width: 100%"
            max-height="315px">
            <el-table-column
              prop="product_name"
              label="产品名称">
            </el-table-column>
            <el-table-column
              prop="area"
              label="落地省份">
            </el-table-column>
            <el-table-column
              label="操作">
              <template slot-scope="scope">
                <el-button type="text" size="mini" @click="next_go(scope.row)">查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {getCookie} from '../../../service/cookie'
  import api from "../../../service/api";

  export default {
    data() {
      return {
        card_body_style: {padding: "15px"},

        loading: false,
        product_name: getCookie('product_name'),

        online_prov_count: 0,
        progress_prov_count: 0,
        promotion_prov_count: 0,
        intention_prov_count: 0,
        // 测试用例数
        test_case_count: 0,
        last_test_case_count: 0,
        // 全流程测试次数
        whole_test_times: 0,
        last_whole_test_times: 0,
        // 测试用例执行次数
        test_case_execute_times: 0,
        last_test_case_execute_times: 0,
        // 接口能力调用次数
        api_call_times: 0,
        last_api_call_times: 0,
        // 商务落地情况
        business_landing_times: 0,
        last_business_landing_times:0,
        //里程碑
        milestone: [],
        tableData: [],
        input_product_name: '',
        input_area: ''

      };
    },
    mounted() {
      this.loading = true;
      this.get_product_list();
    },
    methods: {
      next_go(row) {
        let data = {area: row.area, product_name: row.product_name};
        this.$router.push(`/show_operate_data/detail?info=${JSON.stringify(data)}`);
      },
      // 重置查询
      reset_search() {
        this.input_product_name = ''
        this.input_area = ''
        this.get_product_list()
      },
      // 获取产品名称信息
      get_product_list() {
        let data = {
          search_product_name:this.input_product_name,
          search_prov_name: this.input_area
        }
        api.operate_data_api.get_product_area_list(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info.ret_info.product_info
            if (this.$route.query.hasOwnProperty("product_name")) {
              this.product_name = this.$route.query.product_name
            }
            this.get_area()
          } else
            this.$message.error('系统异常，请联系管理员！')
        });
      },

      get_area() {
        this.loading = true;
        let data = {
          product_name: this.product_name,
        }
        api.operate_data_api.get_view_info(data).then(response => {
          if (response.status === 0) {
            this.milestone = response.info.ret_info.milestone_desc.reverse();
            this.test_case_count =response.info.ret_info.data_info.test_case_count
            this.whole_test_times =response.info.ret_info.data_info.whole_test_times
            this.test_case_execute_times =response.info.ret_info.data_info.test_case_execute_times
            this.api_call_times =response.info.ret_info.data_info.api_call_times
            this.last_test_case_count =response.info.ret_info.last_data_info.test_case_count
            this.last_whole_test_times =response.info.ret_info.last_data_info.whole_test_times
            this.last_test_case_execute_times =response.info.ret_info.last_data_info.test_case_execute_times
            this.last_api_call_times =response.info.ret_info.last_data_info.api_call_times
            this.business_landing_times = response.info.ret_info.data_info.business_landing_times
            this.last_business_landing_times = response.info.ret_info.last_data_info.business_landing_times
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
        this.loading = false
      },
    }
  }
</script>

<style scoped>
  .timeline {
    padding-left: 20px;
    width: 96%;
    height: 550px;
    overflow-y: auto;
    margin: 1rem 1rem;
  }

  .param_left p, .param_right p {
    font-size: 14px;
    color: black;
  }

  .card1 {
    background: lightblue;
  }

  .card2 {
    background: lightcoral;
  }

  .card3 {
    background: lightgreen;
  }

  .card4 {
    background: lightsalmon;
  }

  .card5 {
    background: lightgoldenrodyellow;
  }

  .card_span {
    font-weight: bold;
    margin-top: 18px;
  }

  .card_span > span:nth-child(2) {
    font-size: 12px;
  }

</style>
