<template>
  <CardBox title="SaaS全流程测试" height='100%'>
    <template slot="body">
      <div class="step_box">
        <StepsBox :active="active"></StepsBox>
      </div>
      <div class="steq_panel">
        <StepOne v-if="active === 1" ref="step_one" @change_button="change_button" @next_step="next_step"></StepOne>
        <StepTwo v-else-if='active === 2 && action===3' ref="step_two_template" @next_step="next_step"></StepTwo>
        <StepTwo2 v-else-if='active === 2 && action===6' ref="step_two_case" @next_step="next_step"></StepTwo2>
        <StepThree v-else-if='active === 3'
                   ref="step_three"
                   :step_two_info="step_two_info"
                   :step_one_info="step_one_info"
                   @next_step="next_step">
        </StepThree>
        <StepFour v-else-if='active === 4'
                  ref="step_four"
                  @leave_route="route_leave"
                  :step_one_info="step_one_info"
                  :step_three_info="step_three_info"></StepFour>
        <div class="steq_panel_btn" v-if="active !== 4">
          <el-button
            type="primary"
            plain
            style="background:none"
            @click="goPrev">上一步</el-button>
          <el-button type="primary" @click="goNext" v-if="this.action !== 9">下一步</el-button>
          <el-button type="primary" @click="goNext" v-if="this.action === 9">立即生成</el-button>
        </div>
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
      StepTwo2: () => import('./panel/steqTwo2'),
      StepThree: () => import('./panel/StepThree'),
      StepFour: () => import('./panel/StepFour')
    },
    data () {
      return {
        action: 3,
        active: 1,
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
      // 改变下一步按钮名字
      change_button(action) {
        this.action = action
      },
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
        this.$refs.step_one.confirm_form('test_numbers')
      },
      // 提交绑定用例或模板列表
      submit_bound_list() {
        let offer_id = this.step_one_info.form.fee_code
        if (this.action === 3) {
          if (this.$refs.step_two_template.bind_template_table_data.length ===0){
            this.$message.warning('请先绑定模板！')
          } else {
            this.$refs.step_two_template.get_case_rate(offer_id)
          }
        } else if (this.action === 6){
          if (this.$refs.step_two_case.bind_case_table_data.length ===0) {
            this.$message.warning('请先绑定用例！')
          } else {
            this.$refs.step_two_case.get_case_rate(offer_id)
          }
        }
      },
      // 生成测试任务
      create_test_task() {
        this.$refs.step_three.update_rate()
      },
      // 子组件调用route_leave
      route_leave(flag) {
        this.route_leave_flag = flag
      }
    },
    mounted() {
    },
    beforeRouteLeave(to, from, next) {
      if (this.active === 4) {
        if (this.route_leave_flag) {
          next()
          this.route_leave_flag = false
        } else {
          this.$refs.step_four.close_socket()
        }
      } else {
        next()
      }
    }
  }
</script>
<style lang="scss" scoped>
  .step_box {
    padding: 27px 80px 62px 80px;
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
      margin-top: 72px;
      margin-bottom: 70px;
    }
  }
</style>
