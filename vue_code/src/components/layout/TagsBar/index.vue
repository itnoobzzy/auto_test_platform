<template>
  <ul class="tagsbar">
    <li v-for="(item, i) in breadList" :key="i" @click="to_path(item)">{{ item.meta.title }} <i
      class="el-icon-error tagsbar__close" @click.stop="close(item, i)"></i></li>
  </ul>
</template>

<script>
  import {getCookie} from "../../../service/cookie";

  export default {
    created() {
      this.getBreadcrumb()
    },
    data() {
      return {
        breadList: []
      }
    },
    watch: {
      $route() {
        this.getBreadcrumb()
      }
    },
    methods: {
      // 获取path等信息
      getBreadcrumb() {
        let route_list = []
        route_list.push(this.$route)
        this.breadList.forEach(item => {
          if (this.$route.name !== item.name) {
            route_list.push(item)
          }
        })
        this.breadList = route_list
      },
      // 点击跳转至指定path
      to_path(item) {
        this.$router.push({
          path: item.fullPath
        }).catch(_ => {
          console.log('已经在该页面')
        })
      },
      // 关闭对应面包屑标签
      close(item, i) {
        let path = getCookie('path')
        this.breadList.splice(i, 1)
        // 关闭后刷新界面
        try {
          this.to_path(this.breadList[0])
        }catch (e) {
          this.$router.push({
            path: '/home/' + path + 'wholeProcess'
          }).catch(_ => {
            console.log('已经在该页面')
          })
        }
      }
    }
  }
</script>
<style lang="scss" scoped>
  .tagsbar {
    background: #fff;
    padding: 8px 23px;
    display: flex;
    align-items: center;

    li {
      padding: 6px 12px;
      line-height: normal;
      background: #f3f4f7;
      border-radius: 15px;
      color: #211f1f;
      font-size: 14px;
      margin-right: 11px;
    }

    &__close {
      color: lightgray;
    }
  }
</style>
<style>
  .tagsbar li:hover {
    background-color: lightblue;
    cursor: pointer;
  }

  .tagsbar__close:hover {
    color: red;
  }

  .tagsbar > li:first-child {
    background-color: lightslategray;
  }

</style>
