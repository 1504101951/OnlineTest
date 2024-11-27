<template>
  <div>
    <el-form :model="form" ref="passwordForm" :rules="rules" label-width="120px"
             style="width: 370px;">
      <el-form-item label="原密码" prop="old_pass">
        <el-input type="password" v-model="form.old_pass" autocomplete="off"
                  show-password clearable></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="passwd">
        <el-input type="password" v-model="form.passwd" autocomplete="off"
                  show-password clearable></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="check_pass">
        <el-input type="password" v-model="form.check_pass" autocomplete="off"
                  show-password clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('passwordForm')">修改密码
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<script>
export default {
  name: "ModifyPass",
  data() {
    return {
      form: {
        account: localStorage.getItem('account'),
        old_pass: "",
        passwd: "",
        check_pass: "",
        user_type: localStorage.getItem('user_type')
      },
      rules: {
        old_pass: [
          {required: true, message: '请输入原密码', trigger: 'blur'}
        ],
        passwd: [
          {required: true, message: '请输入新密码', trigger: 'blur'},
          {min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur'}
        ],
        check_pass: [
          {required: true, message: '请再次输入新密码', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              if (value !== this.form.passwd) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$axios.put("/user/login", this.form)
              .then(res => {
                ElMessage({
                  showClose: true,
                  message: res.data.message,
                  type: 'success',
                })
                localStorage.clear()
                this.$router.go("/")
              })
              .catch(error => {
                ElMessage({
                  showClose: true,
                  message: '密码修改失败,' + error.response.data.message,
                  type: 'error',
                })
              });
        }
      });
    }
  }
}
</script>