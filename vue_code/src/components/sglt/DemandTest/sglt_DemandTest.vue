<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="测试名称">
            <el-input placeholder="请输入测试名称" clearable v-model="search_input.test_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="资费代码">
            <el-input placeholder="请输入资费代码" clearable v-model="search_input.offer_id" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="测试状态">
            <el-select size="small" v-model="search_input.test_status" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
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
            <el-table-column prop="require_name" label="测试名称"></el-table-column>
            <el-table-column prop="offer_id" label="资费代码"></el-table-column>
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
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-edit"
                  @click="handle_edit(scope.row)">
                  编辑
                </el-button>
                <el-button type="text" size="mini" @click="look_result(scope.row)" style="color: green" icon="el-icon-view">
                  详情
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

    <Dialog v-bind:visible="visibleEdit" width="600" @closeDialog="close_dialog" :title="dailogTitleType+'需求'">
      <div slot="con">
        <el-form :model="formEdit" label-width="140px" :rules="rules" ref="formEdit">
          <el-form-item label="测试需求名称" prop="require_name">
            <el-input
              placeholder="请输入内容"
              v-model="formEdit.require_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="资费标识" prop="offer_id">
            <el-input
              placeholder="请输入内容"
              v-model="formEdit.offer_id"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="资费名称" prop="offer_name">
            <el-input
              placeholder="请输入内容"
              v-model="formEdit.offer_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="计划完成时间" prop="test_date">
            <el-date-picker
              v-model="formEdit.test_date"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择日期时间"
              style="width:225px">
            </el-date-picker>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" plain @click="reset_form">重置</el-button>
          <el-button type="primary" @click="submit('formEdit')">确认</el-button>
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
          offer_id: '',
          test_status: ''
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

        dailogTitleType: "",
        visibleEdit: false,

        rules: {
          require_name: [
            {required: true, message: '测试需求名称不能为空', trigger: 'blur'},
          ],
          offer_id: [
            {required: true, message: '资费标识不能为空', trigger: 'blur'},
          ],
          offer_name: [
            {required: true, message: '资费名称不能为空', trigger: 'blur'},
          ],
          test_date: [
            {required: true, message: '计划完成时间不能为空', trigger: 'blur'}
          ]
        },
        formEdit: {
          require_name: '',
          offer_id: '',
          offer_name: '',
          test_date: '',
          require_id: ''
        },
      }
    },
    methods: {
      handleSizeChange (size) {
        this.pageSize = size
        this.handle_search()
      },
      handleCurrentChange (val) {
        this.currentPage = val
        this.handle_search()
      },
      close_dialog () {
        this.visibleEdit = false
      },
      // 重置搜索框
      reset_search () {
        this.search_input = {
          test_name: '',
          offer_id: '',
          test_status: ''
        }
        this.handle_search()
      },
      // 查询测试结果表数据
      handle_search () {
        let data = {
          page: this.currentPage,
          pageSize: this.pageSize,
          require_name: this.search_input.test_name,
          offer_id: this.search_input.offer_id,
          test_status: this.search_input.test_status,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.check_test_require(data).then(res => {
          if (res.status === 0) {
            this.tableData = res.info
            this.total_count = res.total_count
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 删除
      handle_delete (index, row) {
        this.$confirm('是否确定删除？').then(_ => {
          let data = {
            require_id: row.require_id,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.delete_test_require(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
              this.handle_search()
            }
            else {
              this.$message.error('系统异常，请联系管理员！')
            }
          });
        })
      },
      // 编辑
      handle_edit (row) {
        this.visibleEdit = true
        this.dailogTitleType = "编辑"
        // 表单回显
        this.formEdit.require_name = row.require_name
        this.formEdit.offer_id = row.offer_id
        this.formEdit.test_date = row.test_date
        this.formEdit.offer_name = row.offer_name
        this.formEdit.require_id = row.require_id
      },
      // 重置编辑表单
      reset_form () {
        this.formEdit = {
          require_name: '',
          offer_id: '',
          offer_name: '',
          test_date: '',
        }
      },
      // 提交编辑
      submit (form) {
        console.log(form)
        this.$refs[form].validate(valid => {
          if (valid) {
            let data = {
              require_id: this.formEdit.require_id,
              require_name: this.formEdit.require_name,
              offer_id: this.formEdit.offer_id,
              offer_name: this.formEdit.offer_name,
              test_date: this.formEdit.test_date
            }
            api.config_manage_api.add_test_require(data).then(res => {
              if (res.status === 0) {
                this.require_id = ''
                this.$message.success('编辑成功！')
                this.visibleEdit = false
                this.currentPage = 1
                this.handle_search()
              }
              else {
                this.$message.error('系统异常，请联系管理员！')
              }
            })
          }
        })
      },
      // 查看全网测试结果详情
      look_result (rows) {
        console.log(this.$router)
        this.$router.push({
          path: '/result/all_net_test_result',
          query: {
            offer_id: rows.offer_id
          }
        })
      }
    },
    mounted() {
      this.currentPage = 1
      this.handle_search()
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
</style>
