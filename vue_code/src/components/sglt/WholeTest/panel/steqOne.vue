<template>
  <div>
    <el-form
      ref="form"
      :rules="rules"
      :model="form"
      label-width="150px"
      class="steq_panel_form">
      <el-row>
        <el-col :span="6">
          <el-form-item label="资费类型" prop="fee_type">
            <el-select
              v-model="form.fee_type"
              placeholder="请选择资费类型"
              size="small"
              style="width:160px">
              <el-option label="资费代码" value="1"></el-option>
              <el-option label="二批代码" value="2"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="18">
          <el-form-item label="资费代码" prop="fee_code">
            <el-input
              v-model="form.fee_code"
              placeholder="请输入资费代码"
              size="small"
              style="width:200px"></el-input>
            <el-button type="primary" size="small"
                       v-loading="fullscreenLoading"
                       element-loading-text="正在查询，请稍等。。。"
                       element-loading-spinner="el-icon-loading"
                       element-loading-background="rgba(0, 0, 0, 0.8)"
                       v-loading.fullscreen.lock="fullscreenLoading"
                       @click="check_fee_detail">查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="资费信息" prop="fee_info">
            <span>{{ form.fee_info }}</span>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="18">
          <el-form-item label="附加资费" prop="add_offer_id">
            <el-input
              v-model="form.add_offer_id"
              placeholder="请输入附加资费"
              size="small"
              style="width:200px"
            ></el-input>
            <el-tooltip class="item" effect="dark" content="(附加资费以逗号分隔填写，格式eg：附加资费ID1,附加资费ID2,附加资费ID3)"
                        placement="right">
              <el-button type="text" icon=" el-icon-info"></el-button>
            </el-tooltip>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="号码类型" prop="number_type">
            <el-select
              clearable
              v-model="form.number_type"
              placeholder="请选择"
              size="small"
              @change="change_number_input_flag(form.number_type)"
              style="width:160px">
              <el-option
                v-for="item in test_number_options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <div v-if="normal_number_flag">
        <el-form :model="test_numbers" ref="test_numbers" label-width="150px">
          <el-form-item label="普通号码" prop="normal_number"
                        :rules="[{ required: true, message: '请输入测试号码', trigger: 'blur'}]">
            <el-input size="small" v-model="test_numbers.normal_number" placeholder="请输入普通测试号码"
                      style="width: 30%"></el-input>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="parent_child_numbers_flag">
        <el-form :model="test_numbers" ref="test_numbers" label-width="150px" size="mini">
          <el-form-item
            prop="parent_number"
            label="测试主号码"
            :rules="[{ required: true, message: '请输入测试主号码', trigger: 'blur'}]">
            <el-input v-model="test_numbers.parent_number" style="width: 30%" size="mini"></el-input>
          </el-form-item>
          <el-form-item
            v-for="(number, index) in test_numbers.parent_child_numbers"
            :label="'测试副号码' + index"
            :key="number.key"
            :prop="'parent_child_numbers.' + index + '.child_number'"
            :rules="{required: true, message: '测试副号码不能为空', trigger: 'blur'}">
            <el-input v-model="number.child_number" style="width: 30%" size="mini"></el-input>
            <el-button @click.prevent="removeDomain(number)" size="mini">删除</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="addDomain">新增副号码</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="family_numbers_flag">
        <el-form :model="test_numbers" ref="test_numbers" label-width="150px" class="demo-dynamic">
          <el-form-item
            prop="family_parent_number"
            label="亲情主号码"
            :rules="[{ required: true, message: '请输入亲情主号码', trigger: 'blur'}]">
            <el-input v-model="test_numbers.family_parent_number" style="width: 30%" size="mini"></el-input>
          </el-form-item>
          <el-form-item
            v-for="(number, index) in test_numbers.family_numbers"
            :label="'亲情副号码' + index"
            :key="number.key"
            :prop="'family_numbers.' + index + '.family_child_number'"
            :rules="{required: true, message: '亲情副号码不能为空', trigger: 'blur'}">
            <el-input v-model="number.family_child_number" style="width: 30%" size="mini"></el-input>
            <el-button @click.prevent="removeDomain(number)" size="mini">删除</el-button>
          </el-form-item>
          <el-form-item>
            <el-button @click="addDomain" size="mini">新增副号码</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-row>
        <el-col>
          <el-form-item label="执行动作" prop="action">
            <el-radio-group v-model="form.action" @change="change_button">
              <el-radio :label="3">绑定测试模版</el-radio>
              <el-radio :label="6">绑定测试用例</el-radio>
              <el-radio :label="9">生成用户资料</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-dialog :visible.sync="cat_fee_detail_flag" width="75%" class="feecontents" title="资费详情" @closeDialog='cat_fee_detail_flag = false'>
      <el-table
        :data="tableData"
        border
        default-expand-all
        style="width: 100%"
        :header-cell-style="{background:'#E4E7ED',color:'#606266'}">
        <el-table-column type="expand">

          <el-collapse accordion>
            <el-collapse-item v-for="(param,i) in dataArr" :key="param.prc_id"
                              :title='"系统类型：" + param.sys_type + " | 资费ID：" + param.prc_id' :name=i>
              <table class="info">
                <tr>
                  <th style="width: 90px">套餐类型</th>
                  <td style="color: blue;width: 90px">{{param.sys_type}}</td>
                  <th style="width: 90px">资费ID</th>
                  <td style="color: blue;width: 90px">{{param.prc_id}}</td>
                  <th style="width: 90px">资费关系</th>
                  <td style="color: blue">{{param.PRCEXPR}}</td>
                </tr>
              </table>
              <el-table
                border
                default-expand-all
                :data="param.List"
                style="width: 100%"
                id="dafaultId"
                :header-cell-style="{background:'#E1FFFF',color:'#606266'}">
                <el-table-column property="PRIORITY" label="优先级" align="center"></el-table-column>
                <el-table-column property="SUBPRIORITY" label="次优先级" align="center"></el-table-column>
                <el-table-column property="sub_plan_id" label="子资费id" align="center"></el-table-column>
                <!--                    <el-table-column property="ltfavorcap" label="套内费率" align="center"></el-table-column>-->
                <!--                    <el-table-column property="thresholdval" label="套内免费资源" align="center"></el-table-column>-->
                <!--                    <el-table-column property="units" label="免费资源单位" align="center"></el-table-column>-->
                <!--                    <el-table-column property="gtfavorcap" label="套外单价" align="center"></el-table-column>-->
                <el-table-column property="feilv1" label="费率1" align="center"></el-table-column>
                <el-table-column property="fazhi1" label="阈值1" align="center"></el-table-column>
                <el-table-column property="feilv2" label="费率2" align="center"></el-table-column>
                <el-table-column property="fazhi2" label="阈值2" align="center"></el-table-column>
                <el-table-column property="units" label="单位" align="center"></el-table-column>

                <el-table-column type="expand" width="80px" label="查看更多" align="center">
                  <template slot-scope="props">
                    <el-form label-position="left"
                             inline class="demo-table-expand">
                      <el-form-item label="赠送模式:" style="color: red" v-show="props.row.adjust">
                        <span>{{props.row.adjust}}</span>
                      </el-form-item>
                      <el-form-item label="截断核减标识:" style="color: red" v-show="props.row.reduction_type">
                        <span>{{props.row.reduction_type}}</span>
                      </el-form-item>
                      <el-form-item label="累计周期标识:" style="color: red" v-show="props.row.accumulateCycleFlag">
                        <span>{{props.row.accumulateCycleFlag}}</span>
                      </el-form-item>
                      <el-form-item label="忙闲时时间:" style="color: red" v-show="props.row.busyday">
                        <span>{{props.row.busyday}}</span>
                      </el-form-item>
                      <el-form-item label="忙闲时时间:" style="color: red" v-show="props.row.busytime">
                        <span>{{props.row.busytime}}</span>
                      </el-form-item>
                      <el-form-item label="v网资费标识:" style="color: red" v-show="props.row.call_flag_code">
                        <span>{{props.row.call_flag_code}}</span>
                      </el-form-item>
                      <el-form-item label="呼叫类型:" style="color: red" v-show="props.row.call_types">
                        <span>{{props.row.call_types}}</span>
                      </el-form-item>
                      <el-form-item label="对端类型:" style="color: red" v-show="props.row.chat_types">
                        <span>{{props.row.chat_types}}</span>
                      </el-form-item>
                      <el-form-item label="日期类型:" style="color: red" v-show="props.row.date_codes">
                        <span>{{props.row.date_codes}}</span>
                      </el-form-item>
                      <el-form-item label="拨打类型:" style="color: red" v-show="props.row.dial_types">
                        <span>{{props.row.dial_types}}</span>
                      </el-form-item>
                      <el-form-item label="费用类型:" style="color: red" v-show="props.row.fee_types">
                        <span>{{props.row.fee_types}}</span>
                      </el-form-item>
                      <el-form-item label="升舱分段资费:" style="color: red" v-show="props.row.gradeattrflag">
                        <span>{{props.row.gradeattrflag}}</span>
                      </el-form-item>
                      <el-form-item label="信息台编码:" style="color: red" v-show="props.row.info_numbers">
                        <span>{{props.row.info_numbers}}</span>
                      </el-form-item>
                      <el-form-item label="对端品牌:" style="color: red" v-show="props.row.other_brands">
                        <span>{{props.row.other_brands}}</span>
                      </el-form-item>
                      <el-form-item label="亲情编码:" style="color: red" v-show="props.row.relation_codes">
                        <span>{{props.row.relation_codes}}</span>
                      </el-form-item>
                      <el-form-item label="亲情类型:" style="color: red" v-show="props.row.relphonetype">
                        <span>{{props.row.relphonetype}}</span>
                      </el-form-item>
                      <el-form-item label="漫游类型:" style="color: red" v-show="props.row.roam_types">
                        <span>{{props.row.roam_types}}</span>
                      </el-form-item>
                      <el-form-item label="分割时间段:" style="color: red" v-show="props.row.split_time">
                        <span>{{props.row.split_time}}</span>
                      </el-form-item>
                      <el-form-item label="系统类型:" style="color: red" v-show="props.row.system_types">
                        <span>{{props.row.system_types}}</span>
                      </el-form-item>
                      <el-form-item label="时间类型:" style="color: red" v-show="props.row.time_type">
                        <span>{{props.row.time_type }}</span>
                      </el-form-item>
                      <el-form-item label="用户品牌:" style="color: red" v-show="props.row.user_brands">
                        <span>{{props.row.user_brands }}</span>
                      </el-form-item>
                      <el-form-item label="用户类型:" style="color: red" v-show="props.row.user_types">
                        <span>{{props.row.user_types }}</span>
                      </el-form-item>
                      <el-form-item label="集团编码:" style="color: red" v-show="props.row.vpmn_attr">
                        <span>{{props.row.vpmn_attr }}</span>
                      </el-form-item>
                      <el-form-item label="小区编码:" style="color: red" v-show="props.row.location_codes">
                        <span>{{props.row.location_codes }}</span>
                      </el-form-item>
                      <el-form-item label="集团标识:" style="color: red" v-show="props.row.vpmn_codes">
                        <span>{{props.row.vpmn_codes }}</span>
                      </el-form-item>
                      <el-form-item label="周末标识:" style="color: red" v-show="props.row.weekendID">
                        <span>{{props.row.weekendID }}</span>
                      </el-form-item>
                      <el-form-item label="优惠费用项:" style="color: red" v-show="props.row.weekendID">
                        <span>{{props.row.feetypes }}</span>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
              </el-table>
            </el-collapse-item>
          </el-collapse>
        </el-table-column>
        <el-table-column prop="PROD_PRC_NAME" label="资费名称" align="center"></el-table-column>
        <el-table-column prop="EFF_DATE" label="销售开始日期" align="center"></el-table-column>
        <el-table-column prop="EXP_DATE" label="销售终止日期" align="center"></el-table-column>
       </el-table>
    </el-dialog>
  </div>
