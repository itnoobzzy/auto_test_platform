<template>
  <CardBox :title=title height='100%'>
    <template slot="body">
      <div class="step_box">
        <StepsBox :active="active"></StepsBox>
      </div>
      <div class="steq_panel">
        <div class="steq_panel_btn" v-if="active !== 3">
          <el-button
            type="primary"
            plain
            size="mini"
            style="background:none"
            @click="goPrev">上一步</el-button>
          <el-button type="primary" @click="goNext" size="mini">下一步</el-button>
        </div>
        <StepOne v-if="active === 1" ref="step_one"  @next_step="next_step"></StepOne>
        <StepTwo v-else-if='active === 2'
                 ref="step_two_case"
                 :step_one_info="step_one_info"
                 @next_step="next_step">
        </StepTwo>
        <StepThree v-else-if='active === 3'
                   ref="step_three"
                   :step_two_info="step_two_info"
                   :step_one_info="step_one_info"
                   @leave_route="route_leave"
                   @return_first_step="return_first_step"
                   @next_step="next_step">
        </StepThree>
      </div>
    </template>
  </CardBox>
</template>

<script>
  export default {
    components: {
      CardBox: () => import('@/components/common/CardBox'),
      StepsBox: () => import('@/components/common/StepsBox'),
      StepOne: () => import('./panel/steqOne'),
      StepTwo: () => import('./panel/steqTwo'),
      StepThree: () => import('./panel/StepThree')
    },
    data () {
      return {
        active: 1,
        title: '单元全流程测试',
        route_leave_flag: false,
        // 第一步数据
        step_one_info: {},
        // 第二步数据
        step_two_info: {},
        // 第三步数据
        step_three_info: {}

      }
    },
    methods: {
      goPrev () {
        this.active = this.active - 1 > 0 ? this.active - 1 : this.active
        console.log(this.active)
      },
      // 父组件调用子组件的下一步
      goNext () {
        switch (this.active) {
          case 1:
            this.confirm_require_form()
            break
          case 2:
            this.submit_bound_list()
            break
          case 3:
            this.create_test_task()
            break
        }
      },
      // 子组件调用下一步
      next_step(step, info) {
        switch (step) {
          case 'step_one':
            this.step_one_info = info
            break
          case 'step_two':
            this.step_two_info = info
            console.log('step_two', info)
            break
          case 'step_three':
            this.step_three_info = info
            console.log('step_three', info)
            break
        }
        this.active = this.active + 1 > 4 ? this.active : this.active + 1
      },
      // 验证需求录入表单
      confirm_require_form() {
        this.$refs.step_one.confirm_form('form')
      },
      // 提交绑定用例或模板列表
      submit_bound_list() {
        let require_name = this.step_one_info.instance_info.require_name
          if (this.$refs.step_two_case.bind_case_table_data.length ===0) {
            this.$message.warning('请先绑定用例！')
          } else {
            this.$refs.step_two_case.create_test_task(require_name)
          }
      },
      // 生成测试任务
      create_test_task() {
        this.$refs.step_three.update_rate()
      },
      // 子组件调用route_leave
      route_leave() {
        this.route_leave_flag = true
        console.log('leave_route', this.route_leave_flag)
      },
      // 第三步子组件调用返回第一步
      return_first_step() {
        this.active = 1
      }
    },
    mounted() {
      // this.title = this.$route.meta.title
    },
    watch: {
      $route() {
        this.title = this.$route.meta.title
      }
    },
    beforeRouteLeave(to, from, next) {
      if (this.active === 3) {
        if (this.route_leave_flag) {
          next()
          this.route_leave_flag = false
        } else {
          this.$refs.step_three.close_socket()
        }
      } else {
        next()
      }
    }
  }
</script>
<style lang="scss" scoped>
  .step_box {
    padding: 27px 80px 27px 80px;
  }

</style>
<style lang="scss">
  .steq_panel{
    .el-form-item{
      margin-bottom: 15px;
    }
    &_form{
      background: #f8f9fc;
      border-radius: 8px;
      padding: 30px 30px 15px 30px;
    }
    &_btn{
      text-align: center;
      /*margin-top: 72px;*/
      margin-bottom: 10px;
    }
  }
</style>
