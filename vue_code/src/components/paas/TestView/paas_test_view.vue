<template>
  <div>
    <CardBox title="查询条件" height="90px">
      <template slot="body">
        <el-form :inline="true" class="mgt-10 form_search">
          <el-form-item label="产品名称">
            <el-input placeholder="输入产品名称" clearable v-model="filterText" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="测试用例名称">
            <el-input placeholder="输入用例名称" clearable v-model="filterText0" size="mini">
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-form-item>
          <el-form-item label="测试用例编码">
            <el-select size="mini" style="width: 160px" v-model="filterText1" clearable filterable
                       remote reserve-keyword placeholder="输入用例编码关键词"
                       :remote-method="remote_select_Method" :loading="select_loading">
              <el-option
                v-for="item in select_options"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </template>
    </CardBox>

    <CardBox title="查询结果" height="100%" marginT="20">
      <template slot="body">
        <div class="table mgt-10">
          <el-tree accordion class="filter-tree" :data="tree_data"
                   :props="defaultProps"
                   :filter-node-method="filterNode"
                   ref="tree">
          </el-tree>
        </div>
      </template>
    </CardBox>

  </div>
</template>

<script>
  import {getCookie} from "../../../service/cookie"
  import api from "../../../service/api";

  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox')
    },
    data() {
      return {
        select_loading:false,
        select_options:[],
        filterText: '',
        filterText0: '',
        filterText1: '',
        tree_data: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        loading:false,
      }
    },
    watch: {
      filterText(val) {
        this.$refs.tree.filter(val)
      },
      filterText0(val) {
        this.$refs.tree.filter(val)
      },
      filterText1(val) {
        if(val == null) val = "";
        this.$refs.tree.filter(val)
      }
    },
    methods: {
      remote_select_Method(query){
        if(query !== ""){
          this.select_loading = true;
          let data = {
            test_action:query,
            user_id:getCookie('user_id')
          }
          api.paas_whole_test_api.select_check_case_code(data).then(response =>{
            if(response.status === 0){
              this.select_options = response.info;
            }else{
              alert(response.info)
            }
            this.select_loading = false;
          })
        }else{
          this.select_loading = false;
          this.select_options = [];
        }
      },
      filterNode(value, data) {
        if (!value) {
          return true
        }
        return data.label.indexOf(value) !== -1;
      },
      check_data(){
        this.loading = true;
        let data = {
          user_id:getCookie('user_id')
        }
        api.paas_whole_test_api.paas_tree_view(data).then(response => {
          if(response.status === 0) {
            let ret_info = response.info;
            let arr = [];
            for(let i = 0;i < ret_info.length;i ++){
              let template_label = "";
              template_label = "模板名称：<" +  ret_info[i].template.module_name + "> | 产品名称：<"
                + ret_info[i].template.module_type + ">"
              let case_child = [];
              let case_info = ret_info[i].case;
              for(let j = 0;j < case_info.length;j ++){
                let case_label = "";
                case_label = "用例名称：<" + case_info[j].case_name + ">";
                case_child.push({label:case_label});
              }
              arr.push({label:template_label,children:case_child});
            }
            this.tree_data = arr;
          }else
            alert(response.info)
          this.loading = false;
        })
      }
    },

    mounted() {
      this.check_data()
    }
  }
</script>
<style lang="scss" scoped>
  .search_box {
    padding: 20px 0;
    display: flex;
    align-items: center;
  }

  .main_class {
    text-align: left !important;
    background-color: #ffffff;
    /*padding-left: 550px;*/
    font-size: 10px;
    line-height: 20px;
    margin: 0 auto;
  }
</style>
