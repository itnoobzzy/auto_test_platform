<template>
  <div class="header__nav">
    <el-menu
      router
      :default-active="activeIndex"
      mode="horizontal"
      @select="handleSelect"
      background-color="transparent">
      <el-submenu index="1" v-if="menu_name_list.includes('测试配置管理') === true">
        <template slot="title">测试配置管理</template>
        <el-submenu index="1-1" v-if="menu_name_list.includes('测试结果管理') === true">
          <template slot="title">测试结果管理</template>
          <el-menu-item :index='"/home/" + path + "DemandUp"' v-if="menu_name_list.includes('测试结果查询') === true">测试结果查询</el-menu-item>
        </el-submenu>
        <el-submenu index="1-2" v-if="menu_name_list.includes('测试模板管理') === true">
          <template slot="title">测试模板管理</template>
          <el-menu-item :index='"/test_template"' v-if="menu_name_list.includes('用例模板管理') === true">测试模板管理</el-menu-item>
          <el-menu-item :index='"/test_case"' v-if="menu_name_list.includes('测试用例管理') === true">测试用例管理</el-menu-item>
          <el-menu-item :index='"/batch_config"' v-if="menu_name_list.includes('批量配置管理') === true">批量配置管理</el-menu-item>
        </el-submenu>
      </el-submenu>

      <el-submenu index="2" v-if="menu_name_list.includes('业务场景测试') === true">
        <template slot="title">业务场景测试</template>
        <el-menu-item :index='"/home/"+path+"wholeProcess"' v-if="menu_name_list.includes('PaaS全流程测试') === true">PaaS全流程测试</el-menu-item>
      </el-submenu>

      <el-submenu index="3" v-if="menu_name_list.includes('任务管理') === true ">
        <template slot="title">任务管理</template>
        <el-menu-item :index='"/task_manage"' v-if="menu_name_list.includes('任务配置') === true">任务配置管理</el-menu-item>
        <el-menu-item :index='"/task_flow"' v-if="menu_name_list.includes('任务流水线') === true">任务流水线</el-menu-item>
      </el-submenu>

      <el-submenu index="4" v-if="menu_name_list.includes('系统管理') === true">
        <template slot="title">系统管理</template>
        <el-menu-item :index='"/user"' v-if="menu_name_list.includes('用户管理') === true">用户管理</el-menu-item>
        <el-menu-item :index='"/role"' v-if="menu_name_list.includes('角色管理') === true">角色管理</el-menu-item>
      </el-submenu>

      <el-submenu index="5" v-if="menu_name_list.includes('运营数据管理') === true ">
        <template slot="title">运营数据管理</template>
        <el-menu-item :index='"/show_operate_data"' v-if="menu_name_list.includes('数据运营统计') === true">数据运营统计</el-menu-item>
        <el-menu-item :index='"/operate_data_config"' v-if="menu_name_list.includes('运营数据配置') === true">运营数据配置</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
  import {getCookie} from "../../../service/cookie";
  import api from "../../../service/api";

  export default {
    data() {
      return {
        path: '',
        activeIndex: '2',
        menu_name_list: []
      }
    },
    methods: {
      handleSelect(key) {
        this.$router.push({
          path: key
        }).catch(_ => {
          console.log('已经在该页面')
        })
      },
    },
    mounted() {
      this.path = getCookie('url_path')
      let data = {
        role_id: getCookie('user_role_id'),
      }
      api.login_out_api.query_role_authority(data).then(res => {
        this.menu_name_list = res.info[0].menu_name_list
      })
    },
  }
</script>
<style lang="scss">
  .header__nav {
    margin-left: 26px;
    z-index: 99;

    .el-menu--horizontal > .el-menu-item {
      height: 68px;
      line-height: 68px;
      color: rgba(255, 255, 255, 0.8);
      background: transparent !important;
      font-size: 16px;
    }

    .el-menu--horizontal > .el-submenu .el-submenu__title {
      color: rgba(255, 255, 255, 0.8) !important;
      height: 52px;
      line-height: 54px;
      background: transparent !important;
      font-size: 16px;
    }

    .el-menu--horizontal > .el-menu-item.is-active {
      border-bottom: none;
      color: #fff;
      background: #2e58f7 !important;
    }

    .el-menu--horizontal > .el-submenu.is-active .el-submenu__title {
      border-bottom: none;
      color: #fff;
      background: #2e58f7 !important;
    }
  }

  .el-menu--horizontal {
    background: #fff;
  }

  .el-menu--horizontal .el-menu-item:not(.is-disabled):focus,
  .el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
    color: #fff;
  }

  .el-menu--horizontal > .el-submenu:focus,
  .el-menu--horizontal > .el-submenu:hover {
    color: #fff;
  }

  .el-menu--horizontal .el-menu .el-submenu__title,
  .el-menu--horizontal .el-menu .el-menu-item {
    color: #444;

    &:hover {
      color: #444;
      background: rgba(46, 88, 247, 0.1) !important;
    }
  }
</style>
