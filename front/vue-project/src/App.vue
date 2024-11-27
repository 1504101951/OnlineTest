<template>
  <div style="height: 100vh;">
    <img :src="back_image"
         style="width: 100%; height: 100%; padding: 0;
               margin: 0;z-index: -1; opacity: 0.8; position: fixed;" alt=""/>
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" :key="$route.fullPath"></component>
      </keep-alive>
    </router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      back_image: ""
    }
  },
  created() {
    if (!sessionStorage.getItem('school_image')
    ) {
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

