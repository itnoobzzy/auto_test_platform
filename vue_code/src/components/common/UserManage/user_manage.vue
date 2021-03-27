<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="用户名称">
            <el-input placeholder="请输入用户名称" clearable v-model="search_input.user_name" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="reset_search">重置</el-button>
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
          <el-table
            :data="tableData"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column prop="user_name" label="用户名" align="center"></el-table-column>
            <el-table-column prop="role_name" label="用户角色" align="center"></el-table-column>
            <el-table-column prop="product_name" label="产品名称" align="center"></el-table-column>
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

    <Dialog v-bind:visible="visibleEdit" width="600" @closeDialog="close_dialog" :title="dailogTitleType+'用户'">
      <div slot="con">
        <el-form :model="formEdit" label-width="140px" :rules="rules" ref="formEdit">
          <el-form-item label="用户名" prop="user_name">
            <el-input
              placeholder="请输入用户名"
              v-model="formEdit.user_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="用户密码" prop="user_password">
            <el-input
              placeholder="请输入用户密码"
              v-model="formEdit.user_password"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="用户角色" prop="user_role_id">
            <el-select v-model="formEdit.user_role_id" placeholder="请选择用户角色">
              <el-option
                v-for="item in roles"
                :key="item.role_id"
                :label="item.role_name"
                :value="item.role_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="产品列表" prop="product_name">
            <el-autocomplete
              class="inline-input"
              v-model="formEdit.product_name"
              :fetch-suggestions="querySearch"
              placeholder="请输入产品名称"
            ></el-autocomplete>
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
          user_name: ''
        },

        dailogTitleType: "",
        visibleEdit: false,

        product_list: [],
        roles: [],
        id111: '',

        rules: {
          user_name: [
            {required: true, message: '用户名不能为空', trigger: 'blur'},
          ],
          user_password: [
            {required: true, message: '用户密码不能为空', trigger: 'blur'},
          ],
          user_role_id: [
            {required: true, message: '用户角色不能为空', trigger: 'change'},
          ],
          product_name: [
            {required: true, message: '产品类型不能为空', trigger: 'change'}
          ]
        },
        formEdit: {
          user_name: '',
          user_password: '',
          user_role_id: '',
          product_name: ''
        },
      }
    },
    methods: {
      querySearch(queryString, cb) {
        let product_list = []
        this.product_list.map((item, index) => {
          let obj = {}
          obj['value'] = item
          product_list[index] = obj
        })
        let results = queryString ? product_list.filter(this.createFilter(queryString)) : product_list;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (product_name) => {
          return (product_name.value.indexOf(queryString) === 0);
        };
      },
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
          user_name: ''
        }
        this.handle_search()
      },
      // 用户列表
      handle_search () {
        let data = {
          page: this.currentPage,
          pageSize: this.pageSize,
          user_name: this.search_input.user_name,
          user_id: getCookie('user_id'),
          user_role_id: getCookie('user_role_id')
        }
        api.system_manage_api.query_user_menu_info(data).then(response => {
          this.tableData = response.info.user_list
          this.total_count = response.info.total_count
          this.roles = response.info.user_role_info
          this.product_list = response.info.product_list
        })
      },
      // 删除
      handle_delete (index, rows) {
        this.$confirm('确定删除当前用户吗？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '确定删除',
          cancelButtonText: '放弃删除'
        }).then(() => {
          let data = {
            id: rows.id,
            user_id: getCookie('user_id')
          }
          api.system_manage_api.del_user_info(data).then(res => {
            if (res.status === 0) {
              this.$message({
                type: 'success',
                message: '删除成功'
              });
              this.handle_search()
            }
          })
        })
          .catch(action => {
            this.$message({
              type: 'info',
              message: action === 'cancel'
                ? '放弃删除'
                : '确认删除'
            })
          });
      },
      // 新增
      handle_add() {
        this.reset_form()
        this.visibleEdit = true
        this.dailogTitleType = "新增"
      },
      // 编辑
      handle_edit (row) {
        this.visibleEdit = true
        this.dailogTitleType = "编辑"
        // 表单回显
        this.formEdit.user_name = row.user_name
        this.formEdit.user_password = row.user_password
        this.formEdit.user_role_id = row.role_id
        this.formEdit.product_name = row.product_name
        this.id111 = row.id
      },
      // 重置编辑表单
      reset_form () {
        this.formEdit = {
          user_name: '',
          user_password: '',
          user_role_id: '',
          product_name: ''
        }
      },
      // 提交编辑
      submit (form) {
        this.$refs[form].validate(valid => {
          if (valid) {
            let data = {
              id: this.id111,
              user_name: this.formEdit.user_name,
              user_password: this.formEdit.user_password,
              role_id: this.formEdit.user_role_id,
              product_name: this.formEdit.product_name,
              user_id: getCookie('user_id')
            }
            switch (this.dailogTitleType) {
              case "新增":
                api.system_manage_api.add_user_info(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success('成功添加用户！')
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                  }
                  this.visibleEdit = false;
                  this.handleCurrentChange(1)
                });
                break;
              case "编辑":
                api.system_manage_api.update_user_info(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success("修改成功")
                  } else {
                    this.$message.error("系统异常，请联系管理员！")
                  }
                  this.visibleEdit = false
                  this.handleCurrentChange(1)
                });
                break;
            }
          }
        })
      },
    },
    mounted() {
      this.handleCurrentChange(1)
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
