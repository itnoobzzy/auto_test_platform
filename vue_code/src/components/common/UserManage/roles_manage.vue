<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="角色ID">
            <el-input placeholder="请输入角色ID" clearable v-model="search_input.role_id" size="mini">
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
            :data="tableData.slice((currentPage-1)*pageSize, pageSize)"
            border
            ref="selection"
            style="width: 100%">
            <el-table-column prop="role_id" label="角色ID" width="100px" align="center"></el-table-column>
            <el-table-column prop="role_name" label="角色名称" align="center"></el-table-column>
            <el-table-column prop="role_desc" label="角色描述" align="center"></el-table-column>
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
              :total="tableData.length">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>
    <Dialog v-bind:visible="visibleEdit" width="600" @closeDialog="close_dialog" :title="dailogTitleType+'角色'">
      <div slot="con">
        <el-form :model="formEdit" label-width="140px" :rules="rules" ref="formEdit">
          <el-form-item label="角色ID" prop="role_id">
            <el-input
              placeholder="请输入角色ID"
              v-model="formEdit.role_id"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="角色名称" prop="role_name">
            <el-input
              placeholder="请输入角色名称"
              v-model="formEdit.role_name"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item label="角色描述" prop="role_desc">
            <el-input
              placeholder="请输入角色描述"
              v-model="formEdit.role_desc"
              style="width:225px"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="bind_privileges('formEdit')">绑定权限</el-button>
          </el-form-item>
          <div v-if="treeShow">
            <el-row type="flex">
              <el-col :span="12" style="border-right: 1px solid #DCDFE6; margin-right: 15px">
                <div>
                  <el-tree
                    @check-change='treeData'
                    :data="menuData"
                    show-checkbox
                    :check-strictly="true"
                    default-expand-all
                    node-key="menu_id"
                    ref="tree"
                    highlight-current
                    :props="defaultProps">
                  </el-tree>
                </div>
              </el-col>
              <el-col :span="12">
                <div>
                  <el-form inline label-position="left">
                    <el-form-item v-for="tag in tags" :key="tag.menu_id" style="margin: 0 5px">
                      <el-tag
                        :type="tag.type">
                        {{tag.menu_name}}
                      </el-tag>
                    </el-form-item>
                  </el-form>
                </div>
              </el-col>
            </el-row>
          </div>
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
      // let check_id = (result, value, callback) => {
      //   let data = {
      //     role_id: value
      //   }
      //   api.system_manage_api.query_role_id(data).then(response => {
      //     if (response.info === '存在') {
      //       this.$message.warning('该角色ID已存在！')
      //       callback(new Error('该角色ID已存在！'))
      //     }
      //   })
      //   callback()
      // }

      return {
        tableData: [],
        currentPage: 1,
        pageSize: 10,

        search_input: {
          role_id: ''
        },

        dailogTitleType: "",
        visibleEdit: false,

        menuData: [],
        menu_id: [],
        defaultProps: {
          children: 'children_info',
          label: 'menu_name'
        },
        tags: [],
        treeShow: false,

        rules: {
          role_id: [
            {required: true, message: '角色代码不能为空', trigger: 'blur'},
            // {validator: check_id, trigger: 'change'}
          ],
          role_name: [{
            required: true, message: '角色名称不能为空', trigger: 'blur'
          }]
        },
        formEdit: {
          role_id: '',
          role_name: '',
          role_desc: ''
        },
      }
    },
    methods: {
      handleSizeChange (size) {
        this.pageSize = size
      },
      handleCurrentChange (val) {
        this.currentPage = val
      },
      close_dialog () {
        this.visibleEdit = false
      },
      // 重置搜索框
      reset_search () {
        this.search_input = {
          role_id: ''
        }
        this.handleCurrentChange(1)
      },
      // 查询测试结果表数据
      handle_search () {
        let data = {
          role_id: this.search_input.role_id,
          user_id: getCookie('user_id')
        }
        api.login_out_api.query_role_authority(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 删除
      handle_delete (index, rows) {
        this.$confirm('确定删除当前角色吗？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '确定删除',
          cancelButtonText: '放弃删除'
        }).then(() => {
          let data = {
            role_id: getCookie('user_role_id')
          }
          api.system_manage_api.delete_role_authority(data).then(res => {
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
        this.tags = []
        this.treeShow = false
        this.formEdit.role_id = row.role_id
        this.formEdit.role_name = row.role_name
        this.formEdit.role_desc = row.role_desc
        this.menu_id = row.menu_id_list
        this.visibleEdit = true
        this.dailogTitleType = "编辑"
      },
      // 绑定权限
      bind_privileges(formName) {
        this.$refs[formName].validate(valid => {
          if (valid) {
            this.treeShow = true
            let data = {
              user_role_id: this.formEdit.role_id
            }
            api.system_manage_api.query_menu_info(data).then(response => {
              if (response.status === 0) {
                this.menuData = response.info
                let data = {
                  role_id: this.formEdit.role_id,
                }
                api.login_out_api.query_role_authority(data).then(res1 => {
                  this.$refs.tree.setCheckedKeys(res1.info[0].menu_id_list);
                  this.tags = this.$refs.tree.getCheckedNodes()
                })
              } else {
                this.$message.error('系统异常，请联系管理员！')
              }
            })
          }
        })
      },
      // 重置编辑表单
      reset_form () {
        this.formEdit = {
          user_name: '',
          user_password: '',
          role_id: '',
          product_name: ''
        }
        if (this.tags.length !== 0) {
          this.$refs.tree.setCheckedKeys([])
        }
      },
      // 提交编辑
      submit (form) {
        this.$refs[form].validate(valid => {
          if (valid) {
            let data = {
              id: this.formEdit.role_id,
              role_id: this.formEdit.role_id,
              role_name: this.formEdit.role_name,
              role_desc: this.formEdit.role_desc,
              menu_id_list: this.menu_id,
              user_id: getCookie('user_id')
            }
            switch (this.dailogTitleType) {
              case "新增":
                api.system_manage_api.add_role_authority(data).then(response => {
                  if (response.status === 0 && response.info !== '此角色已存在') {
                    this.$message.success('添加成功！')
                    this.visibleEdit = false;
                    this.handleCurrentChange(1)
                  } else if (response.info === '此角色已存在'){
                    this.$message.warning('此角色ID已存在！')
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                    this.visibleEdit = false;
                    this.handleCurrentChange(1)
                  }
                });
                break;
              case "编辑":
                api.system_manage_api.update_role_authority(data).then(response => {
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
      treeData() {
        this.tags = this.$refs.tree.getCheckedNodes();
        console.log('menu_id', this.$refs.tree.getCheckedKeys())
        this.menu_id = this.$refs.tree.getCheckedKeys();
      },
    },
    mounted() {
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
