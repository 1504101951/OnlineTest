<template>
    <span style="width: 300px; height: 200px; text-align: center;">
        <el-upload class="image-uploader"
                   action="http://localhost:3100/user/image"
                   :show-file-list="false"
                   :on-success="handleImageSuccess">
            <img v-if="form.image.value" :src="form.image.value" class="image"
                 style="width: 200px; height: 200px; margin: 0 auto;">
        </el-upload>
    </span>
  <el-descriptions class="margin-top" :column="2" border
                   style="margin: 100px auto;">
    <el-descriptions-item v-for="column in columns" :label="column.label">
      <div>
        <el-select v-model='form[column.prop].value'
                   v-if="column.prop==='user_type'"
                   placeholder="请选择班级">
          <el-option
              v-for="option in type_options"
              :key="option.value"
              :label="option.label"
              :value="option.value">
          </el-option>
        </el-select>
        <el-input v-model="form[column.prop].value" v-else></el-input>
      </div>
    </el-descriptions-item>
    <el-descriptions-item
        label="班级"
        v-if="['teacher', 'student'].includes(form.user_type.value)">
      <div>
        <el-select v-model='form.class_info.value'
                   placeholder="请选择班级">
          <el-option
              v-for="option in class_options"
              :key="option.value"
              :label="option.label"
              :value="option.value">
          </el-option>
        </el-select>
      </div>
    </el-descriptions-item>
    <el-descriptions-item label="自我介绍" :span="2">
      <div>
        <el-input v-model="form.introduce.value"></el-input>
      </div>
    </el-descriptions-item>
  </el-descriptions>
  <el-button type="primary" @click="submit(formName)">提交
  </el-button>
</template>

<style>
.el-select .el-input {
  width: 200px;
}
</style>
<script>
export default {
  name: "UserDetails",
  data() {
    return {
      type_options: [
        {
          value: "student",
          label: "学生"
        },
        {
          value: "teacher",
          label: "老师"
        },
        {
          value: "admin",
          label: "管理员"
        },
          {
            value: "company",
            label: "企业"
          }
      ],
      class_options: [],
      form: {
        account: {
          value: this.rowData.account,
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
          value: this.rowData.username,
          label: "用户名",
          placeholder: '请输入昵称',
          type: "text",
          prop: 'form.username',
          rules: [{required: true, message: '请输入账号', trigger: 'blur'}]
        },
        phone: {
          value: this.rowData.phone,
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
          value: this.rowData.email,
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
          value: this.rowData.image,
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
          value: this.rowData.introduce,
          label: "用户简介",
        },
        user_type: {
          value: this.rowData.user_type,
          label: "用户类型",
          rules: [{
            required: true,
            message: "请选择用户类型",
            trigger: 'blur'
          }]
        },
        class_info: {
          value: this.rowData.class_id,
          name: "",
          label: "班级",
        }
      },
      columns: [
        {
          prop: 'account',
          label: "账号"
        },
        {
          prop: "username",
          label: "名称"
        },
        {
          prop: 'user_type',
          label: "用户类型"
        },
        {
          prop: "phone",
          label: "电话"
        },
        {
          prop: "email",
          label: "邮箱"
        },

      ],
      currentPage: 0,
      limit: 10,
      total: 0,
      items: [],
      user_map: {
        company: "公司",
        admin: "管理员",
        student: "学生",
        teacher: "老师"
      }
    }
  },
  props: {
    visible: Boolean,
    rowData: Object,
  },
  methods: {
    handleImageSuccess(res) {
      this.form.image.value = res.image
    },
    submit() {
      this.$axios.put('/user/account', {
        auth_account: localStorage.getItem('account'),
        account: this.form.account.value,
        username: this.form.username.value,
        phone: this.form.phone.value,
        email: this.form.email.value,
        image: this.form.image.value,
        introduce: this.form.introduce.value,
        user_type: this.form.user_type.value,
        class_id: this.form.class_info.value,
      })
          .then(res => {
            ElMessage({
              showClose: true,
              message: '修改用户信息' + res.data.message,
              type: 'success',
            })
            this.$router.go('/')
          })
          .catch(
              err => {
                ElMessage({
                  showClose: true,
                  message: err.response.data.message,
                  type: 'error',
                })
              }
          )
    },
  },
  created() {
    if (['student', 'teacher'].includes(this.rowData.user_type)) {
      this.$axios.get('/admin/class', {
        params: {account: localStorage.getItem('account')}
      })
          .then(res => {
            let temp_options = []
            res.data.result.forEach(item => {
              temp_options.push({
                value: item.id,
                label: item.class_name
              })
            })
            this.class_options = temp_options
          })
    }
  },
  watch: {
    rowData: {
      handler(newValue, oldValue) {
        // 更新表单中的字段值
        this.form.account.value = newValue.account;
        this.form.username.value = newValue.username;
        this.form.phone.value = newValue.phone;
        this.form.email.value = newValue.email;
        this.form.image.value = newValue.image;
        this.form.introduce.value = newValue.introduce;
        this.form.user_type.value = newValue.user_type;
        this.form.class_info.value = newValue.class_id;
        // 在这里你可以根据需要进行其他的逻辑处理
      },
      deep: true // 如果 rowData 是一个对象或数组，需要设置 deep 为 true
    }
  },

}
</script>

<style scoped>

</style>