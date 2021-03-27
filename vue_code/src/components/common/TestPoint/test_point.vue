<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="测试点名称">
            <el-input placeholder="请输入内容" clearable v-model="search_input.point_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="point_reset_search">重置
            </el-button>
            <el-button type="primary" size="small" @click="point_handle_search">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <div slot="extral">
        <el-button type="primary" size="mini" plain class="optionBtn" @click="point_handle_add">新增</el-button>
      </div>
      <template slot="body">
        <div class="table mgt-10">
          <el-table
            :data="point_table_data"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="point_code" label="测试点编号"></el-table-column>
            <el-table-column prop="point_name" label="测试点名称"></el-table-column>
            <el-table-column prop="point_type" label="测试点分类"></el-table-column>
            <el-table-column prop="point_desc" label="测试点描述"></el-table-column>
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-delete"
                  style="color: red"
                  @click="point_handle_delete(scope.row)">
                  删除
                </el-button>
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-edit"
                  @click="point_handle_edit(scope.row)">
                  编辑
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="point_handle_size_change"
              @current-change="point_handle_current_change"
              :current-page.sync="point_current_page"
              :page-sizes="[5,10,15]"
              :page-size="point_page_size"
              layout="sizes, prev, pager, next"
              :total="point_total_count">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>

    <Dialog :visible="visible_flag" width="600" :title.sync="dialog_title" @closeDialog="point_close_edit">
      <div slot="con">
        <el-form :model="form_edit" label-width="100px" :rules="rules" ref="form_edit">
          <el-form-item label="测试点编号" prop="point_code">
            <el-input
              placeholder="请输入测试点编号"
              v-model="form_edit.point_code"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试点名称" prop="point_name">
            <el-input
              placeholder="请输入测试点名称"
              v-model="form_edit.point_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试点描述" prop="point_desc">
            <el-input
              placeholder="请输入测试点描述"
              v-model="form_edit.point_desc"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试点分类" prop="point_type">
            <el-select
              v-model="form_edit.point_type"
              placeholder="请选择"
              style="width:225px">
              <el-option label="清单测试点" value="清单测试点"></el-option>
              <el-option label="账单测试点" value="账单测试点"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="预期结果" prop="expect_result">
            <el-input
              style="width:308px"
              type="textarea"
              placeholder="请输入内容"
              :rows="4"
              v-model="form_edit.expect_result">
            </el-input>
            <el-tooltip
              class="item"
              effect="light"
              content="点击提示预期结果参数信息"
              placement="top">
              <span class="tips_pos">
                <el-button size="small" type="text" @click="open">提示</el-button>
              </span>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" placement="right-start">
              <div slot="content">根据提示输入单词组成的公式<br/>注意：只能输入单词和运算符且不能有空格和特殊字符</div>
              <el-button icon="el-icon-info" size="mini" type="text"></el-button>
            </el-tooltip>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" plain @click="reset_form">重置</el-button>
          <el-button type="primary" @click="submit('form_edit')">确认</el-button>
        </div>
      </div>
    </Dialog>

  </div>
</template>

