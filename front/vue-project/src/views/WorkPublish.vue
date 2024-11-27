<template>
  <div class="common-layout">
    <el-container>
      <el-header
          style="padding:0;margin-top: -8px; position: fixed; width: 100%; z-index: 999;">
        <Header></Header>
      </el-header>
      <el-container style="margin-top: 45px; padding: 0">
        <el-main style="margin: 0 50px; background-color: white; height: auto">
          <PublishWork></PublishWork>
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
import Header from '@/components/Header.vue';
import PublishWork from '@/components/PublishWork.vue';
// @ is an alias to /src
export default {
  name: "WorkPublish",
  components: {
    Header,
    PublishWork,
  },
  data() {
    return {
      token: localStorage.getItem('token'),
      username: localStorage.getItem('username')
    }
  },
  created() {
    if (!this.token || !this.username) {
      ElMessage({
        showClose: true,
        message: "请先登录",
        type: 'error',
      }),
          this.$router.push('/')
    }
  }
}
</script>
