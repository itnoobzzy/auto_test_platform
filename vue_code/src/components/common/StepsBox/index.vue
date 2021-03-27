<template>
  <div class="steps">
    <el-steps :active="active">
      <el-step title="第一步"></el-step>
      <el-step title="第二步"></el-step>
      <el-step title="第三步"></el-step>
      <el-step title="第四步" v-if="active===4"></el-step>
    </el-steps>
  </div>
</template>

<script>
export default {
  props: {
    active: {
      type: Number
    }
  },
  data () {
    return {}
  }
}
</script>
<style lang="scss">
.steps {
  .el-step__icon {
    width: 32px;
    height: 32px;
  }
  .el-step__title {
    font-size: 16px;
    line-height: 32px;
  }
  .el-step__main {
    position: absolute;
    left: 24px;
    top: 0px;
    padding: 0 17px;
    background: #fff;
    white-space: nowrap;
  }
  .el-step__title.is-wait {
    color: #333;
  }
  .el-step__line {
    background: #999;
    height: 1px !important;
  }
  .el-step__icon.is-text {
    border: 1px solid;
  }
  .el-step__icon-inner {
    font-size: 18px;
    font-weight: normal;
  }
  .el-step__title.is-process {
    font-weight: normal;
    color: #333;
  }
  .el-step__head.is-process {
    color: #d0d4d9 !important;
  }
  .is-finish .el-step__icon.is-text {
    background: #2e58f7;
    color: #fff;
  }
  .el-step__title.is-finish {
    color: #333;
  }
  .is-finish .el-step__line {
    background: #2e58f7;
    border: none;
    height: 1px;
  }
  .el-step.is-horizontal .el-step__line {
    top: 15px;
  }
  .el-step__line-inner {
    width: 0 !important;
  }
  .el-step__head {
    width: 97%;
  }
}
</style>
