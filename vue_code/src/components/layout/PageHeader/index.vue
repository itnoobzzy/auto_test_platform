<template>
  <header class="header">
    <div class="header__left">
      <div class="header__logo">
        <svg-icon type="logo" class="logo" />
        智能测试库平台
      </div>

      <div class="header__nav">
        <Menu></Menu>
      </div>
    </div>

    <div class="header__right">
      <img src="~@/assets/images/pic/default--avatar.png" alt="" class="header__right-avatar">
      <span class="header__right-name">{{user_name}}</span>
      <el-divider direction="vertical"></el-divider>
      <el-link style="color: honeydew;font-size: 16px;" href="/" type="primary">退出</el-link>
    </div>
  </header>
</template>

<script>
import {getCookie} from "../../../service/cookie";

export default {
  components: {
    Menu: () => import('../Menu')
  },
  data() {
    return {
      user_name: getCookie('user_name')
    }
  }
}
</script>
<style lang="scss" scoped>
.header {
  height: 50px;
  background: #272c38;
  padding: 0 16px;
  display: flex;
  align-items: center;
  z-index: 10;
  position: relative;
  justify-content: space-between;
  &__left {
    display: flex;
    align-items: center;
  }
  &__right{
    display: flex;
    align-items: center;
    &-avatar{
      width: 25px;
      height: 25px;
      border-radius: 25px;
      overflow: hidden;
      margin-right: 7px;
    }
    &-name{
      font-size: 16px;
      color: #fff;

    }
    &-exit{
      font-size: 20px;
      padding-left: 17px;
      color: #fff;
      margin-left: 17px;
      cursor: pointer;
      border-left: 1px solid rgba(255,255,255,0.29);;
    }
  }
  &__logo {
    color: #fff;
    font-size: 18px;
    display: flex;
    align-items: center;
    .logo {
      font-size: 32px;
      margin-right: 8px;
    }
  }
  &__nav {
    color: #fff;
  }
}
</style>
