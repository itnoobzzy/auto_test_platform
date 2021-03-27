<template>
  <CardBox :title="'智能测试库平台-'+area" height="100%">
    <template slot="body">
      <el-row class="echarts_box" :gutter="76">
        <el-col v-for="item in count" :span="6" class="rel">
          <div :ref="'chart'+item" class="echarts_item"></div>
        </el-col>
      </el-row>
    </template>
  </CardBox>
</template>

<script>
  import CardBox from '@/components/common/CardBox'
  import api from "../../../service/api";
  import {getCookie} from "../../../service/cookie";

  export default {
    components: {
      CardBox
    },
    created() {
      this.product_name = JSON.parse(this.$route.query.info).product_name;
      this.area = JSON.parse(this.$route.query.info).area;
      this.get_param_map()
    },
    mounted() {
      this.handle_draw_bar()
    },
    data () {
      return {
        count: 0,
        loading: false,
        product_name: '',
        area: '',
        param_list: []
      }
    },
    methods: {
      // 画柱状图
      drawLine (id, title, xdata, data) {
        // 基于准备好的dom，初始化echarts实例
        let myChart = this.$echarts.init(id)
        // 绘制图表
        myChart.setOption({
          title: {
            text: title,
            textStyle: {
              color: '#333',
              fontSize: 14
            }
          },
          grid: {
            x: 0,
            x2: 0,
            y: '20%',
            y2: 0,
            containLabel: true
          },
          tooltip: {},
          xAxis: {
            data: xdata,
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLabel: {
              color: '#333',
              textStyle: {
                fontSize: 12
              }
            }
          },
          yAxis: {
            axisLabel: {
              color: '#333',
              textStyle: {
                fontSize: 12
              }
            },
            splitLine: {
              lineStyle: {
                type: 'dashed',
                color: '#ccc'
              }
            },
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            }
          },
          series: [
            {
              name: title,
              type: 'bar',
              barWidth: 16,
              label: {
                show: true,
                position: 'outside',
                formatter: '{c}',
                fontSize: 12,
                textStyle: {
                  color: '#333'
                }
              },
              itemStyle: {
                normal: {
                  barBorderRadius: 30,
                  color: params => {
                    // console.log('params', params)
                    if (params.data > 80 && params.seriesName.indexOf('状态') > -1){
                      return '#db0505'
                    }else {
                      return '#05c9db'
                    }
                  }
                }
              },
              data: data
            }
          ]
        })
      },
      // 获取需要展示的参数
      get_param_map() {
        let data = {
          area: this.area,
          product_name: this.product_name,
          user_id:getCookie('user_id')
        }
        api.operate_data_api.get_detail_info(data).then(response =>{
          if (response.status === 0) {
            this.count = response.info.length
            this.param_list = response.info
            this.handle_draw_bar()
          }else {
            this.$message.error('系统异常，请联系管理员！')
          }
        })
      },
      // 将获取的参数画柱状图
      handle_draw_bar() {
        this.$nextTick(() => {
        console.log('this.$refs', this.$refs)
          this.param_list.forEach((item, index) => {
            let chart = 'chart' + (index + 1)
            let title = item.title + '(' + item.unit + ')'
            let data = item.data
            this.drawLine(
              this.$refs[chart][0],
              title,
              ['上月', '当月', '当月目标'],
              data
            )
          })
        })
      }
    }
  }
</script>
<style lang="scss" scoped>
  .echarts_item{
    width: 100%;

  }
  .tips_icon{
    right: 38px;
  }
</style>
