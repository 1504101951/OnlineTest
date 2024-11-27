<template>
  <div class="common-layout">
    <el-container>
      <el-header
          style="padding:0;margin-top: -8px; position: fixed; width: 100%; z-index: 999;">
        <Header></Header>
      </el-header>
      <el-container style="margin-top: 50px;">
        <el-aside style="width: 200px; padding: 0; margin: 0">
          <UserNav></UserNav>
        </el-aside>
        <el-main style="background-color: white; height: 750px">
          <WorkManager></WorkManager>
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
import Header from '@/components/Header';
import WorkManager from "@/components/WorkManager";
import UserNav from "@/components/UserNav";
// @ is an alias to /src
export default {
  name: "Manager",
  components: {
    Header,
    WorkManager,
    UserNav
  },
  data() {
    return {
      token: localStorage.getItem('token'),
      user_type: localStorage.getItem('user_type'),
    }
  },
  created() {
    if (!this.token || this.user_type !== 'company') {
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
   