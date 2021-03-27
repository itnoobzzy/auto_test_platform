
<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="数据类型">
            <el-input placeholder="请输入用户数据类型" clearable v-model="search_info.user_data_type" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="reset_search">重置
            </el-button>
            <el-button type="primary" size="small" @click="handle_search">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <div slot="extral">
        <el-button type="primary" size="mini" plain @click="handle_add">新增</el-button>
      </div>
      <template slot="body">
        <div class="table mgt-10">
          <el-table :data="testtableData" style="width: 100%" max-height="500px">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-width="100px" size="mini" class="my-form">
                  <el-form-item label="用户数据类型">
                    <span>{{ props.row.user_data_type }}</span>
                  </el-form-item>
                  <el-form-item label="关键字一">
                    <span>{{ props.row.key_field1 }}</span>
                  </el-form-item>
                  <el-form-item label="关键字二">
                    <span>{{ props.row.key_field2 }}</span>
                  </el-form-item>
                  <el-form-item label="用户数据">
                    <span>{{ props.row.user_data_value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column prop="user_data_type" label="用户数据类型" align="center"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="key_field1" label="关键字一" align="center"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="key_field2" label="关键字二" align="center"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="user_data_value" label="用户数据" align="center"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button size="mini" type="text" @click="handlemodify(scope.$index, scope.row)" icon="el-icon-edit">编辑
                </el-button>
                <el-button
                  @click.native.prevent="deleteRow(scope.row)" type="text" size="mini"
                  icon="el-icon-delete"
                  style="color: red"> 移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </CardBox>

    <Dialog v-bind:visible.sync="testdialogForm" width="600" @closeDialog="testdialogForm=false" :title="dailogTitleType+'用户数据'">
      <div slot="con">
        <el-form :model="testruleForm" :rules="rules" ref="testruleForm" label-width="180px">
          <el-form-item size='mini' label="用户数据类型:" prop="user_data_type">
            <el-input size='mini' v-model="testruleForm.user_data_type" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item size='mini' label="关键字段一:" prop="key_field1">
            <el-input size='mini' v-model="testruleForm.key_field1" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item size='mini' label="关键字段二:" prop="key_field2">
            <el-input size='mini' v-model="testruleForm.key_field2" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item size='mini' label="用户样例数据:" prop="user_data_value">
            <el-input size='mini' v-model="testruleForm.user_data_value" style="width: 50%" type="textarea"></el-input>
            <el-tooltip class="item" effect="dark" placement="right-start">
              <div slot="content">多条数据以","分隔<br/>例：1,1,65268685,201702,201702,17,17,20170217081622,20500101000000,0</div>
              <el-button icon="el-icon-info" size="mini" type="text"></el-button>
            </el-tooltip>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="mini" @click="submit('testruleForm')">确定</el-button>
            <el-button size="mini" @click="cleartestruleForm('testruleForm')">重置</el-button>
          </el-form-item>
        </el-form>
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
      Dialog: () => import('@/components/common/Dialog'),
    },
    data () {
      return {
        // 用户数据编辑表单
        testdialogForm: false,
        dailogTitleType: '',
        testruleForm: {
          id: '',
          user_data_type: '',
          key_field1: '',
          key_field2: '',
          user_data_value: '',
        },
        rules: {
          user_data_type: [{required: true, message: '用户数据类型不能为空', trigger: "change"}],
          user_data_value: [{required: true, message: '用户数据不能为空', trigger: 'change'}],
        },
        // 查询输入信息
        search_info: {
          user_data_type: ""
        },
        // 表格
        testtableData: [],
      }
    },
    methods: {
      // 打开新增表单
      handle_add() {
        this.cleartestruleForm()
        this.testdialogForm = true
        this.dailogTitleType = "新增"
      },
      reset_search() {
        this.search_info.user_data_type = ''
        this.handle_search()
      },
      handle_search() {
        let data = {
          user_data_type: this.search_info.user_data_type,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.query_user_data(data).then(response => {
          if (response.status === 0){
            this.testtableData = response.info
          }else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 打开编辑表单
      handlemodify($index, row) {
        this.testdialogForm = true
        this.dailogTitleType = "编辑"
        this.testruleForm.id = row.id
        this.testruleForm.user_data_type = row.user_data_type
        this.testruleForm.key_field1 = row.key_field1
        this.testruleForm.key_field2 = row.key_field2
        this.testruleForm.user_data_value = row.user_data_value
      },
      // 删除
      deleteRow(rows) {
        this.$confirm('是否删除该用户数据？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '确定删除',
          cancelButtonText: '放弃删除'
        }).then(()=> {
          let data = {
            id: rows.id,
            user_data_type : rows.user_data_type,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.delete_user_data(data).then(response => {
            if (response.status === 0){
              this.$message.success('删除成功！')
            }else {
              this.$message.error('系统异常，请联系管理员！')
            }
            this.handle_search()
          })
        }).catch(()=>{})
      },
      // 提交表单
      submit(formName) {
        console.log(this.testruleForm)
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let data = {
              id: this.testruleForm.id,
              user_data_type: this.testruleForm.user_data_type,
              user_data_value: this.testruleForm.user_data_value,
              key_field1: this.testruleForm.key_field1,
              key_field2: this.testruleForm.key_field2,
              user_id: getCookie('user_id')
            }

            if (this.dailogTitleType === "编辑") {
              api.config_manage_api.update_user_data(data).then(response => {
                if (response.status === 0){
                  this.$message.success('编辑成功！')
                  this.handle_search()
                }else {
                  this.$message.error('系统异常，请联系管理员！')
                }
              })
            }
            else {
              api.config_manage_api.add_user_data(data).then(response => {
                if (response.status === 0){
                  this.$message.success('新增成功！')
                  this.handle_search()
                }else {
                  this.$message.error('系统异常，请联系管理员！')
                }
              })
            }
            this.testdialogForm = false
            this.search_info.user_data_type = ''
          }
        });
      },
      // 清除表单
      cleartestruleForm() {
        this.testruleForm.id = ''
        this.testruleForm.user_data_type = ''
        this.testruleForm.user_data_value = ''
        this.testruleForm.key_field2 = ''
        this.testruleForm.key_field1 = ''
      },
    },
    mounted() {
      this.handle_search()
    }
  }
</script>
<style lang="scss" scoped>
  .search_box {
    padding: 20px 0;
    display: flex;
    align-items: center;
  }
  .tips_pos {
    font-size: 14px;
    color: #2e58f7;
    margin-left: 10px;
  }
  .mc_msg {
    padding: 16px;
    position: absolute;
    right: -21vw;
    top: 0;
    z-index: 2099;
    width: 199px;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
    .close {
      color: #ddd;
      position: absolute;
      right: -9.5px;
      top: -9.5px;
      font-size: 20px;
      background: #fff;
      border-radius: 9.5px;
      width: 16px;
      height: 16px;
    }
    &_title {
      font-size: 14px;
      color: #333;
      margin-bottom: 14px;
    }
    p {
      color: #666666;
      font-size: 14px;
      line-height: 1.5;
    }
  }
  .color-zi {
    color: #8b8fff;
    display: inline-block;
    margin-right: 4px;
  }
</style>
<style>
  .my-form .el-form-item__content{
    color: blue !important;
    word-break: break-all !important;
  }
</style>

