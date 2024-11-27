<template>
  <div ref="chart"
       style="width: 600px; height: 300px; background-color:white"></div>
</template>

<script>
export default {
  data() {
    return {
      chart: null
    }
  },
  name: 'PieChart',
  props: {
    chartData: {
      type: Array,
      required: true
    },
    chartTitle: {
      type: String,
      required: true
    },
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      // 基于容器初始化echarts实例
      this.chart = this.$echarts.init(this.$refs.chart)

      // 设置图表配置项和数据
      const option = {
        title: {
          text: this.chartTitle,
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
          {
            name: '就业比率',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: this.chartData,
          }
        ]
      }

      // 将配置项设置到echarts实例中
      this.chart.setOption(option)
    }
  },
  beforeDestroy() {
    // 在销毁组件时销毁图表实例，防止内存泄漏
    if (this.chart) {
      this.chart.dispose()
    }
  },
}
</script>

<style scoped>
/* 这里可以添加一些样式来美化图表 */
</style>
