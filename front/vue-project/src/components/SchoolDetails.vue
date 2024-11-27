<template>
  <el-form :label-position="center" :model="form"
           style="text-align: center; width: 100%;" ref="form">
    <el-card shadow="hover" style="width: 1000px; margin: 20px auto;">
      <h1 style="">学校信息</h1>
      <span
          style="margin: 0 auto; display: flex; flex-direction: row; width: 640px">
      <el-form-item label="学校名称"
                    label-width="80px"
                    prop="name.value" required :rules="form.name.rules"
                    style="width: 320px; margin: 20px 0">
        <el-input
            v-model="form.name.value"
            placeholder="请输入学校名称"
            style="width: 200px; margin: 0;" :disabled="!is_edit">
        </el-input>
      </el-form-item>
      <el-form-item label="联系手机" label-width="80px" prop="phone.value"
                    :rules="form.phone.rules"
                    style="width: 320px; margin: 20px 0">
        <el-input v-model="form.phone.value"
                  placeholder="请输入联系方式"
                  style="width: 300px;" :disabled="!is_edit">
        </el-input>
      </el-form-item>
        </span>
      <el-form-item prop="image.value" required
                    style="width: 700px; text-align: center; margin: 0 auto"
                    :rules="form.image.rules">
        <el-card style="width: 640px; height: 360px; margin: 10px auto;"
                 shadow="never"
                 :body-style="{padding: '0px', margin: '0px auto'}">
          <el-upload class="avatar-uploader"
                     action="http://localhost:3100/user/image"
                     :show-file-list="false"
                     :on-success="handleAvatarSuccess"
                     v-if="is_edit">
            <i-ep-plus v-if="form.image.value===''"
                       style="margin: auto auto; width: 200px;
                                 height: 360px;">
            </i-ep-plus>
            <img v-else-if="form.image.value!=='default.jpg'"
                 :src="form.image.value"
                 class="avatar"
                 style="width: 640px; height: 360px; padding: 0;margin: 0">
            <img v-else
                 :src="require('@/assets/imgs/default.jpg')"
                 class="avatar"
                 style="width: 180px; height: 235px; padding: 0;margin: 0">
          </el-upload>
          <span v-else>
                        <img v-if="form.image.value!=='default.jpg'"
                             :src="form.image.value"
                             class="avatar"
                             style="width: 640px; height: 360px; padding: 0;margin: 0">
            <img v-else
                 :src="require('@/assets/imgs/default.jpg')"
                 class="avatar"
                 style="width: 180px; height: 235px; padding: 0;margin: 0">
          </span>
        </el-card>
      </el-form-item>
      <el-form-item label="联系邮箱" label-width="80px" prop="email.value"
                    :rules="form.email.rules"
                    style="width: 640px; margin: 20px auto">
        <el-input v-model="form.email.value"
                  placeholder="请输入邮箱"
                  style="width: 580px;" :disabled="!is_edit">
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="warning" @click="is_edit = !is_edit"
                   v-if="user_type === 'admin' && !is_edit"
                   style="margin: 10px auto; width: 100px;"
                   size="large">
          编辑学校信息
        </el-button>
        <el-button type="primary" @click="submit('form')"
                   v-if="user_type === 'admin' && is_edit"
                   style="margin: 10px auto; width: 100px;"
                   size="large">
          提交
        </el-button>
      </el-form-item>
    </el-card>
  </el-form>
</template>

<script>
export default {
  name: "SchoolManager",
  data() {
    return {
      user_type: localStorage.getItem('user_type'),
      is_edit: false,
      form: {
        name: {
          value: '',
          rules: [{required: true, message: '请输入学校名称', trigger: 'blur'}]
        },
        image: {
          value: "",
          rules: [{required: true, message: '请上传学校背景', trigger: 'blur'}]
        },
        email: {
          value: "",
          rules: [{required: true, message: '请输入邮箱', trigger: 'blur'},
            {type: 'email', message: '请输入有效邮箱', trigger: ['blur', 'change']}]
        },
        phone: {
          value: "",
          rules: [{required: true, message: '请输入联系方式', trigger: 'blur'}]
        }
      }
    }
  },
  methods:
      {
        handleAvatarSuccess(res) {
          this.form.image.value = res.image
        },
        submit(formName) {
          this.$refs[formName].validate((valid) => {
            if (valid) {
              this.$axios.post('/admin/schoolInfo',
                  {
                    email: this.form.email.value,
                    school_name: this.form.name.value,
                    phone: this.form.phone.value,
                    school_image: this.form.image.value,
                    account: localStorage.getItem('account')
                  })
                  .then(res => {
                        sessionStorage.clear()
                        ElMessage({
                          showClose: true,
                          message: res.data.message,
                          type: 'success',
                        })
                        this.$router.go("/")
                      }
                  )
                  .catch(
                      error => {
                        ElMessage({
                          showClose: true,
                          message: error.response.data.message,
                          type: 'error',
                        })
                      }
                  )
            }
          })
        }
      },
  created() {
    this.$axios.get('/admin/schoolInfo')
        .then(res => {
          this.form.name.value = res.data.result.school_name
          this.form.email.value = res.data.result.email
          this.form.phone.value = res.data.result.phone
          this.form.image.value = res.data.result.school_image
        })
  }
}
</script>

<style scoped>

</style>