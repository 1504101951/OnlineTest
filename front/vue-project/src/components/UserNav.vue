<template>
  <el-col :span="12" style="width: 200px; max-width: 100%;">
    <el-menu :default-active="this.$route.path" class="el-menu-vertical-demo"
             style="min-height: 750px; width: 100%;">
      <el-menu-item style="padding: 100px 0;" v-for="item in menu[user_type]"
                    @click="navigationTo(item.url)">
        <span style="margin: 0 auto;text-align: center;">
          {{ item.label }}
        </span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>
<script>
export default ({
  name: "UserNav",
  data() {
    return {
      user_type: localStorage.getItem('user_type'),
      menu: {
        student: [
          {
            name: 'center',
            url: "center",
            label: '个人中心'
          },
          {
            name: "invite",
            url: "invite",
            label: "面试会话"
          },
          {
            name: "job",
            url: 'job',
            label: "工作管理"
          }
        ],
        company: [
          {
            name: 'center',
            url: "center",
            label: '个人中心'
          },
          {
            name: "manager",
            url: 'manager',
            label: "岗位管理"
          },
          {
            name: "pool",
            url: "pool",
            label: "简历池"
          }
        ],
        admin: [
          {
            name: "center",
            url: 'center',
            label: "个人中心"
          }
        ],
        teacher: [
          {
            name: "center",
            url: "center",
            label: "个人中心"
          },
          {
            name: "class",
            url: "class",
            label: "班级管理"
          }
        ]
      }
    }
  },
  methods:
      {
        navigationTo(url) {
          const now_time = new Date().toLocaleString();
          this.$router.push({
            name: url, params: {
              date: now_time
            }
          })
        },
      },
  beforeRouteLeave: (to, from, next) => { //写在前一个组件
    to.meta.keepAlive = false
    next()
  },
})
</script>