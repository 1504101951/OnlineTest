<template>
  <el-form
    :label-position="center"
    :model="form"
    style="width: 300px; margin: 60px auto 20px auto; text-align: center"
  >
    <el-form-item>
      <el-input
        v-model="form.account"
        placeholder="请输入账号"
        style="margin: 0 auto"
        size="large"
      >
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-input
        type="password"
        placeholder="请输入密码"
        v-model="form.password"
        show-passwd
        size="large"
      >
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-row>
        <el-switch v-model="form.isRemember" active-text="记住密码" />
      </el-row>
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        @click.prevent="login"
        style="margin: 10px auto; width: 100px"
        size="large"
        >登录
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "Login",
  token: "",
  data() {
    return {
      form: {
        account: "",
        password: "",
        isRemember: false,
      },
    };
  },
  methods: {
    login() {
      this.$axios
        .post("/user/login", {
          account: this.form.account,
          password: this.form.password,
        })
        .then((res) => {
          localStorage.setItem("token", res.data.token);
          localStorage.setItem("image", res.data.result.image);
          localStorage.setItem("username", res.data.result.username);
          localStorage.setItem("account", res.data.result.account);
          ElMessage({
            showClose: true,
            message: res.data.result.username + "欢迎您的登录。",
            type: "success",
          });
          if (this.form.isRemember) {
            localStorage.setItem("password", this.form.password);
          } else {
            localStorage.removeItem("password");
          }
          this.$router.go("/"); 
        })
        .catch((error) => {
          ElMessage({
            showClose: true,
            message: "登录失败," + error.response.data.message,
            type: "error",
          });
        });
    },
  },
  created() {
    if (localStorage.getItem("password")) {
      this.form.account = localStorage.getItem("account");
      this.form.password = localStorage.getItem("password");
    }
  },
};
</script>
