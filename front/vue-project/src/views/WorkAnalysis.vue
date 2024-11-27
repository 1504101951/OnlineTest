<template>
  <div class="common-layout">
    <el-container>
      <el-header
          style="padding:0;margin-top: -8px; position: fixed; width: 100%; z-index: 999;">
        <Header></Header>
      </el-header>
      <el-container
          style="margin-top: 50px;">
        <el-main style="margin: 0 50px;background-color: white">
          <div style="display: flex; flex-direction: row">
            <PieChart style="margin: 0 auto"
                      :chartData="jobPercent.chartData"
                      :chartTitle="jobPercent.chartTitle"
                      :chartSeries="jobPercent.chartSeries"
                      :key="jobPercent.chartKey">

            </PieChart>
            <h1 style="position: absolute; line-height: 400px; right: 300px">
              {{ jobPercent.chartDesc }}</h1>
          </div>
          <div style="display: flex; flex-direction: row">
            <BarChart style="margin: 0 auto"
                      :chartData="jobCity.chartData"
                      :chartTitle="jobCity.chartTitle"
                      :chartSeries="jobCity.chartSeries"
                      :key="jobCity.chartKey"
                      :keyword="jobCity.keyWord">
            </BarChart>
            <BarChart style="margin: 0 auto"
                      :chartData="jobType.chartData"
                      :chartTtitle="jobType.chartTitle"
                      :chartSeries="jobType.chartSeries"
                      :key="jobType.chartKey"
                      :keyword="jobType.keyWord">
            </BarChart>
          </div>
        </el-main>
      </el-container>

    </el-container>
  </div>
</template>
<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>

<script>
import Header from '@/components/Header.vue'
import BarChart from '@/components/BarChart.vue'// @ is an alias to /src
import PieChart from "@/components/PieChart";

export default {
  name: "WorkAnalysis",
  components: {
    Header,
    BarChart,
    PieChart
  },
  data() {
    return {
      jobPercent: {
        chartData: [],
        chartTitle: "",
        chartSeries: [],
        chartDesc: "",
        chartKey: "",
      },
      jobCity:
          {
            chartData: [],
            chartTitle: "",
            chartSeries: [],
            chartKey: "",
          },
      jobType:
          {
            chartData: [],
            chartTitle: "",
            chartSeries: [],
            chartKey: "",
          },
      user_type: localStorage.getItem('user_type'),
    }
  },
  methods: {
    getJobRate() {
      this.$axios.get("teacher/jobPercent", {
        params: {
          account: localStorage.getItem('account')
        }
      })
          .then(res => {
            this.jobPercent.chartData = res.data.result
            this.jobPercent.chartTitle = '班级就业详情'
            this.jobPercent.chartSeries = '就业率'
            this.jobPercent.chartDesc = res.data.workDesc
            this.jobPercent.chartKey = new Date()
          })
          .catch(err => {
            this.$message({
              type: 'error',
              message: err.response.data.message
            })
            const now_time = new Date().toLocaleString()
            this.$router.push(
                {
                  name: 'home',
                  params: {
                    date: now_time
                  }
                }
            )
          })
    },
    getJobCity() {
      this.$axios.get("teacher/job", {
        params: {
          account: localStorage.getItem('account'),
          group_keyword: "city"
        }
      })
          .then(res => {
            this.jobCity.chartData = res.data.result
            this.jobCity.chartTitle = "就业城市分析"
            this.jobCity.chartSeries = [
              {
                name: '城市就业人数',
                type: 'bar',
                data: res.data.result.map(item => item.total),
                yAxisIndex: 1
              },
              {
                name: '城市人均薪资',
                type: 'line',
                data: res.data.result.map(item => item.salary),
                yAxisIndex: 0
              }
            ]
            this.jobCity.chartKey = new Date()
            this.jobCity.keyWord = 'city'
          })
    },
    getJobType() {
      this.$axios.get("teacher/job", {
        params: {
          account: localStorage.getItem('account'),
          group_keyword: "work"
        }
      })
          .then(res => {
            this.jobType.chartData = res.data.result
            this.jobType.chartTitle = "就业岗位分析"
            this.jobType.chartSeries = [
              {
                name: '岗位就业人数',
                type: 'bar',
                data: res.data.result.map(item => item.total),
                yAxisIndex: 1
              },
              {
                name: '岗位人均薪资',
                type: 'line',
                data: res.data.result.map(item => item.salary),
                yAxisIndex: 0
              }
            ]
            this.jobType.chartKey = new Date()
            this.jobType.keyWord = 'work'
          })
    },
  },
  created() {
    if (localStorage.getItem('token') && localStorage.getItem('user_type') === 'teacher') {
      this.getJobRate()
      this.getJobCity()
      this.getJobType()
    }
  },
  beforeRouteEnter: (to, from, next) => { // 写在当前组件
    to.meta.keepAlive = false
    next()
  },

}
</script>
