<template>
  <el-form
    :label-position="center"
    :model="form"
    style="text-align: center"
    ref="form"
    :rules="rules"
  >
    <el-row>
      <span
        style="
          min-width: 200px;
          margin: 0 auto;
          height: 230px;
          line-height: 200px;
        "
      >
        <el-upload
          class="avatar-uploader"
          action="http://localhost:3100/user/image"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
        >
          <img
            v-if="form.image"
            :src="require(`@/assets/${form.image}`)"
            class="avatar"
            style="width: 200px; height: 200px; margin: 0 auto"
          />
          <i-ep-plus
            v-else
            style="margin: 0 auto; width: 50px; height: 50px"
          ></i-ep-plus>
        </el-upload>
      </span>
      <span style="margin: 0 auto">
        <span style="text-align: center; margin: 0 auto; width: 300px">
          <el-form-item
            :label="item.label"
            :prop="item.prop"
            label-width="80px"
            v-for="item in form.el_item"
            :rules="item.rules"
          >
            <el-input
              v-model="form.el_item[Object.keys(item)[0]]"
              :placeholder="item.placeholder"
              style="width: 250px"
              :type="item.type ? item.type : 'text'"
            >
            </el-input>
          </el-form-item>
        </span>
        <el-form-item label="输入简介" label-width="80px">
          <el-input
            placeholder="请输入简介"
            v-model="form.introduce"
            maxlength="20"
            show-word-limit
            style="width: 250px"
          ></el-input>
        </el-form-item>
      </span>
    </el-row>
    <el-form-item>
      <el-button
        type="primary"
        @click="register('form')"
        style="margin: 10px auto; width: 100px"
        size="large"
        >注册
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      form: {
        image: "imgs/default/default.jpg",
        el_item: [
          {
            account: "",
            label: "输入账号",
            placeholder: "请输入账号",
            prop: "el_item.account",
            rules: [
              { required: true, message: "请输入账号", trigger: "blur" },
              {
                min: 4,
                max: 20,
                message: "账号长度必须为4-20字符",
                trigger: "blur",
              },
              {
                pattern: /^[a-zA-Z0-9_]+$/,
                message: "账号只能包含字母、数字和下划线",
                trigger: "blur",
              },
            ],
          },
          {
            username: "",
            label: "输入昵称",
            placeholder: "请输入昵称",
            type: "text",
            prop: "el_item.username",
            rules: [{ required: true, message: "请输入账号", trigger: "blur" }],
          },
          {
            password: "",
            label: "输入密码",
            placeholder: "请输入密码",
            prop: "el_item.password",
            type: "password",
            rules: [
              { required: true, message: "请输入密码", trigger: "blur" },
              {
                min: 6,
                max: 20,
                message: "密码长度应为6-20个字符",
                trigger: "blur",
              },
              {
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
                message: "密码必须包含大小写字母和数字",
                trigger: "blur",
              },
            ],
          },
          {
            check_passwd: "",
            label: "确认密码",
            placeholder: "请再次输入密码",
            prop: "el_item.check_passwd",
            type: "password",
            rules: [
              { required: true, message: "请再次输入新密码", trigger: "blur" },
              {
                validator: (rule, value, callback) => {
                  if (value !== this.form.el_item.password) {
                    callback(new Error("两次输入的密码不一致"));
                  } else {
                    callback();
                  }
                },
                trigger: "blur",
              },
            ],
          },
          {
            phone: "",
            label: "输入电话",
            placeholder: "请输入电话",
            prop: "el_item.phone",
            rules: [
              { required: true, message: "请输入账号", trigger: "blur" },
              {
                pattern: /^1\d{10}$/,
                message: "请输入正确的手机号",
                trigger: "blur",
              },
            ],
          },
          {
            email: "",
            label: "输入邮箱",
            placeholder: "请输入邮箱",
            prop: "el_item.email",
            rules: [
              {
                required: true,
                message: "请输入邮箱",
                trigger: "blur",
              },
              {
                type: "email",
                message: "请输入有效邮箱",
                trigger: ["blur", "change"],
              },
            ],
          },
        ],
        isRemember: false,
      },
    };
  },
  methods: {
    handleAvatarSuccess(res) {
      this.form.image = "temp/" + res.image;
    },
    register(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios
            .post("/user/account", {
              account: this.form.el_item.account,
              username: this.form.el_item.username,
              password: this.form.el_item.password,
              check_passwd: this.form.el_item.check_passwd,
              sex: this.form.el_item.sex,
              image: this.form.image,
              email: this.form.el_item.email,
              phone: this.form.el_item.phone,
              introduce: this.form.el_item.introduce,
              profession: this.form.el_item.profession,
              is_admin: this.form.el_item.is_admin,
            })
            .then((res) => {
              ElMessage({
                showClose: true,
                message: res.data.message,
                type: "success",
              });
              this.$router.go("/");
            })
            .catch((error) => {
              ElMessage({
                showClose: true,
                message: "注册失败," + error.response.data.message,
                type: "error",
              });
            });
        } else {
          return false;
        }
      });
    },
  },
};
</script>
<style>
/* CSS样式 */
.el-form-item__label {
  text-align: left;
  height: 10px;
  line-height: 10px;
}

.custom-input {
  width: 250px;
}
</style>