<script>
  import api from "../../../service/api";
  import {getCookie} from "../../../service/cookie";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox'),
      Dialog: () => import('@/components/common/Dialog'),
      ShuttleBox: () => import('@/components/common/ShuttleBox')
    },
    data() {
      let check_expect_result = (rule, value, callback) => {
        let flag = 0

        // 如果不是英文、下划线、运算符和()就提示
        if (/.*[\u4e00-\u9fa5]+.*$/.test(value)) {
          callback(new Error('不能包含中文！'))
        }
        let pattern = new RegExp(/[^(\+)(\-)(\*)(\/)(\.)(\()(\))(\_)(a-zA-Z)(0-9)]+/)
        if (pattern.test(value)) {
          callback(new Error('不能包含除运算符外的特殊字符'))
        }
        let value_arr = value.replace(/[^a-zA-Z_]/g, ',').split(',')
        for (let i = 0; i < value_arr.length; i++) {
          if (value_arr[i] === '') {
            value_arr.splice(i, 1)
            i = i - 1
          }
        }
        for (let j = 0; j < value_arr.length; j++) {
          if (this.expect_arr.indexOf(value_arr[j]) === -1) {
            flag = 1
            break
          }
        }
        flag === 1 ? callback(new Error('请根据提示输入正确的参数')) : callback()
      }

      return {
        // 查询搜索内容
        search_input: {
          point_name: ''
        },
        // 测试点表格
        point_table_data: [],
        point_page_size: 10,
        point_current_page: 1,
        point_total_count: 0,
        // 测试点编辑
        visible_flag: false,
        dialog_title: '',
        form_edit: {
          point_id: '',
          point_code: '',
          point_type: '',
          point_name: '',
          point_desc: '',
          expect_result: ''
        },
        rules: {
          point_code: [{required: true, message: '测试点编号不能为空', trigger: "blur"}],
          point_name: [{required: true, message: '测试点名称不能为空', trigger: 'blur'}],
          point_desc: [{required: true, message: '测试点描述不能为空', trigger: 'blur'}],
          point_type: [{required: true, message: '请选择分类', trigger: 'blur'}],
          expect_result: [
            {required: true, message: '预期结果不能为空', trigger: 'blur'},
            {validator: check_expect_result, trigger: 'change'},
          ]
        },
        tips_str: '',
        expect_arr: []
      }
    },
    methods: {
      // 测试点查询
      point_handle_search() {
        let data = {
          page: this.point_current_page,
          pageSize: this.point_page_size,
          point_name: this.search_input.point_name,
          user_id: getCookie('user_id')
        }
        api.config_manage_api.check_point_info(data).then(response => {
          if (response.status === 0) {
            this.point_table_data = response.info
            this.point_total_count = response.total_count
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      point_reset_search() {
        this.search_input.point_name = ''
        this.point_handle_search()
      },
      // 测试点分页
      point_handle_current_change(val) {
        this.point_current_page = val
        this.point_handle_search()
      },
      point_handle_size_change(size) {
        this.point_page_size = size
        this.point_handle_search()
      },
      // 测试点删除
      point_handle_delete(row) {
        this.$confirm('是否删除此测试点?', '提示', {
          type: 'warning'
        }).then(() => {
          let data = {
            point_id: row.point_id,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.delete_point_info(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
            } else {
              this.$message.error('系统异常，请联系管理员！')
            }
            this.point_current_page = 1
            this.search_input.point_name = ''
            this.point_handle_search()
          })
        })
      },
      // 测试点编辑
      point_handle_edit(row) {
        this.dialog_title = '编辑测试点'
        this.visible_flag = true
        this.form_edit.point_code = row.point_code
        this.form_edit.point_type = row.point_type
        this.form_edit.point_name = row.point_name
        this.form_edit.point_desc = row.point_desc
        this.form_edit.expect_result = row.expect_result
        this.form_edit.point_id = row.point_id
      },
      // 新增测试点
      point_handle_add() {
        this.dialog_title = '新增测试点'
        this.visible_flag = true
        this.form_edit.point_id = ''
        this.reset_form()
      },
      // 提交编辑表单
      submit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let data = {
              point_id: this.form_edit.point_id,
              point_code: this.form_edit.point_code,
              point_type: this.form_edit.point_type,
              point_name: this.form_edit.point_name,
              point_desc: this.form_edit.point_desc,
              expect_result: this.form_edit.expect_result,
              user_id: getCookie('user_id')
            }
            api.config_manage_api.add_point_info(data).then(response => {
              if (response.status === 0) {
                this.$message.success('编辑成功！')
                this.point_handle_search()
              }else {
                this.$message.error('系统异常，请联系管理员！')
              }
              this.visible_flag = false
            })
          }
        })
      },
      // 重置表单
      reset_form() {
        this.form_edit.point_code = ''
        this.form_edit.point_type = ''
        this.form_edit.point_name = ''
        this.form_edit.point_desc = ''
        this.form_edit.expect_result = ''
      },
      // 关闭编辑弹窗
      point_close_edit() {
        this.dialog_title = ''
        this.visible_flag = false
      },
      // 获取提示内容
      get_tips() {
        let data = {
          user_id: getCookie('user_id')
        }
        api.config_manage_api.get_formula_info(data).then(response => {
          let tips = response.info
          for (let i = 0; i < tips.length; i++) {
            this.expect_arr = this.expect_arr.concat(Object.values(tips[i]))
          }
          for (let i = 0; i < tips.length; i++) {
            this.tips_str = this.tips_str + Object.keys(tips[i]) + ": " + '<br>' + Object.values(tips[i]) + "<br>"
          }
        })
      },
      // 弹框提示
      open() {
        this.$notify({
          customClass: 'infoStyle',
          title: '参数信息',
          duration: 60000,
          dangerouslyUseHTMLString: true,
          message: this.tips_str,
          type: 'info',
        });
      },
    },

    mounted() {
      this.point_current_page = 1
      this.point_handle_search()
      this.get_tips()
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
    box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.15);

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
  .infoStyle {
    width: 300px;
    max-height: 600px;
    overflow: scroll !important;
  }
</style>
