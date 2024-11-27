<template>
    <span style="width: 300px; height: 200px; text-align: center;"
          v-if="ModifyDescStatus">
        <el-upload class="image-uploader"
                   action="http://localhost:3100/user/image"
                   :show-file-list="false"
                   :on-success="handleImageSuccess">
            <img v-if="form.image.value" :src="form.image.value" class="image"
                 style="width: 200px; height: 200px; margin: 0 auto;">
            <i-ep-plus v-else
                       style="margin: 0 auto; width: 200px; height: 200px; "></i-ep-plus>
        </el-upload>
    </span>
  <span v-else style="width: 300px; height: 200px; text-align: center;">
        <div>
            <img v-if="form.image.value" :src="form.image.value" class="image"
                 style="width: 200px; height: 200px; margin: 0 auto;">
        </div>
    </span>
  <el-descriptions class="margin-top" :column="3" border
                   style=" margin: 100px auto;">
    <el-descriptions-item v-for="(item, key) in show_form " :key="key"
                          :label="item.label">
        <div v-if="ModifyDescStatus">
          <el-input v-if="item.label === '用户类型'" v-model="item.value" disabled></el-input>
          <el-input v-else v-model="item.value"></el-input>
        </div>
        <div v-else>
          {{ item.value }}
        </div>
    </el-descriptions-item>
    <template #title>
      <el-button type="warning" @click="dialogVisiblePass = true">修改密码
      </el-button>
    </template>
    <template #extra>
      <el-button type="danger" @click="changeModifyStatus"
                 v-if="ModifyDescStatus">取消编辑
      </el-button>
      <el-button type="primary" @click="changeModifyStatus" v-else>编辑信息
      </el-button>
    </template>
  </el-descriptions>
  <el-button type="primary" @click="modifyDesc" v-if="ModifyDescStatus">提交
  </el-button>
  <el-dialog v-model="dialogVisiblePass" title="修改密码" :append-to-body='true'
             width="35%">
    <ModifyPass></ModifyPass>
  </el-dialog>
</template>

<script>
import ModifyPass from "@/components/ModifyPass.vue"

export default {
  name: "userDesc",
  components: {
    ModifyPass,
  },
  data() {
    return {
      image: "",
      ModifyDescStatus: false,
      dialogVisiblePass: false,
      form: {
        account: {
          value: "",
          label: "account",
          prop: "form.account",
          rules: [
            {required: true, message: '请输入账号', trigger: 'blur'},
            {min: 4, max: 20, message: '账号长度必须为4-20字符', trigger: 'blur'},
            {
              pattern: /^[a-zA-Z0-9_]+$/,
              message: '账号只能包含字母、数字和下划线',
              trigger: 'blur'
            }
          ]
        },
        username: {
          value: "",
          label: "用户名",
          placeholder: '请输入昵称',
          type: "text",
          prop: 'form.username',
          rules: [{required: true, message: '请输入账号', trigger: 'blur'}]
        },
        phone: {
          value: "",
          label: "电话",
          placeholder: '请输入电话',
          prop: 'form.phone',
          rules: [
            {required: true, message: '请输入账号', trigger: 'blur'},
            {
              pattern: /^1\d{10}$/,
              message: '请输入正确的手机号',
              trigger: 'blur'
            }]
        },
        email: {
          value: "",
          label: "邮箱",
          placeholder: "请输入邮箱",
          prop: 'form.email',
          rules: [
            {
              required: true,
              message: '请输入邮箱',
              trigger: 'blur',
            },
            {
              type: 'email',
              message: '请输入有效邮箱',
              trigger: ['blur', 'change'],
            },
          ]
        },
        image: {
          value: "",
          label: 'image',
          rules: [
            {
              required: true,
              message: "请上传头像",
              trigger: 'blur'
            }
          ]
        },
        introduce: {
          value: "",
          label: "用户简介"
        },
        user_type: {
          value: "",
          label: "用户类型"
        }
      },
      show_form: {},
    }
        ;
  },
  methods: {
    handleImageSuccess(res) {
      this.form.image.value = res.image
    },
    modifyDesc() {
      const post_form =
          {
            account: this.form.account.value,
            username: this.form.username.value,
            phone: this.form.phone.value,
            email: this.form.email.value,
            image: this.form.image.value,
            introduce: this.form.introduce.value || '',
            user_type: this.form.user_type.value,
          }
      this.$axios.put("/user/account", post_form).then(res => {
        ElMessage({
          showClose: true,
          message: '账户信息修改' + res.data.message + ",请重新登录",
          type: 'success',
        })
        localStorage.clear()
        this.$router.go("/")
      }).catch(error => {
            ElMessage({
              showClose: true,
              message: error.response.data.message,
              type: 'error',
            })
          }
      )
    },
    changeModifyStatus() {
      this.ModifyDescStatus = !this.ModifyDescStatus
    }
  },
  created() {
    const user = localStorage.getItem("account")
    this.$axios.get("/user/account", {
      params: {account: user}
    }).then(res => {
      const result = res.data.result
      this.form.account.value = result.account
      this.form.username.value = result.username
      this.form.phone.value = result.phone
      this.form.email.value = result.email
      this.form.user_type.value = result.user_type
      this.form.image.value = result.image
      this.form.introduce.value = result.introduce
      
      this.show_form.username = this.form.username
      this.show_form.phone = this.form.phone
      this.show_form.email = this.form.email
      this.show_form.user_type = this.form.user_type
      this.show_form.introduce = this.form.introduce


    }).catch(error => {
    });
  }
}
</script>