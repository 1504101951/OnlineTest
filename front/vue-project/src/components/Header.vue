<template>
  <div style="min-width: 100%; margin-top: -8px">
    <h1 class="heading">{{ school_name }}</h1>
    <el-menu default-active="activeIndex" mode="horizontal">
      <div v-for="item in nav_header">
        <el-menu-item v-if="item.children == null" :key="item.name"
                      :index="item.name" @click="clickMenu(item)">
          <template #title>
            <span slot="title">{{ item.label }}</span>
          </template>
        </el-menu-item>
        <el-sub-menu v-if="item.children != null" :key="item.name"
                     :index="item.name">
          <template #title>
            <span slot="title">{{ item.label }}</span>
          </template>
          <el-menu-item v-for="child in item.children"
                        :key="item.name + child.name"
                        :index="item.name + child.name"
                        @click="clickMenu(child)">
            {{ child.label }}
          </el-menu-item>
        </el-sub-menu>
      </div>
      <div style="flex-grow: 0.9; display: flex; flex-direction: row">
        <div v-if="token" style="position: absolute; right: 0">
          <el-menu-item :key="user.name" :index="user.name">
            <el-sub-menu :key="user.name" :index="user.name">
              <template #title>
                <img v-if="image=='default.jpg'"
                     :src="require('@/assets/img/' + image)" width="20"
                     height="20"
                     style="padding-right: 10px;"/>
                <img v-else :src="image" width="20" height="20"
                     style="padding-right: 10px;">
                <span slot="title">{{ username }}</span>
              </template>
              <el-menu-item v-for="child in user.children" :key="child.name"
                            :index="child.name" @click="clickMenu(child)">
                <img :src="require('@/assets/img/' + child.icon)" width="20"
                     height="20" style="padding-right: 10px;"/>
                {{ child.label }}
              </el-menu-item>
              <el-menu-item key="message" index="message"
                            @click="clickMenu({name: message_url[user_type]})"
                            style="display: flex; flex-direction: row">
                <img :src="require('@/assets/img/message.png')" width="20"
                     height="20" style="padding-right: 10px;"/>
                消息
                <el-badge :value="messages" v-if="messages"
                          style="line-height: 0; margin-left: 10px;">
                </el-badge>
              </el-menu-item>
              <el-menu-item key="logout" index="logout" @click="logout">
                <img :src="require('@/assets/img/logout.png')" width="20"
                     height="20" style="padding-right: 10px;"/>
                退出登录
              </el-menu-item>
            </el-sub-menu>
          </el-menu-item>
        </div>
        <div v-else style="position: absolute; right: 0">
          <el-row>
            <el-menu-item key="login" index="login"
                          @click="dialogVisibleLogin = !dialogVisibleLogin">
              <template #title>
            <span slot="title">
              <h1>登录</h1>
              <el-dialog v-model="dialogVisibleLogin" title="登录" width="30%"
                         :before-close="handleClose"
                         :append-to-body='true'>
                <Login></Login>
              </el-dialog>
            </span>
              </template>
            </el-menu-item>
            <el-menu-item key="register" index="register"
                          @click="dialogVisibleRegister = !dialogVisibleRegister">
              <template #title>
            <span slot="title">
              <h1>注册</h1>
              <el-dialog v-model="dialogVisibleRegister" title="注册"
                         :before-close="handleClose" :append-to-body='true'
                         width="35%">
                <Register></Register>
              </el-dialog>
            </span>
              </template>
            </el-menu-item>
          </el-row>
        </div>
      </div>
    </el-menu>
  </div>
  <el-backtop :right="100" :bottom="100"/>
</template>

<style>
.el-select .el-input {
  width: 130px;
}

.el-menu {
  min-width: 100%;
}

.input-with-select .el-input-group__prepend {
  background-color: #fff;
}

.flex-grow {
  flex-grow: 0.98;
}

.heading {
  position: absolute; /* 设置标题为绝对定位 */
  top: 10px; /* 将标题置于容器的中间 */
  left: 50%;
  z-index: 999;
  transform: translate(-50%, -50%); /* 居中 */
}
</style>
<script>
// @ is an alias to /src
import Login from "@/components/Login.vue"
import Register from "@/components/Register.vue"

