<template>
  <div>
    <el-container style="height: 98vh">
      <el-header
          style="padding:0;margin-top: -8px; position: fixed; width: 100%; z-index: 999;">
        <Header></Header>
      </el-header>
      <el-main style="padding: 0; height: auto; margin: -10px -8px;">
        <div style="height: 100%;">
          <img :src="back_image"
               style="width: 100%; height: 100%; padding: 0;
               margin: 0;z-index: -1; opacity: 0.8" alt=""/>
        </div>
      </el-main>
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
// @ is an alias to /src
export default {
  name: "Home",
  components: {
    Header
  },
  data() {
    return {
      back_image: ""
    }
  },
  created() {
    if(!sessionStorage.getItem('school_image')
    )
    {
      this.$axios.get('/admin/schoolInfo')
          .then(res => {
            sessionStorage.setItem('school_image', res.data.result.school_image)
            sessionStorage.setItem('school_name', res.data.result.school_name)
            this.back_image = res.data.result.school_image
          })
    }
    this.back_image = sessionStorage.getItem('school_image')
  }
}
</script>