</template>

<script>
  import api from "../../../../service/api";
  import {getCookie} from "../../../../service/cookie";

  export default {
    components: {
      Dialog: () => import('@/components/common/Dialog')
    },
    data() {
      return {
        // 输入需求表单
        form: {
          fee_type: '1',
          fee_code: '',
          fee_info: '',
          add_offer_id: '',
          number_type: '',
          action: 3
        },
        rules: {
          fee_code: [
            {required: true, message: '请输入资费代码', trigger: 'blur'}
          ],
          number_type: [
            {required: true, message: '请选择号码类型', trigger: 'blur'}
          ],
          action: [{required: true, message: '请选择执行动作', trigger: 'blur'}]
        },
        // 选择输入号码类型
        normal_number_flag: false, // 显示普通号码输入框
        parent_child_numbers_flag: false, // 显示主副卡号码输入框
        family_numbers_flag: false, // 显示亲情卡号码输入框
        test_number_options: [{
          value: 'normal_number',
          label: '普通号码测试'
        }, {
          value: 'family_numbers',
          label: '亲情卡测试'
        }, {
          value: 'parent_child_numbers',
          label: '主副卡测试'
        }],
        test_numbers: {
          parent_child_numbers: [{
            child_number: ''
          }],
          family_numbers: [{
            family_child_number: ''
          }],
          parent_number: '',
          family_parent_number: '',
          normal_number: ''
        },
        // 查看资费详情
        fullscreenLoading: false,
        cat_fee_detail_flag: false,
        tableData: [],
        tableData2: [],
        dataArr: [],
        instance_info: {
          test_numbers: {
            family_numbers: [],
            family_parent_number: '',
            parent_child_numbers: [],
            parent_number: '',
            number_type: '',
            normal_number: ''
          }
        }
      }
    },
    methods: {
      change_button(value) {
        this.$emit('change_button', value)
      },
      // 移除号码输入框
      removeDomain(item) {
        let index = -1
        if (this.form.number_type === 'parent_child_numbers') {
          index = this.test_numbers.parent_child_numbers.indexOf(item)
          if (index !== -1) {
            this.test_numbers.parent_child_numbers.splice(index, 1)
          }
        } else if (this.form.number_type === 'family_numbers') {
          index = this.test_numbers.family_numbers.indexOf(item)
          if (index !== -1) {
            this.test_numbers.family_numbers.splice(index, 1)
          }
        }
      },
      // 增加号码输入框
      addDomain() {
        if (this.form.number_type === 'parent_child_numbers') {
          this.test_numbers.parent_child_numbers.push({
            child_number: '',
            key: Date.now()
          });
        } else if (this.form.number_type === 'family_numbers') {
          this.test_numbers.family_numbers.push({
            family_child_number: '',
            key: Date.now()
          });
        }
      },
      // 重置号码输入表单
      resetForm() {
        this.test_numbers = {
          parent_child_numbers: [{
            child_number: ''
          }],
          family_numbers: [{
            family_child_number: ''
          }],
          parent_number: '',
          family_parent_number: '',
          normal_number: ''
        }
      },
      // 选择特殊号码输入框
      change_number_input_flag(value) {
        switch (value) {
          case 'parent_child_numbers':
            this.parent_child_numbers_flag = true
            this.family_numbers_flag = false
            this.normal_number_flag = false
            break;
          case 'family_numbers':
            this.family_numbers_flag = true
            this.parent_child_numbers_flag = false
            this.normal_number_flag = false
            break;
          case 'normal_number':
            this.normal_number_flag = true
            this.family_numbers_flag = false
            this.parent_child_numbers_flag = false
            break;
          default:
            this.normal_number_flag = false
            this.family_numbers_flag = false
            this.parent_child_numbers_flag = false
        }
        this.resetForm('test_numbers')
      },
      // 查询资费详情
      check_fee_detail() {
        if (!this.form.fee_code) {
          this.$message.warning('资费代码或二批代码不能为空！')
        }
        else {
          this.fullscreenLoading = true
          let data = {
            offer_id: this.form.fee_code,
            user_id: getCookie('user_id')
          }
          api.config_manage_api.query_charges_info(data).then(res => {
            if (res.status === -4) {
              alert('非法请求')
              this.$router.push('/')
            }
            if (res.status === -1) {
              this.fullscreenLoading = false
              this.cat_fee_detail_flag = false
              this.$message.error('该资费套餐不存在，请重新输入！')
            } else if (res.status === 0) {
              this.fullscreenLoading = false
              this.tableData = []
              this.tableData2 = []
              this.cat_fee_detail_flag = true
              let info = res.info
              let tdData = res.info.title[0]
              // 第一个表头的数据
              let first_tb = {}
              first_tb['PROD_PRC_NAME'] = tdData['PROD_PRC_NAME']
              first_tb['EFF_DATE'] = tdData['EFF_DATE']
              first_tb['EXP_DATE'] = tdData['EXP_DATE']
              this.form.fee_info = tdData['PROD_PRC_NAME']
              this.tableData.push(first_tb)
              // 1、语音
              for (let i = 0; i < res.info.prc_info.length; i++) {
                let list1 = []
                if (info.prc_info[i].system_type === '语音') {
                  list1.push(i)
                  if (list1 !== []) {
                    list1.forEach(item => {
                      console.log(info.prc_info[0].plan_infos)
                      let prc_info = info.prc_info[item].plan_infos
                      for (let l = 0; l < prc_info.length; l++) {
                        let vc_dict = {}
                        vc_dict.sys_type = info.prc_info[i].system_type
                        vc_dict.prc_id = info.prc_info[i].prc_id
                        vc_dict.PRCEXPR = info.prc_info[i].PRCEXPR
                        vc_dict.PRIORITY = info.prc_info[i].PRIORITY
                        vc_dict.SUBPRIORITY = info.prc_info[i].SUBPRIORITY
                        vc_dict.sub_plan_id = prc_info[l].sub_plan_id
                        vc_dict.ltfavorcap = info.prc_info[i].sub_plan_info[l].ltfavorcap_desc
                        vc_dict.thresholdval = info.prc_info[i].sub_plan_info[l].thresholdval_desc
                        vc_dict.units = info.prc_info[i].sub_plan_info[l].units
                        if (!vc_dict.units) {
                          vc_dict.units = '-'
                        } else if (vc_dict.units === '60') {
                          vc_dict.units = '分钟'
                        }
                        vc_dict.gtfavorcap = info.prc_info[i].sub_plan_info[l].gtfavorcap

                        vc_dict.adjust = info.prc_info[i].sub_plan_info[l].adjust
                        vc_dict.reduction_type = info.prc_info[i].sub_plan_info[l].reduction_type
                        vc_dict.accumulateCycleFlag = info.prc_info[i].sub_plan_info[l].accumulateCycleFlag
                        vc_dict.busyday = info.prc_info[i].sub_plan_info[l].busyday
                        vc_dict.busytime = info.prc_info[i].sub_plan_info[l].busytime
                        vc_dict.call_flag_code = info.prc_info[i].sub_plan_info[l].call_flag_code
                        vc_dict.call_types = info.prc_info[i].sub_plan_info[l].call_types
                        vc_dict.chat_types = info.prc_info[i].sub_plan_info[l].chat_types
                        vc_dict.date_codes = info.prc_info[i].sub_plan_info[l].date_codes
                        vc_dict.dial_types = info.prc_info[i].sub_plan_info[l].dial_types
                        vc_dict.fee_types = info.prc_info[i].sub_plan_info[l].fee_types
                        vc_dict.gradeattrflag = info.prc_info[i].sub_plan_info[l].gradeattrflag
                        vc_dict.info_numbers = info.prc_info[i].sub_plan_info[l].info_numbers
                        vc_dict.other_brands = info.prc_info[i].sub_plan_info[l].other_brands
                        vc_dict.relation_codes = info.prc_info[i].sub_plan_info[l].relation_codes
                        vc_dict.relphonetype = info.prc_info[i].sub_plan_info[l].relphonetype
                        vc_dict.roam_types = info.prc_info[i].sub_plan_info[l].roam_types
                        vc_dict.split_time = info.prc_info[i].sub_plan_info[l].split_time
                        vc_dict.system_types = info.prc_info[i].sub_plan_info[l].system_types
                        vc_dict.time_type = info.prc_info[i].sub_plan_info[l].time_type
                        vc_dict.user_brands = info.prc_info[i].sub_plan_info[l].user_brands
                        vc_dict.user_types = info.prc_info[i].sub_plan_info[l].user_types
                        vc_dict.vpmn_attr = info.prc_info[i].sub_plan_info[l].vpmn_attr
                        vc_dict.location_codes = info.prc_info[i].sub_plan_info[l].location_codes
                        vc_dict.vpmn_codes = info.prc_info[i].sub_plan_info[l].vpmn_codes
                        vc_dict.weekendID = info.prc_info[i].sub_plan_info[l].weekendID
                        vc_dict.feetypes = info.prc_info[i].sub_plan_info[l].feetypes
                        this.tableData2.push(vc_dict)
                      }
                    })
                  }
                }

                let list2 = []
                if (info.prc_info[i].system_type === '流量') {
                  list2.push(i)
                  let float = []
                  if (list2 !== []) {
                    list2.forEach(item => {
                      float = info.prc_info[item].plan_infos
                    })
                  }
                  for (let f in float) {
                    let float_dict = {}
                    float_dict.sys_type = info.prc_info[i].system_type
                    float_dict.prc_id = info.prc_info[i].prc_id
                    float_dict.PRIORITY = info.prc_info[i].PRIORITY
                    float_dict.SUBPRIORITY = info.prc_info[i].prc_info.SUBPRIORITY
                    float_dict.PRCEXPR = info.prc_info[i].PRCEXPR
                    float_dict.sub_plan_id = float[f].sub_plan_id
                    // float_dict.ltfavorcap = info.prc_info[i].sub_plan_info[0].ltfavorcap_desc
                    // float_dict.thresholdval = info.prc_info[i].sub_plan_info[0].thresholdval_desc
                    // float_dict.units = info.prc_info[i].sub_plan_info[0].units
                    float_dict.units = info.prc_info[i].sub_plan_info[i].units
                    float_dict.fazhi1 = info.prc_info[i].sub_plan_info[i].fazhi1
                    float_dict.fazhi2 = info.prc_info[i].sub_plan_info[i].fazhi2
                    float_dict.feilv1 = info.prc_info[i].sub_plan_info[i].feilv1
                    float_dict.feilv2 = info.prc_info[i].sub_plan_info[i].feilv2
                    float_dict.feilv3 = info.prc_info[i].sub_plan_info[i].feilv3

                    if (!float_dict.units) {
                      float_dict.units = '-'
                    } else if (float_dict.units === '1024') {
                      float_dict.units = 'KB'
                    } else if (float_dict.units === '1048576') {
                      float_dict.units = 'MB'
                    }
                    // float_dict.gtfavorcap = info.prc_info[i].sub_plan_info[0].gtfavorcap_desc

                    float_dict.adjust = info.prc_info[i].sub_plan_info[f].adjust
                    float_dict.reduction_type = info.prc_info[i].sub_plan_info[f].reduction_type
                    float_dict.accumulateCycleFlag = info.prc_info[i].sub_plan_info[f].accumulateCycleFlag
                    float_dict.busyday = info.prc_info[i].sub_plan_info[f].busyday
                    float_dict.busytime = info.prc_info[i].sub_plan_info[f].busytime
                    float_dict.call_flag_code = info.prc_info[i].sub_plan_info[f].call_flag_code
                    float_dict.call_types = info.prc_info[i].sub_plan_info[f].call_types
                    float_dict.chat_types = info.prc_info[i].sub_plan_info[f].chat_types
                    float_dict.date_codes = info.prc_info[i].sub_plan_info[f].date_codes
                    float_dict.dial_types = info.prc_info[i].sub_plan_info[f].dial_types
                    float_dict.fee_types = info.prc_info[i].sub_plan_info[f].fee_types
                    float_dict.gradeattrflag = info.prc_info[i].sub_plan_info[f].gradeattrflag
                    float_dict.info_numbers = info.prc_info[i].sub_plan_info[f].info_numbers
                    float_dict.other_brands = info.prc_info[i].sub_plan_info[f].other_brands
                    float_dict.relation_codes = info.prc_info[i].sub_plan_info[f].relation_codes
                    float_dict.relphonetype = info.prc_info[i].sub_plan_info[f].relphonetype
                    float_dict.roam_types = info.prc_info[i].sub_plan_info[f].roam_types
                    float_dict.split_time = info.prc_info[i].sub_plan_info[f].split_time
                    float_dict.system_types = info.prc_info[i].sub_plan_info[f].system_types
                    float_dict.time_type = info.prc_info[i].sub_plan_info[f].time_type
                    float_dict.user_brands = info.prc_info[i].sub_plan_info[f].user_brands
                    float_dict.user_types = info.prc_info[i].sub_plan_info[f].user_types
                    float_dict.vpmn_attr = info.prc_info[i].sub_plan_info[f].vpmn_attr
                    float_dict.location_codes = info.prc_info[i].sub_plan_info[f].location_codes
                    float_dict.vpmn_codes = info.prc_info[i].sub_plan_info[f].vpmn_codes
                    float_dict.weekendID = info.prc_info[i].sub_plan_info[f].weekendID
                    float_dict.feetypes = info.prc_info[i].sub_plan_info[f].feetypes
                    this.tableData2.push(float_dict)
                  }
                }
                if (info.prc_info[i].system_type === '其他') {
                  let other = info.prc_info[i].plan_infos

                  for (let o in other) {
                    let other_dict = {}
                    other_dict.sys_type = info.prc_info[i].system_type
                    other_dict.prc_id = info.prc_info[i].prc_id
                    other_dict.prioritylevel = '-'
                    other_dict.sub_plan_id = other[o].sub_plan_id
                    other_dict.ltfavorcap = info.prc_info[i].sub_plan_info[0].ltfavorcap_desc
                    other_dict.thresholdval = info.prc_info[i].sub_plan_info[0].thresholdval_desc
                    other_dict.units = info.prc_info[i].sub_plan_info[0].units
                    if (!other_dict.units) {
                      other_dict.units = '-'
                    }
                    other_dict.gtfavorcap = info.prc_info[i].sub_plan_info[0].gtfavorcap_desc
                    other_dict.PRIORITY = info.prc_info[i].PRIORITY
                    other_dict.SUBPRIORITY = info.prc_info[i].SUBPRIORITY
                    other_dict.PRCEXPR = info.prc_info[i].PRCEXPR

                    other_dict.adjust = info.prc_info[i].sub_plan_info[o].adjust
                    other_dict.reduction_type = info.prc_info[i].sub_plan_info[o].reduction_type
                    other_dict.accumulateCycleFlag = info.prc_info[i].sub_plan_info[o].accumulateCycleFlag
                    other_dict.busyday = info.prc_info[i].sub_plan_info[o].busyday
                    other_dict.busytime = info.prc_info[i].sub_plan_info[o].busytime
                    other_dict.call_flag_code = info.prc_info[i].sub_plan_info[o].call_flag_code
                    other_dict.call_types = info.prc_info[i].sub_plan_info[o].call_types
                    other_dict.chat_types = info.prc_info[i].sub_plan_info[o].chat_types
                    other_dict.date_codes = info.prc_info[i].sub_plan_info[o].date_codes
                    other_dict.dial_types = info.prc_info[i].sub_plan_info[o].dial_types
                    other_dict.fee_types = info.prc_info[i].sub_plan_info[o].fee_types
                    other_dict.gradeattrflag = info.prc_info[i].sub_plan_info[o].gradeattrflag
                    other_dict.info_numbers = info.prc_info[i].sub_plan_info[o].info_numbers
                    other_dict.other_brands = info.prc_info[i].sub_plan_info[o].other_brands
                    other_dict.relation_codes = info.prc_info[i].sub_plan_info[o].relation_codes
                    other_dict.relphonetype = info.prc_info[i].sub_plan_info[o].relphonetype
                    other_dict.roam_types = info.prc_info[i].sub_plan_info[o].roam_types
                    other_dict.split_time = info.prc_info[i].sub_plan_info[o].split_time
                    other_dict.system_types = info.prc_info[i].sub_plan_info[o].system_types
                    other_dict.time_type = info.prc_info[i].sub_plan_info[o].time_type
                    other_dict.user_brands = info.prc_info[i].sub_plan_info[o].user_brands
                    other_dict.user_types = info.prc_info[i].sub_plan_info[o].user_types
                    other_dict.vpmn_attr = info.prc_info[i].sub_plan_info[o].vpmn_attr
                    other_dict.location_codes = info.prc_info[i].sub_plan_info[o].location_codes
                    other_dict.vpmn_codes = info.prc_info[i].sub_plan_info[o].vpmn_codes
                    other_dict.weekendID = info.prc_info[i].sub_plan_info[o].weekendID
                    other_dict.feetypes = info.prc_info[i].sub_plan_info[o].feetypes
                    this.tableData2.push(other_dict)
                  }
                }
                if (info.prc_info[i].system_type === '短信') {
                  let sms = info.prc_info[i].plan_infos
                  for (let ss in sms) {
                    let sms_dict = {}
                    sms_dict.sys_type = info.prc_info[i].system_type
                    sms_dict.prc_id = info.prc_info[i].prc_id
                    sms_dict.prioritylevel = '-'
                    sms_dict.sub_plan_id = sms[ss].sub_plan_id
                    sms_dict.ltfavorcap = info.prc_info[i].sub_plan_info[ss].favorcap
                    sms_dict.thresholdval = info.prc_info[i].sub_plan_info[ss].thresholdval_desc
                    sms_dict.units = info.prc_info[i].sub_plan_info[ss].units
                    if (sms_dict.units.length <= 0) {
                      sms_dict.units = '条'
                    }
                    sms_dict.gtfavorcap = info.prc_info[i].sub_plan_info[ss].gtfavorcap_desc
                    sms_dict.PRIORITY = info.prc_info[i].PRIORITY
                    sms_dict.SUBPRIORITY = info.prc_info[i].SUBPRIORITY
                    sms_dict.PRCEXPR = info.prc_info[i].PRCEXPR

                    sms_dict.adjust = info.prc_info[i].sub_plan_info[ss].adjust
                    sms_dict.reduction_type = info.prc_info[i].sub_plan_info[ss].reduction_type
                    sms_dict.accumulateCycleFlag = info.prc_info[i].sub_plan_info[ss].accumulateCycleFlag
                    sms_dict.busyday = info.prc_info[i].sub_plan_info[ss].busyday
                    sms_dict.busytime = info.prc_info[i].sub_plan_info[ss].busytime
                    sms_dict.call_flag_code = info.prc_info[i].sub_plan_info[ss].call_flag_code
                    sms_dict.call_types = info.prc_info[i].sub_plan_info[ss].call_types
                    sms_dict.chat_types = info.prc_info[i].sub_plan_info[ss].chat_types
                    sms_dict.date_codes = info.prc_info[i].sub_plan_info[ss].date_codes
                    sms_dict.dial_types = info.prc_info[i].sub_plan_info[ss].dial_types
                    sms_dict.fee_types = info.prc_info[i].sub_plan_info[ss].fee_types
                    sms_dict.gradeattrflag = info.prc_info[i].sub_plan_info[ss].gradeattrflag
                    sms_dict.info_numbers = info.prc_info[i].sub_plan_info[ss].info_numbers
                    sms_dict.other_brands = info.prc_info[i].sub_plan_info[ss].other_brands
                    sms_dict.relation_codes = info.prc_info[i].sub_plan_info[ss].relation_codes
                    sms_dict.relphonetype = info.prc_info[i].sub_plan_info[ss].relphonetype
                    sms_dict.roam_types = info.prc_info[i].sub_plan_info[ss].roam_types
                    sms_dict.split_time = info.prc_info[i].sub_plan_info[ss].split_time
                    sms_dict.system_types = info.prc_info[i].sub_plan_info[ss].system_types
                    sms_dict.time_type = info.prc_info[i].sub_plan_info[ss].time_type
                    sms_dict.user_brands = info.prc_info[i].sub_plan_info[ss].user_brands
                    sms_dict.user_types = info.prc_info[i].sub_plan_info[ss].user_types
                    sms_dict.vpmn_attr = info.prc_info[i].sub_plan_info[ss].vpmn_attr
                    sms_dict.location_codes = info.prc_info[i].sub_plan_info[ss].location_codes
                    sms_dict.vpmn_codes = info.prc_info[i].sub_plan_info[ss].vpmn_codes
                    sms_dict.weekendID = info.prc_info[i].sub_plan_info[ss].weekendID
                    sms_dict.feetypes = info.prc_info[i].sub_plan_info[ss].feetypes
                    this.tableData2.push(sms_dict)
                  }
                }
                this.dataArr = [];
                this.tableData2.map(mapItem => {
                  if (this.dataArr.length === 0) {
                    this.dataArr.push({
                      sys_type: mapItem.sys_type,
                      prc_id: mapItem.prc_id,
                      PRCEXPR: mapItem.PRCEXPR,
                      List: [mapItem]
                    })
                  } else {
                    let res = this.dataArr.some(item => {
                      if (item.sys_type === mapItem.sys_type && item.prc_id === mapItem.prc_id && item.PRCEXPR === mapItem.PRCEXPR) {
                        item.List.push(mapItem)
                        return true
                      }
                    })
                    if (!res) {
                      this.dataArr.push({
                        sys_type: mapItem.sys_type,
                        prc_id: mapItem.prc_id,
                        PRCEXPR: mapItem.PRCEXPR,
                        List: [mapItem]
                      })
                    }
                  }
                })
              }
            }
          })
        }
      },
      // 校验表单
      confirm_form(form_name) {
        if (!this.form.fee_info) {
          this.$message.warning('请先查询确认资费详情信息！')
          return false
        }
        if (!this.form.number_type) {
          this.$message.warning('请选择号码类型！')
          return false
        }
        this.$refs[form_name].validate((valid) => {
          if (valid) {
            let parent_child_numbers = []
            let family_numbers = []
            this.test_numbers.parent_child_numbers.forEach((item, index) => {
              parent_child_numbers[index] = item.child_number
            })
            this.test_numbers.family_numbers.forEach((item, index) => {
              family_numbers[index] = item.family_child_number
            })
            this.instance_info.test_numbers.parent_number = this.test_numbers.parent_number
            this.instance_info.test_numbers.parent_child_numbers = parent_child_numbers
            this.instance_info.test_numbers.family_parent_number = this.test_numbers.family_parent_number
            this.instance_info.test_numbers.family_numbers = family_numbers
            this.instance_info.test_numbers.number_type = this.form.number_type
            this.instance_info.test_numbers.normal_number = this.test_numbers.normal_number

            let ret_info = {}
            ret_info.form = this.form
            ret_info.instance_info = this.instance_info
            this.$emit('next_step', 'step_one', ret_info)
          }
        })
      }
    },
    mounted() {
    }
  }
</script>
<style lang="scss" scoped>
  .info {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
  }

  .info th {
    font-size: 15px;
    background-color: #E1FFFF;
    text-align: center;
    padding-left: 10px;
    font-weight: bold;
    border: 1px solid #ddd;
    width: 150px;
  }

  .info tr {
    line-height: 25px;
  }

  .info td {
    background-color: #E1FFFF;
    text-align: center;
    border: 1px solid #ddd;
    padding-left: 10px;
    width: 210px;
  }

  .line_three {
    padding: 18px 10px;

    .info {
      font-size: 14px;
      display: flex;
      align-items: center;

      p {
        margin-right: 40px;
      }
    }

    .info_line {
      margin-top: 8px;
      text-align: center;

      &_item {
        border: 1px solid #e5ecf2;
        border-bottom: none;
        padding: 10px 0;
      }
    }
  }

  .feecontents {
    text-align: center;
    position: absolute;
    width: 122%;
    left: -150px;
  }
</style>
