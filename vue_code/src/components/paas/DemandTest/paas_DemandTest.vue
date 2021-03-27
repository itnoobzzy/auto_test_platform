<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="测试需求名称">
            <el-input placeholder="请输入需求名称" clearable v-model="search_input.test_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="产品名称" v-if="product_name === '智能测试库平台'">
            <el-input placeholder="请输入产品名称" clearable v-model="search_input.product_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="测试状态">
            <el-select v-model="search_input.test_status" placeholder="请选择" size="mini">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="reset_search">重置</el-button>
            <el-button type="primary" size="small" @click="handle_search">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <template slot="body">
        <div class="table mgt-10">
          <el-table
            :data="tableData"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="require_name" label="测试需求名称"></el-table-column>
            <el-table-column prop="require_source" label="产品名称"></el-table-column>
            <el-table-column prop="test_status" label="测试状态"></el-table-column>
            <el-table-column prop="test_date" label="测试时间"></el-table-column>
            <el-table-column label="操作" width="190">
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-delete"
                  style="color: red"
                  @click="handle_delete(scope.$index, scope.row)">
                  删除
                </el-button>
                <el-button v-if="scope.row.test_status === '已测试'" size="mini" type="text"
                           @click="look_result(scope.row)">
                  <span style="color:green;"><i class="el-icon-view">详情</i></span>
                </el-button>
              </template>
            </el-table-column>
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
                  <span v-html="props.row.real_result">{{ props.row.real_result }}</span>
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
          <el-table-column prop="real_result" width="300" label="实际结果" :show-overflow-tooltip="true">
            <template slot-scope="scope">
              <el-tooltip class="item" effect="light" placement="right-start">
                <div slot="content" style="width: 600px">
                  <div class="div-a">
                    <div v-html="scope.row.real_result">{{scope.row.real_result}}</div>
                  </div>
                </div>
                <el-button type="text" @click="">查看详情</el-button>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="result_desc" label="是否通过" align="center"
                           :show-overflow-tooltip="true"></el-table-column>
        </el-table>
        <div class="search_pagination tr">
          <el-pagination
            @size-change="handleSizeChange2"
            @current-change="handleCurrentChange2"
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
  import {getCookie} from "../../../service/cookie";
  import api from "../../../service/api";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox'),
      Dialog: () => import('@/components/common/Dialog')
    },
    data() {
      return {
        tableData: [],
        currentPage: 1,
        pageSize: 10,
        total_count: 0,

        search_input: {
          test_name: '',
          test_status: '',
          product_name: ''
        },
        options: [
          {
            value: '已测试',
            label: '已测试'
          },
          {
            value: '未测试',
            label: '未测试'
          }
        ],

        result_table: [],
        result_paas: 0,
        result_not_paas: 0,
        show_result: false,
        rc_loading: false,
        require_name: "",
        product_name: getCookie('product_name'),
        result_type: '',

        result_table_pageSize: 10,
        result_table_currentPage: 1,
        result_table_count: 0,
      }
    },
    methods: {
      report_create() {
        this.rc_loading = true
        let data = {
          info: this.result_table
        }
        api.result_manage_api.create_report(data).then(response => {
          window.open(response)
        })
      },
      look_result(rows) {
        this.require_name = rows.require_name
        this.result_type = ''
        this.handlesearch2()
      },
      // 条件过滤结果
      filter_result(result_type) {
        this.result_type = result_type
        let data = {
          page: 1,
          pageSize: 10,
          require_name: this.require_name,
          result_type: result_type,
          user_id: getCookie('user_id')
        }
        api.result_manage_api.query_result_detail(data).then(response => {
          if (response.status === 0) {
            this.result_table = response.info.ret_info.ret_info
            this.result_table_count = response.info.total_count
          }
        })
      },
      handleSizeChange(size) {
        this.pageSize = size
        this.handle_search()
      },
      handleCurrentChange(val) {
        this.currentPage = val
        this.handle_search()
      },
      handleSizeChange2(size) {
        this.result_table_pageSize = size
        this.handlesearch2()
      },
      handleCurrentChange2(val) {
        this.result_table_currentPage = val
        this.handlesearch2()
      },
      handlesearch2() {
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
            let error_infos = response.errors.non_field_errors
            error_infos.forEach(item => {
              this.$message.error(item)
            })
          }
        })
      },
      close_dialog() {
        this.visibleEdit = false
      },
      // 重置搜索框
      reset_search() {
        this.search_input = {
          test_name: '',
          test_status: '',
          product_name: ''
        }
        this.handle_search()
      },
      // 查询测试结果表数据
      handle_search() {
        let data = {
          page: this.currentPage,
          pageSize: this.pageSize,
          require_name: this.search_input.test_name,
          product_name: this.product_name,
          test_status: this.search_input.test_status
        }
        api.result_manage_api.check_test_require(data).then(res => {
          if (res.status === 0) {
            this.tableData = res.info.ret_info
            this.total_count = res.info.total_count
          } else if (res.status === 400){
            res.errors.forEach(item => {
              this.$message.error(item)
            })
          }
        })
      },
      // 删除
      handle_delete(index, row) {
        this.$confirm('是否确定删除？', '提示', {type:"warning"}).then(_ => {
          let data = {
            require_id: row.require_id
          }
          api.result_manage_api.delete_test_result(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
              this.handle_search()
            } else {
              this.$message.error('系统异常，请联系管理员！')
            }
          });
        })
      },
    },
    mounted() {
      this.handleCurrentChange(1);
    }
  }
</script>
<style lang="scss" scoped>
  .el-upload__tip {
    display: inline-block;
    margin-left: 8px;
    color: #666;
    font-size: 14px;
  }

  .icon_word {
    width: 10px;
    margin-right: 2px;

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