export default {
  name: "Header",
  components: {
    Login,
    Register,
  },
  data() {
    return {
      school_name: "",
      message_url: {
        student: 'invite',
        company: "pool"
      },
      image: localStorage.getItem('image'),
      token: localStorage.getItem('token'),
      user_type: localStorage.getItem('user_type'),
      username: localStorage.getItem("username"),
      nav_header: [],
      search_key: '',
      category: "全部",
      dialogVisibleLogin: false,
      dialogVisibleRegister: false,
      dialogVisibleMessage: false,
      messages: 0,
      menuData: {
        'student': [
          {
            path: "/",
            name: "home",
            label: "首页",
            icon: 'home.png',
            url: "/",
          },
          {
            label: "就业中心",
            name: "workCenter",
            path: '/jobCenter/workCenter/',
            url: '/jobCenter/workCenter/',
          },
          {
            path: "/resume/",
            name: "resume",
            label: "简历管理",
            url: "/resume/",
            param: localStorage.getItem('account'),
          },
        ],
        'company':
            [
              {
                path: '/',
                name: 'home',
                label: "首页",
                icon: 'home.png',
                url: '/'
              },
              {
                path: "/personnel/",
                name: "personnel",
                label: "人才市场",
                url: "/personnel/",
              },
              {
                label: "职业中心",
                name: "jobCenter",
                path: '/jobCenter/',
                url: '/jobCenter/',
                children: [
                  {
                    label: "招聘市场",
                    name: 'workCenter',
                    path: "/workCenter/",
                    url: '/workCenter/'
                  },
                  {
                    label: '岗位发布',
                    name: "workPublish",
                    path: '/workPublish/',
                    url: "/workPublish/",
                  }
                ]
              },
            ],
        'admin':
            [
              {
                path: '/',
                name: 'home',
                label: "首页",
                icon: 'home.png',
                url: '/'
              },
              {
                label: '用户管理',
                name: "userManager",
                path: '/userManager/',
                url: "/userManager/",
              },
              {
                label: "学校管理",
                name: "school",
                path: '/school/',
                url: '/school/',
                children: [
                  {
                    label: "班级管理",
                    name: 'classManager',
                    path: "/classManager/",
                    url: '/classManager/'
                  },

                  {
                    label: "学校管理",
                    name: "schoolManager",
                    path: '/schoolManager/',
                    url: "/schoolManager/",
                  }
                ]
              },
            ],
        'teacher': [
          {
            path: '/',
            name: 'home',
            label: "首页",
            icon: 'home.png',
            url: '/'
          },
          {
            label: '班级详情',
            name: "classDetails",
            path: '/classDetails/',
            url: "/classDetails/",
          },
          {
            label: "就业分析",
            name: "workAnalysis",
            path: '/workAnalysis/',
            url: '/workAnalysis/',
          },
        ],

      },
      user: {
        path: "/user",
        name: "user",
        label: this.username,
        icon: "user.png",
        children: [
          {
            path: "/user/center",
            name: "center",
            label: "个人中心",
            icon: "center.png",
            url: "/user/center",
          },
        ]
      }
    };
  },
  methods: {
    clickMenu(item) {
      if (item.param) {
        this.$router.push(item.path + item.param);
      } else {
        const now_time = new Date().toLocaleString();
        this.$router.push({
          name: item.name, params: {
            date: now_time
          }
        })
      }
    },
    handleClose(done) {
      ElMessageBox.confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {
          });
    },
    logout() {
      localStorage.clear();
      ElMessage({
        showClose: true,
        message: '成功退出登录',
        type: 'success',
      })
      const now_time = new Date().toLocaleString();
      this.$router.push({
        name: 'home', params: {
          date: now_time
        }
      })

    },
    handleStorageChange(event) {

      if (event.key === 'user_type') {
        this.user_type = event.newValue;
      }
    },
    getMessage() {
      if (this.user_type === 'company' || this.user_type === 'student') {
        this.$axios.get('/user/message', {
          params: {
            account: localStorage.getItem('account'),
            is_read: 0,
          }
        })
            .then(res => {
                  this.messages = res.data.total
                }
            )
      }
    },
    listenMessage(user_type) {
      this.nav_header = this.menuData[this.user_type] || this.menuData['student'];
      if (user_type === 'company' || user_type === 'student') {
        this.getMessage()
      }
    },
    getSchoolName() {
      if (!sessionStorage.getItem('school_name')) {
        this.$axios.get('/admin/schoolInfo')
            .then(res => {
              sessionStorage.setItem('school_image', res.data.result.school_image)
              sessionStorage.setItem('school_name', res.data.result.school_name)
              this.school_name = res.data.result.school_name
            })
      }
      this.school_name = sessionStorage.getItem('school_name')
    }
  },
  beforeRouteLeave: (to, from, next) => { //写在前一个组件
    to.meta.keepAlive = false
    next()
  },
  created() {
    this.getSchoolName()
    this.$router.beforeEach((to, from, next) => {
      this.dialogVisibleLogin = false
      this.dialogVisibleRegister = false
      this.dialogVisibleMessage = false
      next()
    });
    window.addEventListener('storage', this.handleStorageChange);
    this.listenMessage(this.user_type);

  },

};
</script>
  