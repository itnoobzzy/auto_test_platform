<!--  -->
<template>
  <el-tabs v-model="activeName" type="card" class="import-tab">
    <el-tab-pane label="导入" name="first">
      <div>
        <el-button type="warning" @click.native.prevent="handle_import()" size="mini" style="float: right;" icon="el-icon-top" round>导入</el-button>
        <el-button type="info" @click.native.prevent="template_download()" size="mini" style="float: right;" icon="el-icon-message" round>模板下载</el-button>
      </div>
      <el-upload
        class="upload-demo"
        drag
        multiple
        ref="upload"
        action="config_manage/batch_import_case/"
        :before-upload="beforeUpload"
        :on-success="uploadSuccess"
        :file-list="file_list"
        :data="{user_name: user_name}"
        :auto-upload="false">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          点击或将文件拖拽到这里,或<em>点击</em>上传
        </div>
        <div class="el-upload__text text2">提示:仅支持excel格式文件</div>
      </el-upload>
    </el-tab-pane>
    <el-tab-pane label="导出" name="second">
      <div>
        <el-row>
          <el-row>
            <el-col :span="10" class="fl">
              <el-col :span="12">
                <el-input
                  v-model="search_input.template_name"
                  clearable
                  placeholder="请输入测试模板名称"
                  suffix-icon="el-icon-search">
                </el-input>
              </el-col>
              <el-col :span="12">
                <el-button class="com-btn btn-white mgl-30" @click="handle_reset(1)">重置</el-button>
                <el-button type="primary"  class="com-btn" @click="handle_search(1)">查询</el-button>
              </el-col>
            </el-col>
            <el-col :span="8" class="fr tr">
              <el-button type="primary" class="com-btn" icon="el-icon-delete" @click="handle_delete('all')">删除所有模板配置</el-button>
              <el-button type="primary" class="com-btn" icon="el-icon-folder-add"
                         @click="handle_export('all')"
                         v-loading="fullscreenLoading"
                         element-loading-text="正在导出，请稍后。。。。"
                         element-loading-spinner="el-icon-loading"
                         element-loading-background="rgba(0, 0, 0, 0.8)"
                         v-loading.fullscreen.lock="fullscreenLoading"
              >全部导出</el-button>
            </el-col>
          </el-row>
          <el-table
            :data="template_table_data"
            border
            ref="selection"
            @selection-change="handle_selection_change"
            style="width: 100%"
            align="center"
            class="mgt-25">
            <el-table-column
              type="selection"
              width="60">
            </el-table-column>
            <el-table-column
              prop="module_name"
              label="测试模板名称">
            </el-table-column>
            <el-table-column
              prop="module_type"
              label="测试模板分类">
            </el-table-column>
            <el-table-column
              prop="create_time"
              label="创建时间">
            </el-table-column>
            <el-table-column
              prop="author"
              label="创建者">
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page.sync="currentPage"
              :page-sizes="[5, 10, 15, 20]"
              :page-size="pageSize"
              layout="sizes, prev, pager, next"
              :total="total_count"
              class="mgt-30 fr">
            </el-pagination>
          </div>
        </el-row>
        <el-row class="mgt-25">
          <div class="opSetting tc">
            <div @click="bind_data">
              <el-button :disabled="!selected_list.length" size="mini" type="primary" >
                选中<i class="el-icon-arrow-down"></i>
              </el-button>
            </div>
          </div>
        </el-row>
        <el-row class="mgt-30 clearfix">
          <el-row>
            <el-col :span="8" class="fr tr">
              <el-button type="primary" class="com-btn" @click="handle_delete('choose')">删除选中配置</el-button>
              <el-button type="primary" class="com-btn" @click="handle_export('choose')">导出选中模板</el-button>
            </el-col>
          </el-row>
          <el-table
            :data="choose_template_table_data"
            border
            ref="selection"
            class="mgt-30"
            align="center"
            style="width: 100%">
            <el-table-column
              prop="module_name"
              label="测试模板名称">
            </el-table-column>
            <el-table-column
              prop="module_type"
              label="测试模板分类">
            </el-table-column>
            <el-table-column
              prop="create_time"
              label="创建时间">
            </el-table-column>
            <el-table-column
              prop="author"
              label="创建者">
            </el-table-column>
            <el-table-column
              prop=""
              label="操作">
              <template slot-scope="scope">
                <el-button @click.native.prevent="delete_row(scope.$index,scope.row)" type="text" size="small">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-row>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
  import {getCookie} from "../../../service/cookie";
  import api from "../../../service/api";

  export default {
    data () {
      return {
        user_name: getCookie('user_name'),
        loading: false,
        fullscreenLoading:false,
        user_id: getCookie('user_id'),
        file_list: [],
        activeName: 'second',
        // 未选中模板列表
        template_table_data: [],
        currentPage: 1,
        pageSize: 10,
        total_count: 0,
        // 选中模板列表
        choose_template_table_data: [],
        selected_list: [],
        // 查询模板
        search_input: {
          template_name: ''
        }
      }
    },

    methods: {
      // 导入模板下载
      template_download() {
        let data = {
          user_id: getCookie('user_id'),
        }
        api.config_manage_api.download_template(data).then(response => {
            window.open(response)
        })
      },
      // 勾选
      handle_selection_change(val) {
        this.selected_list = val
      },
      // 去重
      de_weight (arr, key) {
        let ret = []
        arr.forEach((item) => {
          let compare = []
          ret.forEach((retitem) => {
            compare.push(retitem[key])})
          if (compare.indexOf(item[key]) === -1) {
            ret.push(item)
          }
        })
        return ret
      },
      // 选中
      bind_data() {
        this.selected_list.forEach(item => {
          this.choose_template_table_data.push(item)
        })
        this.choose_template_table_data = this.de_weight(this.choose_template_table_data, 'case_template_id')
      },
      // 取消选中
      delete_row(index) {
        this.choose_template_table_data.splice(index, 1)
      },
      // 校验上传文件格式
      beforeUpload(file) {
        let file_ext = file.name.replace(/.+\./, "")
        let types = ['xlsx','xls']
        if (types.indexOf(file_ext.toLowerCase()) === -1) {
          this.$message.warning('请上传Excel格式附件')
          this.$refs.upload.clearFiles()
        } else {
          this.loading = this.$loading({
            lock: true,
            text: '正在导入中...',
            spinner: 'el-icon-loading'
          })
        }
      },
      // 上传文件成功
      uploadSuccess(response){
        this.loading.close();
        setTimeout(() => {
          if (response.status === 0) {
            this.$message.success(response.info)
          } else {
            this.$message.error(response.info)
          }
        }, 500);
        this.$refs.upload.clearFiles();
      },
      // 导入
      handle_import() {
        this.$refs.upload.submit()
      },
      // 导出
      handle_export(op) {
        let template_list = []
        if (op === 'choose') {
          if (this.choose_template_table_data.length === 0) {
            this.$message.warning('请先选中需要导出的模板！')
            return false
          }
          this.choose_template_table_data.forEach(item => {
            template_list.push(item.case_template_id)
          })
        }
        // 大于30条数据，进行下载提示
        if (template_list.length > 30) {
          this.$message.success('数据量较大，正在下载中，请稍后...')
        }
        this.fullscreenLoading = true
        let data = {
          template_id_list: template_list,
          product_name: getCookie('product_name')
        }
        api.config_manage_api.batch_export_case(data).then(response => {
          this.fullscreenLoading = false
          if (response.status === 400) {
            this.$message.error(response.info)
          } else {
            window.open(response)
          }
        })
      },
      // 删除模板
      handle_delete(op) {
        let template_list = []
        switch (op) {
          case 'choose':
            // 删除选中模板
            if (this.choose_template_table_data.length === 0) {
              this.$message.warning('请先选择要删除的模板配置！')
            } else {
              this.choose_template_table_data.forEach(item => {
                template_list.push(item.case_template_id)
              })
              let data = {
                template_id_list: template_list,
                product_name: getCookie('product_name')
              }
              api.config_manage_api.batch_delete_case(data).then(response => {
                if (response.status === 0) {
                  this.handle_search()
                  this.$message.success('配置模板删除成功！')
                } else {
                  this.$message.error('系统异常，请联系管理员！')
                }
                this.choose_template_table_data = []
              })
            }
            break
          case 'all':
            let data = {
              user_id: getCookie('user_id')
            }
            api.config_manage_api.delete_all_case(data).then(response => {
              if (response.status === 0) {
                this.$message.success('配置删除成功！')
              } else {
                this.$message.error('系统异常，请联系管理员！')
              }
            })
        }
      },
      // 查询模板
      handle_search() {
        let data = {
          page:this.currentPage,
          pageSize:this.pageSize,
          module_name:this.search_input.template_name,
          user_id: getCookie('user_id'),
          product_name: getCookie('product_name'),
        }
        api.config_manage_api.check_case_template(data).then(response => {
          if (response.status === 0) {
            this.template_table_data = response.info.ret_info
            this.total_count = response.info.total_count
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      handleSizeChange(size){
        this.pageSize=size
        this.handle_search()
      },
      handleCurrentChange(val){
        this.currentPage=val
        this.handle_search()
      },
      handle_reset() {
        this.search_input.template_name = ''
        this.handleCurrentChange(1)
      }
    },

    mounted() {
      this.handleCurrentChange(1)
    }
  }

</script>
<style lang='scss'>
  @import '../../../styles/import.scss';
</style>
