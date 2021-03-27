<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="运营省份">
            <el-select
              size="small"
              v-model="search_input.prov_name"
              placeholder="请选择">
              <el-option
                v-for="item in options.prov_list"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="参数">
            <el-select
              size="small"
              v-model="search_input.param_val"
              placeholder="请选择">
              <el-option
                v-for="item in options.param_list"
                :key="item.param_name"
                :label="item.param_name"
                :value="item.param_name">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="月份">
            <el-date-picker value-format="yyyyMM" v-model="search_input.month" size="mini" type="month"
                            placeholder="选择月份">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" plain style="background:none" @click="handle_reset('search')">重置
            </el-button>
            <el-button type="primary" size="small" @click="handleCurrentChange(1)">查询</el-button>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <div slot="extral">
        <el-tooltip class="item" effect="light" content="点击收集当月运营数据" placement="top">
          <el-button type="primary" size="mini" round style="margin-left: 1rem" @click="collect_operate_data">收集<i
            class="el-icon-download el-icon--right"></i></el-button>
        </el-tooltip>
        <el-button type="primary" size="mini" plain @click="newAdd" style="float: left;margin-left: 1rem">新增</el-button>
        <el-button type="warning" size="mini" plain icon="el-icon-upload2" @click="batch_flag = true">导入</el-button>
        <el-button type="warning" size="mini" plain icon="el-icon-download" @click="open_export_dialog">导出</el-button>
      </div>
      <template slot="body">
        <div class="table mgt-10">
          <el-table
            :data="tableData"
            border
            ref="selection"
            style="width: 100%">
            <el-table-column prop="product_name" align="center" label="产品名称"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="product_ver" align="center" label="版本号"
                             :show-overflow-tooltip="true"></el-table-column>
            <el-table-column prop="operate_month" label="月份" align="center"></el-table-column>
            <el-table-column prop="prov_name" label="运营省份" align="center"></el-table-column>
            <el-table-column prop="prov_type" label="省份类型" align="center"></el-table-column>
            <el-table-column prop="operative_index" label="运营数据类型" align="center"></el-table-column>
            <el-table-column
              prop="operative_sub_index"
              align="center"
              label="运营数据名称"
              show-overflow-tooltip>
              <template slot-scope="scope">
                <p v-if="!scope.row.update_flag">{{ scope.row.operative_sub_index }}</p>
                <el-input
                  class="table_ipt"
                  v-model="scope.row.operative_sub_index"
                  size="mini"
                  placeholder="请输入运营数据名称"
                  v-else
                ></el-input>
              </template>
            </el-table-column>
            <el-table-column label="当月数据" align="center">
              <template slot-scope="scope">
                <p v-if="!scope.row.update_flag">{{ scope.row.operate_data }}</p>
                <el-input
                  class="table_ipt"
                  v-model="scope.row.operate_data"
                  size="mini"
                  placeholder="请输入子运营数据值"
                  v-else
                ></el-input>
              </template>
            </el-table-column>
            <el-table-column label="当月目标值" align="center">
              <template slot-scope="scope">
                <p v-if="!scope.row.update_flag">{{ scope.row.target_value }}</p>
                <el-input
                  class="table_ipt"
                  v-model="scope.row.target_value"
                  placeholder="请输入当月目标值"
                  size="mini"
                  v-else
                ></el-input>
              </template>
            </el-table-column>
            <el-table-column label="单位" align="center">
              <template slot-scope="scope">
                <p v-if="!scope.row.update_flag">{{ scope.row.units }}</p>
                <el-input
                  class="table_ipt"
                  v-model="scope.row.units"
                  size="mini"
                  placeholder="请输入单位"
                  v-else
                ></el-input>
              </template>
            </el-table-column>
            <el-table-column
              prop="operate_desc"
              label="运营数据描述"
              align="center"
              show-overflow-tooltip>
            </el-table-column>
            <el-table-column align="center" label="是否展示" :show-overflow-tooltip="true">
              <template slot-scope="scope">
                <el-switch
                  v-model="scope.row.show_flag"
                  @click.native.prevent="save_update(scope.$index,scope.row)"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  active-value="是"
                  inactive-value="否">
                </el-switch>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button @click.native.prevent="delete_row(scope.$index,scope.row)" type="text" size="small"><u>删除</u>
                </el-button>
                <el-button v-if="!scope.row.update_flag" @click.native.prevent="update_row(scope.$index,scope.row)"
                           type="text" size="small"><u>修改</u></el-button>
                <el-button v-else @click.native.prevent="save_update(scope.$index,scope.row)" type="text" size="small">
                  <u style="color: #ff4d51">保存</u></el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page.sync="currentPage"
              :page-sizes="[5, 10, 15]"
              :page-size="pageSize"
              layout="sizes, prev, pager, next"
              :total="total_count">
            </el-pagination>
          </div>
        </div>
      </template>
    </CardBox>

    <Dialog
      :visible="batch_flag"
      width="50%"
      title="批量导入运营数据"
      @closeDialog="batch_flag=false">
      <div slot="con">
        <el-row>
          <el-button type="info" @click="template_download()" size="mini" style="margin: auto;" icon="el-icon-message"
                     round>模板下载
          </el-button>
        </el-row>
        <div style="text-align: center">
          <el-upload class="upload-demo" drag
                     multiple
                     ref="upload"
                     action="operate_data_config/import_operate_data/"
                     :before-upload="beforeUpload"
                     :on-success="uploadSuccess"
                     :file-list="fileList"
                     :auto-upload="false">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击</em>
              <br>
              <span style="color: red">提示:只能上传Excel格式文件</span>
            </div>
          </el-upload>
        </div>
      </div>
      <div slot='footer'>
        <div class="dialog__footer">
          <el-button type="primary" plain @click="handle_close">取消</el-button>
          <el-button type="primary" @click="leading_in()">导入</el-button>
        </div>
      </div>
    </Dialog>

    <Dialog
      :visible.sync="export_flag"
      @closeDialog="export_flag=false"
      width="50%"
      center
      title="导出运营数据">
      <div slot="con">
        <el-form :model="export_form" label-width="180px">
          <el-form-item size='mini' label="导出月份:" prop="operate_month">
            <el-select v-model="export_form.operate_month" placeholder="请选择">
              <el-option
                v-for="item in month_options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <el-footer slot="footer">
        <el-button type="primary" @click="export_operate_data" plain size="mini" style="margin: auto auto">导出
        </el-button>
      </el-footer>
    </Dialog>

    <Dialog
      :visible="add_flag"
      :width="'800'"
      center
      @closeDialog="add_flag=false"
      title="新增运营数据">
      <div slot="con">
        <el-form :model="form" label-width="100px" :rules="rules" ref="form" :inline="true">
          <el-form-item label="运营省份" prop="add_prov_name">
            <el-autocomplete
              size="mini"
              class="inline-input"
              v-model="form.add_prov_name"
              :fetch-suggestions="querySearch"
              placeholder="请输入运营省份"
              @select="handleSelect"
            ></el-autocomplete>
          </el-form-item>
          <el-form-item label="省份类型" prop="add_prov_type">
            <el-select style="width: 180px" v-model="form.add_prov_type" placeholder="请选择" size="mini">
              <el-option v-for="item in form.prov_type_sel" :label="item.name" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="数据类型" prop="select_param">
            <el-select @change="click_select_param" multiple style="width: 180px" v-model="form.select_param"
                       placeholder="请选择" size="mini">
              <el-option v-for="(item,index) in options.param_list" :label="item.param_name"
                         :value="index"></el-option>
            </el-select>
            <el-button type="primary" size="small" plain class="optionBtn" @click="param_input_flag = true">添加类型
            </el-button>
          </el-form-item>
          <el-form-item label="月份" prop="add_month">
            <el-date-picker value-format="yyyyMM" v-model="form.add_month" size="mini" type="month"
                            placeholder="选择月份">
            </el-date-picker>
          </el-form-item>
        </el-form>
        <div class="table mgt-10">
          <el-table
            :data="form.param_table.slice((form_current_page - 1) * form_page_size, form_page_size)"
            border
            ref="selection"
            style="width: 100%"
            align="center">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="param_name" label="类型名称"></el-table-column>
            <el-table-column prop="p_cname" label="运营数据名称" show-overflow-tooltip>
              <template slot-scope="scope">
                <el-input v-if="scope.row.flag" style="width: 90px" v-model="scope.row.operative_sub_index" size="mini"
                          placeholder="请输入内容"></el-input>
                <span v-else>{{scope.row.operative_sub_index}}</span>
              </template>
            </el-table-column>
            <el-table-column prop="operate_data" align="center" label="当月数据值">
              <template slot-scope="scope">
                <el-input style="width: 70px" v-model="scope.row.operate_data" size="mini"
                          placeholder="请输入"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="operate_data" label="当月目标值">
              <template slot-scope="scope">
                <el-input style="width: 70px" v-model="scope.row.target_value" size="mini" placeholder="请输入"></el-input>
              </template>
            </el-table-column>
            <el-table-column align="center" label="单位">
              <template slot-scope="scope">
                <el-input v-if="scope.row.flag" style="width: 70px" v-model="scope.row.units" size="mini"
                          placeholder="单位"></el-input>
                <span v-else>{{scope.row.units}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" label="运营数据描述" show-overflow-tooltip>
              <template slot-scope="scope">
                <el-input v-if="scope.row.flag" type="textarea" autosize v-model="scope.row.operate_desc" size="mini"
                          placeholder="请输入内容"></el-input>
                <span v-else>{{scope.row.operate_desc}}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" label="是否展示" :show-overflow-tooltip="true">
              <template slot-scope="scope">
                <el-switch
                  v-model="scope.row.show_flag"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  active-value="是"
                  inactive-value="否">
                </el-switch>
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button @click.native.prevent="updateDesc(scope.$index,scope.row)" type="text" size="small">
                  <u>编辑</u></el-button>
                <el-button @click.native.prevent="deleteDesc(scope.$index,scope.row)" type="text" size="small"><u>移除</u>
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="search_pagination tr">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page.sync="form_current_page"
              :page-sizes="[5, 10, 15]"
              :page-size="form_page_size"
              layout="sizes, prev, pager, next"
              :total="form.param_table.length">
            </el-pagination>
          </div>
        </div>
      </div>
      <div slot='footer'>
        <div class="dialog__footer">
          <el-button type="primary" plain @click="handle_reset('from')">重置</el-button>
          <el-button type="primary" @click="add_save">确认</el-button>
        </div>
      </div>
    </Dialog>

    <Dialog
      :visible.sync="param_input_flag"
      @closeDialog="param_input_flag=false"
      center
      title="添加运营数据类型">
      <div slot="con">
        <el-form :model="param_input_data" label-width="180px" ref="param_input_data" :rules="param_input_data_rules">
          <el-form-item size='mini' label="数据类型名称:" prop="param_name">
            <el-input v-model="param_input_data.param_name" placeholder="请输入数据类型名称"></el-input>
          </el-form-item>
          <el-form-item size='mini' label="运营数据个数:" prop="cont">
            <el-select @change="newparam_add" v-model="param_input_data.cont" placeholder="请选择个数">
              <el-option v-for="item in 10" :key="item" :label="item" :value="item"></el-option>
            </el-select>
          </el-form-item>
          <div v-for="(item, index) in param_input_data.subparam_info">
            <el-form-item size='mini' label="运营数据名称:" :rules="{required: true, message: '运营数据名称不能为空', trigger: 'blur'}">
              <el-input v-model="item.operative_sub_index" placeholder="请输入运营数据名称"></el-input>
            </el-form-item>
            <el-form-item size='mini' label="运营数据单位:" :prop="item.units" :rules="{required: true, message: '运营数据单位不能为空', trigger: 'blur'}">
              <el-input v-model="item.units" placeholder="请输入运营数据单位"></el-input>
            </el-form-item>
            <el-form-item type="textarea" size='mini' label="运营数据描述:" :prop="item.operate_desc" :rules="{required: true, message: '运营数据描述不能为空', trigger: 'blur'}">
              <el-input v-model="item.operate_desc" placeholder="请输入运营数据描述"></el-input>
            </el-form-item>
            <el-form-item type="textarea" size='mini' label="当月运营目标值:" :prop="item.target_value" :rules="{required: true, message: '当月运营目标值不能为空', trigger: 'blur'}">
              <el-input v-model="item.target_value" placeholder="请输入当月运营目标值"></el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>
      <div slot='footer'>
        <div class="dialog__footer">
          <el-button type="primary" plain @click="param_input_flag = false">取消</el-button>
          <el-button type="primary" @click="add_param_click">保存</el-button>
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
      Dialog: () => import('@/components/common/Dialog')
    },
    data() {
      return {
        product_name: '',
        // 查询
        search_input: {
          month: '',
          prov_name: '',
          param_val: ''
        },
        options: {
          prov_list: [],
          param_list: []
        },
        // 表格
        tableData: [],
        currentPage: 1,
        pageSize: 5,
        total_count: 0,
        // 增加运营配置表单
        form: {
          prov_list: [],
          month: '',
          add_prov_type: '',
          add_prov_name: '',
          add_month: '',
          select_param: [],
          param_table: [],
          show_flag: '',
          prov_type_sel: [{value: 1, name: "研发项目"}, {value: 2, name: "商务项目"}]
        },

        // 批量导入
        batch_flag: false,
        fileList: [],
        loading: false,
        // 导出
        export_form: {
          operate_month: ''
        },
        month_options: [{
          value: '',
          label: '所有'
        }],
        export_flag: false,
        // 新增
        param_input_flag: false,
        param_input_data: {param_name: "", cont: 0, subparam_info: []},
        prov_input_flag: false,
        add_flag: false,
        rules: {
          add_prov_name: [{required: true, message: '运营省份不能为空', trigger: 'blur'}],
          add_prov_type: [{required: true, message: '省份类型不能为空', trigger: 'change'}],
          select_param: [{ required: true, message: '请选择参数',trigger: 'change'}],
          add_month: [{required: true, message: '月份不能为空', trigger: 'change'}]
        },
        form_page_size: 5,
        form_current_page: 1,
        // 新增参数
        param_input_data_rules: {
          param_name: [{ required: true, message: '参数名称不能为空',trigger: 'change'}],
          cont: [{ required: true, message: '参数个数不能为空',trigger: 'change'}],
        }
      }
    },
    methods: {
      // 收集运营数据
      collect_operate_data() {
        let data = {
          product_name: getCookie('product_name')
        }
        api.operate_data_api.get_prov_operate_data(data).then(res => {
          if (res.status === 0){
            this.$message.success('数据收集成功，可至数据运营展示界面查看！')
          }else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 选择运营省份
      handleSelect(item) {
        this.form.add_prov_name = item.value
        console.log('form.add_prov_name', this.form.add_prov_name)
      },
      querySearch(queryString, cb) {
        let prov_name = this.options.prov_list
        let results = queryString ? prov_name.filter(this.createFilter(queryString)) : prov_name;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (prov_name) => {
          return (prov_name.value.indexOf(queryString) > -1);
        };
      },
      // 分页
      handleSizeChange(size) {
        if (this.add_flag) {
          this.form_page_size = size
        } else {
          this.pageSize = size
          this.handle_search()
        }
      },
      handleCurrentChange(val) {
        if (this.add_flag) {
          this.form_current_page = val
        } else {
          this.currentPage = val
          this.handle_search()
        }
      },
      // 查询
      handle_search() {
        let data = {
          page: this.currentPage,
          pageSize: this.pageSize,
          product_name: this.product_name,
          operative_index: this.search_input.param_val,
          prov_name: this.search_input.prov_name,
          operate_month: this.search_input.month
        }
        console.log('data', data)
        api.operate_data_api.get_operate_data_info(data).then(response => {
          if (response.status === 0) {
            this.tableData = response.info.ret_info
            this.total_count = response.info.total_count
            this.tableData.forEach(item => {
              item.update_flag = false
            })
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }

        })
      },
      // 重置
      handle_reset(op) {
        switch (op) {
          case 'search':
            this.search_input = {
              month: '',
              prov_name: '',
              param_val: ''
            }
            this.handleCurrentChange(1)
            break

        }

      },
      get_area_list() {
        let data = {
          product_name: this.product_name
        }
        api.operate_data_api.get_area_prov_list(data).then(response => {
          if (response.status === 0) {
            this.form.prov_list = response.info.ret_info.prov_name
            this.options.prov_list = response.info.ret_info.prov_name.map(item => {
              return {value: item, label:item}
            })
            this.options.param_list = response.info.ret_info.param_list
            this.handleCurrentChange(1)
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 删除
      delete_row(index, rows) {
        this.$confirm('是否删除该运营配置？', '确认信息', {type: "warning"}).then(() => {
          let data = {
            id: rows.id
          }
          api.operate_data_api.delete_operate_data_info(data).then(response => {
            if (response.status === 0) {
              this.$message.success('删除成功！')
            } else {
              this.$message.error('删除失败，系统异常，请联系管理员！')
            }
            this.handleCurrentChange(1);
          })
        }).catch(_ => {
        })

      },
      // 更新参数
      update_row(index, rows) {
        this.tableData[index].update_flag = true;
        this.$set(this.tableData, index, rows)
      },
      // 保存更新
      save_update(index, rows) {
        if (rows.operative_sub_index === '' || rows.operate_data === '' || rows.units === '') {
          this.$message.warning('参数信息不能为空！')
        } else {
          let data = {
            id: rows.id,
            operative_sub_index: rows.operative_sub_index,
            operate_month: rows.operate_month,
            operate_data: rows.operate_data,
            prov_type: rows.prov_type,
            product_name: rows.product_name,
            show_flag: rows.show_flag,
            target_value: rows.target_value,
            operative_index: rows.operative_index,
            prov_name: rows.prov_name,
            units: rows.units,
            user_id: getCookie('user_id')
          }
          api.operate_data_api.update_operate_data_info(data).then(response => {
            if (response.status === 0) {
              this.tableData[index].update_flag = false
              this.$set(this.tableData, index, rows)
            } else {
              this.$message.error('系统异常，请联系管理员！')
            }
            this.get_area_list()
          })
        }
      },

      handleSelectionChange(val) {
        this.sync_info_option = val;
      },
      clean_sync_info_option() {
        this.sync_info_option = [];
        this.sync_op = false
      },
      // 提交同步信息
      commit_sync_info() {
        let data = {
          info: this.sync_info_option
        }
        api.operate_data_api.commit_sync_info(data).then(response => {
          if (response.status === 0) {
            this.sync_op = false
            this.sync_info_option = []
            this.$message.success('同步成功！')
          } else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 批量导入
      beforeUpload(file) {
        let FileExt = file.name.replace(/.+\./, "");
        let types = ['xlsx', 'xls'];
        if (types.indexOf(FileExt.toLowerCase()) === -1) {
          alert('请上传Excel附件')
          this.$refs.upload.clearFiles();
        } else {
          this.loading = this.$loading({
            lock: true,
            text: '正在导入中...',
            spinner: 'el-icon-loading',
          });
        }
      },
      uploadSuccess(response, file, fileList) {
        this.loading.close()
        setTimeout(() => {
          this.$message.success(response.info)
        }, 500)
        this.batch_flag = false
        this.$refs.upload.clearFiles()
      },
      leading_in() {
        this.$refs.upload.submit()
      },
      template_download() {
        let data = {
          user_id: getCookie('user_id')
        }
        api.operate_data_api.download_operate_template(data).then(response => {
          window.open(response);
        })
      },
      handle_close() {
        this.fileList = []
        this.batch_flag = false
      },
      // 打开导出运营数据弹框
      open_export_dialog() {
        this.month_options = [
          {
            value: '',
            label: '所有'
          }
        ]
        let data = {
          user_id: getCookie('user_id')
        }
        api.operate_data_api.get_operate_month(data).then(res => {
          res.info.forEach(item => {
            this.month_options.push(item)
          })
        })
        this.export_form.operate_month = ""
        this.export_flag = true
      },
      // 导出运营数据
      export_operate_data() {
        let data = {
          operate_month: this.export_form.operate_month
        }
        api.operate_data_api.export_operate_data(data).then(res => {
          window.open(res)
          this.$message.success('运营数据导出成功')
        })
        this.export_flag = false
        this.options = [{
          value: '',
          label: '所有'
        }]
      },
      // 新增
      newAdd() {
        this.add_flag = true
        this.add_reset()
      },
      add_reset() {
        this.prov_input_flag = false
        this.param_input_flag = false
        this.form.param_table = []
        this.form.add_prov_name = ""
        this.form.add_month = ""
        this.param_input_data = {param_name: "", cont: 0, subparam_info: []}
        this.form.select_param = []
        this.form.add_prov_type = ""
      },
      // 提交新增表单
      add_save() {
        if (this.form.param_table.length === 0) {
          this.$message.warning('请先选择运营数据类型！')
          return false
        }
        console.log(this.$refs['form'])
        this.$refs['form'].validate((valid) => {
          if (valid) {
            let flag = false
            let save_data = []
            for (let i = 0; i < this.form.param_table.length; i++) {
              if (this.form.param_table[i].operative_sub_index === "" || this.form.param_table[i].operate_data === "" || !this.form.param_table[i].operate_data || this.form.param_table[i].operate_desc === "") {
                this.$message.warning("请将类型<" + this.form.param_table[i].operative_sub_index + ">信息补充完整.")
                flag = true
                return false
              }
              save_data.push({
                product_name: this.product_name, operate_month: this.form.add_month,
                prov_name: this.form.add_prov_name, prov_type: this.form.add_prov_type,
                operative_index: this.form.param_table[i].param_name, operative_sub_index: this.form.param_table[i].operative_sub_index,
                operate_data: this.form.param_table[i].operate_data, units: this.form.param_table[i].units,
                operate_desc: this.form.param_table[i].operate_desc, notes: "", target_value: this.form.param_table[i].target_value,
                show_flag: this.form.param_table[i].show_flag
              })
            }
            if (flag === false) {
              let data = {
                operate_info: save_data
              }
              api.operate_data_api.add_operate_data_info(data).then(response => {
                if (response.status === 0) {
                  this.$message.success('新增成功！')
                  this.add_flag = false
                  this.get_area_list()
                } else
                  this.$message.error('系统异常，请联系管理员！')
              })
            }
          }
        })
      },
      updateDesc(index, rows) {
        rows.flag = true;
      },
      deleteDesc(index, rows) {
        this.form.param_table.splice(index, 1);
        let index_1 = this.hasExits(this.options.param_list, "param_name", rows.param_name);
        let index_2 = this.hasExits(this.options.param_list[index_1].subparam_info, "operative_sub_index", rows.operative_sub_index);
        this.options.param_list[index_1].subparam_info.splice(index_2, 1);
      },
      //查找数组对象中是否某个键值对，如果存在就返回最后一个相同键值对的下标,否则返回-1
      hasExits(arr, key, value) {
        let ret = -1;
        for (let i = 0; i < arr.length; i++) {
          if (arr[i][key] === value) {
            ret = i;
          }
        }
        return ret;
      },
      // 选择参数
      click_select_param(val) {
        this.form.param_table = [];
        val.forEach(item => {
          for (let i = 0; i < this.options.param_list[item].subparam_info.length; i++) {
            this.form.param_table.push({
              param_name: this.options.param_list[item].param_name,
              operative_sub_index: this.options.param_list[item].subparam_info[i].operative_sub_index,
              units: this.options.param_list[item].subparam_info[i].units,
              operate_data: "",
              operate_desc: this.options.param_list[item].subparam_info[i].operate_desc,
              flag: false
            })
          }
        })
        console.log(this.form.param_table)
      },
      // 选择子参数个数
      newparam_add(val) {
        this.param_input_data.subparam_info = []
        for (let i = 0; i < val; i++) {
          this.param_input_data.subparam_info.push({operative_sub_index: "", operate_desc: "", units: '', target_value: ''})
        }
      },
      // 添加参数
      add_param_click() {
        if (this.param_input_data.cont === 0) {
          this.$message.warning('请先选择运营数据个数！')
          return false
        }
        console.log('this.param_input_data.subparam_info', this.param_input_data.subparam_info)
        for (let i = 0; i<this.param_input_data.subparam_info.length; i++) {
          if (!this.param_input_data.subparam_info[i].operative_sub_index) {
            console.log('第' + i + '个运营数据的数据名称不能为空！')
            this.$message.error('第' + i + '个运营数据的数据名称不能为空！')
            return false
          }
          if (!this.param_input_data.subparam_info[i].units) {
            console.log('第' + i + '个运营数据的数据单位不能为空！')
            this.$message.error('第' + i + '个运营数据的数据单位不能为空！')
            return false
          }
          if (!this.param_input_data.subparam_info[i].operate_desc) {
            console.log('第' + i + '个运营数据的数据描述不能为空！')
            this.$message.error('第' + i + '个运营数据的数据描述不能为空！')
            return false
          }
          if (!this.param_input_data.subparam_info[i].target_value) {
            console.log('第' + i + '个运营数据的当月运营目标不能为空！')
            this.$message.error('第' + i + '个运营数据的当月运营目标不能为空！')
            return false
          }
        }
        this.$refs['param_input_data'].validate((valid) => {
          if (valid) {
            let arr = [];
            for (let k = 0; k < this.param_input_data.subparam_info.length; k++) {
              arr.push({
                operative_sub_index: this.param_input_data.subparam_info[k].operative_sub_index,
                units: this.param_input_data.subparam_info[k].units,
                operate_desc: this.param_input_data.subparam_info[k].operate_desc,
                target_value: this.param_input_data.subparam_info[k].target_value
              });
            }
            let index = this.hasExits(this.options.param_list, "param_name", this.param_input_data.param_name)
            if (index !== -1) {
              for (let m = 0; m < this.options.param_list.length; m++) {
                if (this.options.param_list[m].param_name === this.param_input_data.param_name) {
                  for (let n = 0; n < arr.length; n++) {
                    this.options.param_list[m].subparam_info.push(arr[n]);
                  }
                  break;
                }
              }
              let index_1 = this.hasExits(this.form.param_table, "param_name", this.param_input_data.param_name);
              if (index_1 !== -1) {
                for (let cn = 0; cn < arr.length; cn++) {
                  let param_arr = {
                    param_name: this.options.param_list[index].param_name,
                    operative_sub_index: arr[cn].operative_sub_index,
                    units: arr[cn].units,
                    operate_data: "",
                    operate_desc: arr[cn].operate_desc, flag: false
                  };

                  this.form.param_table.splice(index_1 + 1, 0, param_arr)
                }
              }
            } else {
              this.options.param_list.push({param_name: this.param_input_data.param_name, subparam_info: arr})
            }
            this.param_input_flag = false;
          }
        })
      },
    },

    mounted() {
      this.product_name = getCookie('product_name')
      this.get_area_list()
    }
  }
</script>
