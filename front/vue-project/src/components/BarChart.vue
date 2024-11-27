<template>
  <div ref="chart"
       style="width: 600px; height: 400px; background-color: white"></div>
</template>

<script>
export default {
  data() {
    return {
      chart: null
    }
  },
  props: {
    chartData: {
      type: Array,
      required: true
    },
    chartTitle: {
      type: String,
      required: true

    },
    chartSeries: {
      type: Array,
      required: true
    },
    keyword: {
      type: String,
      required: true
    }
  },
  mounted() {
    console.log('-------Bar--------')
    console.log(this.chartData)
    console.log(this.chartTitle)
    console.log(this.chartSeries)
    console.log('-------End--------')
    // 获取容器
    const chartContainer = this.$refs.chart
    // 基于容器初始化echarts实例
    const chart = this.$echarts.init(chartContainer)
    // 使用this.chart保存echarts实例以便后续操作
    this.chart = chart

    // 设置图表配置项和数据
    const option = {
      title: {
        text: this.chartTitle
      },
      tooltip: {},
      xAxis: {
        data: this.chartData.map(item => item[this.keyword])
      },
      yAxis: [{
        name: "平均薪资",
        type: "value",
        position: "left",
        axisLabel: {
          formatter: "{value} 元"
        }
      },
        {
          name: "就业人数",
          type: "value",
          position: "right",
          axisLabel: {
            formatter: "{value}人"
          }
        }],
      series: this.chartSeries
    }

    // 将配置项设置到echarts实例中
    this.chart.setOption(option)
  },
  beforeDestroy() {
    // 在销毁组件时销毁图表实例，防止内存泄漏
    if (this.chart) {
      this.chart.dispose()
    }
  }
}
</script>

<style>
/* 可以添加一些样式来美化图表容器 */
</style>
