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
            <el-table-column prop="host_ip" align="center" label="ip地址"></el-table-column>
            <el-table-column prop="exec_env" align="center" label="所属环境"></el-table-column>
            <el-table-column prop="host_user" align="center" label="登录用户"></el-table-column>
            <el-table-column prop="host_pwd" align="center" label="登录密码" :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="host_path" align="center" label="执行目录"></el-table-column>
            <el-table-column prop="is_cur_env" align="center" label="当前环境"></el-table-column>
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
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </CardBox>

    <Dialog v-bind:visible="edit_flag" width="600" @closeDialog="close_edit" :title="title+'主机配置'">
      <div slot="con">
        <el-form :model="form" :rules="rules" ref="form" label-width="100px" style="margin-left: 100px" size="mini">
          <el-form-item label="主机ip" prop="host_ip">
            <el-input v-model="form.host_ip" style="width: 50%" size="mini"></el-input>
          </el-form-item>
          <el-form-item label="登录用户" prop="host_user">
            <el-input v-model="form.host_user" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="host_pwd">
            <el-input type="password" v-model="form.host_pwd" style="width: 50%"></el-input>
            <el-button type="primary" size="mini" @click="test_connect" :loading="loading" :disabled="loading">{{execute_button_name}}</el-button>
          </el-form-item>
          <el-form-item label="确认密码" prop="check_host_pwd">
            <el-input type="password" v-model="form.check_host_pwd" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="执行环境" prop="exec_env">
            <el-select v-model="form.exec_env" placeholder="选择主机执行环境">
              <el-option label="开发" value="开发"></el-option>
              <el-option label="测试" value="测试"></el-option>
              <el-option label="生产" value="生产"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="执行目录" prop="host_path">
            <el-input v-model="form.host_path" style="width: 50%"></el-input>
          </el-form-item>
          <el-form-item label="当前环境" prop="is_cur_env">
            <el-select v-model="form.is_cur_env" placeholder="是否设置为当前环境">
              <el-option label="是" value="是"></el-option>
              <el-option label="否" value="否"></el-option>
            </el-select>
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
      let check_host_pwd = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.form.host_pwd) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      }
      return {
        loading: false,
        execute_button_name: '连接验证',
        host_id: '',
        tableData: [],
        title: '',
        edit_flag: false,
        form: {
          host_ip: '',
          exec_env: '',
          host_user: '',
          host_pwd: '',
          host_path: '',
          check_host_pwd: '',
          is_cur_env: ''
        },
        rules: {
          host_ip: [{required: true, message: '请输入主机ip', trigger: 'change'}],
          host_user: [{required: true, message: '请输入登录用户名', trigger: 'change'}],
          exec_env: [{required: true, message: '请选择主机执行环境', trigger: 'change'}],
          host_path: [{required: true, message: '请输入主机执行目录', trigger: 'change'}],
          is_cur_env: [{required: true, message: '请选择是否设置为当前环境', trigger: 'change'}],
          host_pwd: [{required: true, message: '请输入登录密码', trigger: 'change'}],
          check_host_pwd: [
            {required: true, message: '请再次输入密码', trigger: 'change'},
            {validator: check_host_pwd, trigger: 'blur'}
          ],
        },
      }
    },
    methods: {
      // 测试主机连接是否正常
      test_connect() {
        this.loading = true
        this.execute_button_name = '测试连接中'
        let data = {
          host_ip: this.form.host_ip,
          host_user: this.form.host_user,
          host_pwd: this.form.host_pwd
        }
        if (! this.form.host_ip) {
          this.$message.warning('请先输入测试主机ip')
          this.loading = false
          this.execute_button_name = '连接验证'
          return false
        }
        if (! this.form.host_user) {
          this.$message.warning('请先输入测试主机用户名')
          this.loading = false
          this.execute_button_name = '连接验证'
          return false
        }
        if (! this.form.host_pwd) {
          this.$message.warning('请先输入测试主机密码')
          this.loading = false
          this.execute_button_name = '连接验证'
          return false
        }
        api.config_manage_api.test_connect(data).then(response => {
          if (response.status === -2) {
            this.$message.warning('用户名或密码错误，SSH连接失败!')
            this.execute_button_name = '连接验证'
          } else if (response.status === 0) {
            this.$message.success('主机连接成功！')
            this.execute_button_name = '连接成功'
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
          this.loading = false
        })
      },
      // 关闭弹窗
      close_edit() {
        this.edit_flag = false
        this.execute_button_name = '连接验证'
      },
      //查询
      handle_search() {
        let data = {
          user_id: getCookie('user_id')
        };
        api.config_manage_api.query_host_data(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        });
      },
      //删除
      handle_delete(rows) {
        this.$confirm('确定删除？', '提示', {type:"warning"}).then(_ => {
          let data = {
            host_id: rows.host_id,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.delete_host_data(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
              this.handle_search()
            } else {
              this.$message.error('系统异常，请联系管理员！')
            }
          })
        }).catch(_ => {})
      },
      // 编辑
      handle_edit(row) {
        this.host_id = row.host_id
        this.form = {
          host_ip: row.host_ip,
          exec_env: row.exec_env,
          host_user: row.host_user,
          host_pwd: row.host_pwd,
          check_host_pwd: row.host_pwd,
          is_cur_env: row.is_cur_env,
          host_path: row.host_path
        }
        this.title = '编辑'
        this.edit_flag = true
      },
      // 新增
      handle_add() {
        this.host_id = ''
        this.form = {
          host_ip: '',
          exec_env: '',
          host_user: '',
          host_pwd: '',
          check_host_pwd: '',
          is_cur_env: ''
        }
        this.title = '新增'
        this.edit_flag = true
      },
      // 提交表单
      handle_submit(form) {
        this.$refs[form].validate((valid) => {
          if (valid) {
            let data = {
              user_id: getCookie('user_id'),
              host_id: this.host_id,
              host_path: this.form.host_path,
              host_ip: this.form.host_ip,
              exec_env: this.form.exec_env,
              host_user: this.form.host_user,
              host_pwd: this.form.host_pwd,
              is_cur_env: this.form.is_cur_env
            }
            switch (this.title) {
              case "新增":
                api.config_manage_api.add_host_data(data).then(response => {
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
                api.config_manage_api.update_host_data(data).then(response => {
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
      handle_reset(form) {
        this.form = {
          host_ip: '',
          exec_env: '',
          host_user: '',
          host_pwd: '',
          check_host_pwd: '',
          is_cur_env: ''
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
