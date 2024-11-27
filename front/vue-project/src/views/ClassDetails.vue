<template>
  <div class="common-layout">
    <el-container>
      <el-header
          style="padding:0;margin-top: -8px; position: fixed; width: 100%; z-index: 999;">
        <Header></Header>
      </el-header>
      <el-container style="margin-top: 50px;">
        <el-main style="margin: 0 50px; background-color: white">
          <ClassStudent></ClassStudent>
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
import ClassStudent from '@/components/ClassStudent.vue'
// @ is an alias to /src
export default {
  name: "ClassDetails",
  components: {
    Header,
    ClassStudent
  },
  data() {
    return {}
  },
  beforeRouteEnter: (to, from, next) => { // 写在当前组件
    to.meta.keepAlive = false
    next()
  },
  created() {
    if (!localStorage.getItem('token') || !localStorage.getItem('user_type') === 'teacher') {
      this.$router.push('/teacher/class')
    }
  }
}
</script>
