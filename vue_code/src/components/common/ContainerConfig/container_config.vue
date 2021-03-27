<template>
  <div>
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
            <el-table-column prop="image_name" align="center" label="容器名称"></el-table-column>
            <el-table-column prop="program_dir" align="center" label="容器代码目录"></el-table-column>
            <el-table-column prop="local_program_dir" align="center" label="主机代码目录"></el-table-column>
            <el-table-column prop="result_log_dir" align="center" label="容器结果目录"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="local_log_dir" align="center" label="主机结果目录"></el-table-column>
            <el-table-column prop="svn_dir" align="center" label="svn版本库路径"></el-table-column>
            <el-table-column prop="git_dir" align="center" label="git版本库路径"></el-table-column>
            <el-table-column prop="git_branch_name" align="center" label="git分支名"></el-table-column>
            <el-table-column prop="mark" align="center" label="说明"></el-table-column>
            <el-table-column label="操作" width="190">
              <template slot-scope="scope">
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-delete"
                  style="color: red"
                  @click="handle_delete(scope.row)">
                  删除
                </el-button>
                <el-button
                  type="text"
                  size="mini"
                  icon="el-icon-edit"
                  @click="handle_edit(scope.row)">
                  编辑
                </el-button>
                <el-button type="text" size="mini" icon="el-icon-refresh"
                           class="my_button"
                           @click="handle_code_update(scope.row)"
                           v-loading="loading"
                           :disabled="button_flag"
                           element-loading-text="更新中"
                           element-loading-spinner="el-icon-loading"
                           element-loading-background="white">程序构建</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </CardBox>

    <Dialog v-bind:visible="edit_flag" width="600" @closeDialog="close_edit" :title="title+'容器配置'">
      <div slot="con">
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" style="margin-left: 100px" size="mini">
          <el-form-item label="容器名称" prop="image_name">
            <el-input v-model="form.image_name" style="width: 50%" size="mini"></el-input>
          </el-form-item>
          <el-form-item label="容器代码目录" prop="program_dir">
            <el-input v-model="form.program_dir" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="主机代码目录" prop="local_program_dir">
            <el-input v-model="form.local_program_dir" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="容器结果目录" prop="result_log_dir">
            <el-input v-model="form.result_log_dir" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="主机结果目录" prop="local_log_dir">
            <el-input v-model="form.local_log_dir" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="代码库路径" prop="vcs_type">
            <el-select v-model="form.vcs_type" placeholder="选择代码库" @change="change_vcs" style="width: 50%">
              <el-option label="svn" value="svn"></el-option>
              <el-option label="git" value="git"></el-option>
            </el-select>
          </el-form-item>
          <div v-if="form.vcs_type==='svn'">
            <el-form-item label="svn版本库路径" prop="svn_dir"
                          :rules="[{ required: true, message: '请输入svn版本库路径', trigger: 'blur' }]">
              <el-input v-model="form.svn_dir" style="width: 50%"></el-input>
            </el-form-item>
          </div>
          <div v-else-if="form.vcs_type==='git'">
            <el-form-item label="git版本库路径" prop="git_dir"
                          :rules="[{ required: true, message: '请输入git版本库路径', trigger: 'blur' }]">
              <el-input v-model="form.git_dir" style="width: 50%"></el-input>
            </el-form-item>
            <el-form-item label="git分支名称" prop="git_branch_name"
                          :rules="[{ required: true, message: '请输入git分支名称', trigger: 'blur' }]">
              <el-input v-model="form.git_branch_name" style="width: 50%"></el-input>
            </el-form-item>
          </div>
          <el-form-item label="说明" prop="mark">
            <el-input type="textarea" v-model="form.mark" style="width: 50%"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <div class="dialog__footer">
          <el-button type="primary" plain @click="handle_reset">重置</el-button>
          <el-button type="primary" @click="handle_submit('form')">确认</el-button>
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
        loading: false,
        button_flag: false,
        tableData: [],
        title: '',
        edit_flag: false,
        container_id: '',
        form: {
          vcs_type: '',
          image_name: '',
          program_dir: '',
          local_program_dir: '',
          result_log_dir: '',
          local_log_dir: '',
          svn_dir: '',
          git_dir: '',
          git_branch_name: ''
        },
        rules: {
          image_name: [{required: true, message: '请输入容器名称', trigger: 'blur'}],
          program_dir: [{required: true, message: '请输入容器代码目录', trigger: 'blur'}],
          local_program_dir: [{required: true, message: '请输入主机代码目录', trigger: 'blur'}],
          result_log_dir: [{required: true, message: '请输入容器结果目录', trigger: 'blur'}],
          local_log_dir: [{required: true, message: '请输入主机结果目录', trigger: 'blur'}],
          vcs_type: [{required: true, message: '请选择代码版本库', trigger: 'change'}],
        },
      }
    },
    methods: {
      // 代码更新
      handle_code_update(row) {
        this.loading = true
        this.button_flag = true
        let data = {
          user_id: getCookie('user_id'),
          image_name: row.image_name,
          program_dir: row.program_dir,
          local_program_dir: row.local_program_dir,
          vcs_type: row.vcs_type,
          svn_dir: row.svn_dir,
          git_dir: row.git_dir,
          git_branch_name: row.git_branch_name
        }
        api.config_manage_api.get_docker_data(data).then(response => {
          if (response.status === 0) {
            this.$message.success('容器内代码更新成功！')
          }else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.loading = false
          this.button_flag = false
        })
      },
      // 选择代码版本库
      change_vcs() {
        console.log('vcs', this.form.vcs_type)
      },
      // 关闭弹窗
      close_edit() {
        this.edit_flag = false
      },
      //查询
      handle_search() {
        let data = {
          user_id: getCookie('user_id')
        };
        api.config_manage_api.query_docker_data(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        });
      },
      //删除
      handle_delete(rows) {
        this.$confirm('确定删除？', '提示', {type: "warning"}).then(_ => {
          let data = {
            id: rows.id,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.delete_docker_data(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
              this.handle_search()
            } else {
              this.$message.error('系统异常，请联系管理员！')
            }
          })
        }).catch(_ => {
        })
      },
      // 编辑
      handle_edit(row) {
        this.container_id = row.id
        this.form = {
          vcs_type: row.vcs_type,
          image_name: row.image_name,
          program_dir: row.program_dir,
          local_program_dir: row.local_program_dir,
          result_log_dir: row.result_log_dir,
          local_log_dir: row.local_log_dir,
          svn_dir: row.svn_dir,
          git_dir: row.git_dir,
          git_branch_name: row.git_branch_name,
          mark: row.mark
        }
        this.title = '编辑'
        this.edit_flag = true
        // this.$refs['form'].resetFields()
        console.log(this.form.vcs_type)

      },
      // 新增
      handle_add() {
        this.container_id = ''
        this.form = {
          image_name: '',
          program_dir: '',
          local_program_dir: '',
          result_log_dir: '',
          local_log_dir: '',
          svn_dir: '',
          git_dir: '',
          git_branch_name: '',
          mark: '',
          vcs_type: ''
        }
        this.title = '新增'
        this.edit_flag = true
        this.$refs['form'].resetFields()
      },
      // 提交表单
      handle_submit(form) {
        this.$refs[form].validate((valid) => {
          if (valid) {
            let data = {
              user_id: getCookie('user_id'),
              id: this.container_id,
              image_name: this.form.image_name,
              program_dir: this.form.program_dir,
              local_program_dir: this.form.local_program_dir,
              result_log_dir: this.form.result_log_dir,
              local_log_dir: this.form.local_log_dir,
              vcs_type: this.form.vcs_type,
              svn_dir: this.form.svn_dir,
              git_dir: this.form.git_dir,
              git_branch_name: this.form.git_branch_name,
              mark: this.form.mark
            }
            switch (this.title) {
              case "新增":
                api.config_manage_api.add_docker_data(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success('新增成功！')
                    this.edit_flag = false
                    this.handle_search()
                  } else if (response.status === -2) {
                    this.$message.error(response.info)
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                  }
                });
                break;
              case "编辑":
                api.config_manage_api.update_docker_data(data).then(response => {
                  if (response.status === 0) {
                    this.$message.success('编辑成功！')
                    this.edit_flag = false
                    this.handle_search()
                  } else if (response.status === -2) {
                    this.$message.error(response.info)
                  } else {
                    this.$message.error('系统异常，请联系管理员！')
                  }
                });
                break;
            }
          }
        })
      },
      // 重置表单
      handle_reset() {
        this.form = {
          image_name: '',
          program_dir: '',
          local_program_dir: '',
          result_log_dir: '',
          local_log_dir: '',
          svn_dir: '',
          git_dir: '',
          git_branch_name: '',
          mark: '',
          vcs_type: ''
        }
      }
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
<style>
   .my_button .el-loading-mask .el-loading-spinner .el-loading-text {
    font-size: 10px !important;
  }
</style>
