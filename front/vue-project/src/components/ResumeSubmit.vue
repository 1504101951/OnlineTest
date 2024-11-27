<template>
  <el-form :label-position="center" :model="form"
           style="text-align: center; width: 100%;" ref="form" :rules="rules">
    <el-card shadow="hover" style="width: 1000px; margin: 20px auto;">
      <h1 style="">我的简历</h1>
      <div style="display: flex; flex-direction: row;
          text-align: center; margin: 0 auto; width: 600px;">
        <span style="width: 380px">
              <span style="display: flex; flex-direction: row">
              <el-form-item v-for="user_info in form.user_info_list"
                            :label="user_info.label"
                            label-width="80px"
                            :prop="user_info.prop" :rules="user_info.rules">
                <el-input
                    v-model="form.user_info_list[Object.keys(user_info)[0]]"
                    style="width: 120px; margin: 0 auto;"
                    :placeholder="user_info.placeholder">
              </el-input>
              </el-form-item>
              </span>
        <span style="display: flex; flex-direction: row">
              <el-form-item v-for="user_edu in form.user_edu_list"
                            :label="user_edu.label"
                            label-width="80px"
                            :prop="user_edu.prop" :rules="user_edu.rules">
                <el-cascader
                    v-model="form.user_edu_list[Object.keys(user_edu)[0]]"
                    :options="user_edu.options"
                    style="width: 120px"
                    :placeholder="user_edu.placeholder">
              </el-cascader>
              </el-form-item>
                </span>
              <span style="display: flex; flex-direction: row">
          <el-form-item required
                        v-for="work_label in form.work_label_list"
                        :prop="work_label.prop"
                        style="margin: 0;" :label="work_label.label"
                        :rules="work_label.rules"
                        label-width="80px">
          <el-cascader
              v-model="form.work_label_list[Object.keys(work_label)[0]]"
              :options="work_label.options"
              style="width: 120px"
              :placeholder="work_label.label">
          </el-cascader>
        </el-form-item>
              </span>
        <span style="display: flex; flex-direction: row; margin: 10px 0;">

          <el-form-item label="性别" required label-width="80px">
              <el-cascader
                  v-model="form.gender.gender"
                  :options="form.gender.options"
                  style="width: 120px"
                  :placeholder="form.gender.placeholder">
              </el-cascader>
            </el-form-item>
          <el-form-item label="生日" required label-width="80px">
                <el-date-picker
                    v-model="form.birth"
                    type="month"
                    placeholder="出生年月" style="width: 120px">
                </el-date-picker>
            </el-form-item>
            </span>
            <el-form-item label="邮箱" label-width="80px" prop="email"
                          style="width: 500px">
              <el-input v-model="form.email"
                        placeholder="请输入邮箱"
                        style="width: 340px; margin: 0; padding-right: 20px">
              </el-input>
            </el-form-item>
          </span>
        <span style="margin-left: 30px">
          <el-form-item prop="image"
                        style="width: 180px; text-align: center; padding: 0; margin: 0">
                    <el-card style="width: 180px; height: 235px; padding: 0;"
                             shadow="never"
                             :body-style="{padding: '0px', margin: '0px'}">
                        <el-upload class="avatar-uploader"
                                   action="http://localhost:3100/user/image"
                                   :show-file-list="false"
                                   :on-success="handleAvatarSuccess">
                            <i-ep-plus v-if="form.image === ''"
                                       style="margin: auto auto; width: 100px;
                                 height: 100px; padding-top: 50px">
                            </i-ep-plus>
                            <img v-else-if="form.image!=='default.jpg'"
                                 :src="form.image"
                                 class="avatar"
                                 style="width: 180px; height: 235px; padding: 0;margin: 0">
                            <img v-else
                                 :src="require('@/assets/imgs/default.jpg')"
                                 class="avatar"
                                 style="width: 180px; height: 235px; padding: 0;margin: 0">
                        </el-upload>
                    </el-card>
            </el-form-item>
              </span>
      </div>
      <div style="width: 600px; padding-left: 75px">
        <el-form-item label="薪资" prop="salary" label-width="80px"
                      style="text-align: center; margin: 20px auto; width: 390px;">
          <div style="width: 500px;">
            <div class="block">
              <el-slider
                  v-model="form.salary" range :marks="form.marks"
                  :min="3000" :max="18000" step="1000"
                  style="padding-left: 10px; width: 500px; margin-bottom: 10px">
              </el-slider>
            </div>
          </div>
        </el-form-item>
      </div>
      <el-form-item v-for="exp in form.experience" :prop="exp.prop"
                    label-width="80px" :label="exp.label"
                    style="text-align: center; margin: 20px auto; width: 580px;">
        <el-input v-model="form.experience[Object.keys(exp)[0]]"
                  :placeholder="exp.placeholder"
                  style="width: 580px; margin: 0 auto;" type="textarea"
                  resize="none"
                  :autosize="{ minRows: 4 }"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="SubmitResume('form')"
                   style="margin: 10px auto; width: 100px;"
                   size="large">
          保存简历
        </el-button>
      </el-form-item>
    </el-card>
  </el-form>
</template>

<script>
export default {
  name: "ResumeSubmit",
  data() {
    return {
      rules: {
        salary: [
          {required: true, message: '请选择意向薪资', trigger: 'blur'}
        ],
        image: [
          {required: true, message: '请上传证件照', trigger: 'blur'}
        ],
        gender: [
          {required: true, message: '请选择性别', trigger: 'blur'}
        ],
        email: [
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
        ],
      },
      form: {
        birth: this.$moment(new Date(2000, 0, 1)),
        username: localStorage.getItem("id"),
        image: '',
        salary: [5000, 9000],
        marks: {
          4000: '4000元',
          7000: '7000元',
          10000: {
            style: {
              color: '#1989FA'
            },
            label: '10000元',
          },
          15000: '15000元'
        },
        gender: {
          gender: 'man',
          options: [
            {
              value: "man",
              label: '男',
            },
            {
              value: 'woman',
              label: '女'
            }
          ],
          placeholder: '请选择性别'
        },
        experience: [
          {
            skill: '',
            prop: 'experience.skill',
            label: '技能特长',
            placeholder: '请输入掌握的技能',
          },
          {
            award: '',
            prop: 'experience.award',
            placeholder: '请输入获奖详情',
            label: '获奖详情'
          },
          {
            practice: '',
            label: '实习经历',
            prop: 'experience.practice',
            placeholder: '请输入实习经历',
          },

        ],
        user_info_list: [
          {
            name: "",
            label: "姓名",
            prop: "user_info_list.name",
            placeholder: '请输入姓名',
            rules: [
              {required: true, message: '请输入姓名', trigger: 'blur'},
            ]
          },
          {
            phone: "",
            label: "电话",
            prop: "user_info_list.phone",
            placeholder: '请输入电话',
            rules: [
              {required: true, message: '请输入手机号', trigger: 'blur'},
              {
                pattern: /^1\d{10}$/,
                message: '请输入正确的手机号',
                trigger: 'blur'
              }
            ]
          },
        ],
        user_edu_list: [
          {
            education: '',
            label: "学历",
            placeholder: "请选择教育背景",
            prop: 'user_edu_list.education',
            options: [
              {
                label: "专科",
                value: "专科"
              },
              {
                label: "本科",
                value: "本科"
              },
              {
                label: "硕士",
                value: '硕士',
              },
              {
                label: '博士',
                value: "博士"
              },
              {
                label: "其他",
                value: '其他'
              }
            ],
            rules: [
              {required: true, message: '请选择教育背景', trigger: 'blur'},
            ],
          },
          {
            major: '',
            label: "专业",
            placeholder: '请选择专业',
            prop: "user_edu_list.major",
            options: [
              {
                value: '计算机科学与技术',
                label: '计算机科学与技术'
              },
              {
                value: '电子商务',
                label: '电子商务'
              },
              {
                value: '汉语言文学',
                label: '汉语言文学'
              },
              {
                value: '国际贸易',
                label: '国际贸易'
              },
              {
                value: '土木工程',
                label: '土木工程'
              },
              {
                value: '机械工程',
                label: '机械工程'
              },
              {
                value: "不限",
                label: "不限"
              }
            ],
            rules: [
              {required: true, message: '请选择专业', trigger: 'blur'},
            ],
          },
        ],
        email: "",
        work_label_list: [
          {
            work: '',
            label: "岗位",
            prop: 'work_label_list.work',
            options: [
              {
                value: '后端开发',
                label: '后端开发'
              },
              {
                value: '前端开发',
                label: '前端开发'
              },
              {
                value: '产品设计',
                label: '产品设计'
              },
              {
                value: '产品运营',
                label: '产品运营'
              },
              {
                value: '项目经理',
                label: '项目经理'
              },
              {
                value: '其他',
                label: '其他'
              },
            ],
            rules: [
              {required: true, message: '请选择岗位', trigger: 'blur'},
            ],
          },
          {
            city: '',
            label: "城市",
            prop: 'work_label_list.city',
            options: [
              {
                value: '杭州',
                label: '杭州'
              },
              {
                value: '宁波',
                label: '宁波'
              },
              {
                value: '温州',
                label: '温州'
              },
              {
                value: '绍兴',
                label: '绍兴'
              },
              {
                value: "湖州",
                label: "湖州"
              },
              {
                value: '嘉兴',
                label: '嘉兴'
              },
              {
                value: '金华',
                label: '金华'
              },
              {
                value: '衢州',
                label: '衢州'
              },
              {
                value: '台州',
                label: '台州'
              },
              {
                value: '丽水',
                label: '丽水'
              },
              {
                value: '舟山',
                label: '舟山'
              },
              {
                value: '省外',
                label: '省外'
              },
            ],
            rules: [
              {required: true, message: '请选择意向城市', trigger: 'blur'},
            ],
          }

        ]
      },
    }
  },
  methods: {
    handleAvatarSuccess(res) {
      this.form.image = res.image
    },
    formatDate(date)
    {
      return date.format("YYYY-MM-DD HH:mm:ss")
    },
    SubmitResume(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post("/student/resume/" + localStorage.getItem("account"), {
            name: this.form.user_info_list.name,
            email: this.form.email,
            phone: this.form.user_info_list.phone,
            education: this.form.user_edu_list.education[0],
            major: this.form.user_edu_list.major[0],
            work: this.form.work_label_list.work[0],
            city: this.form.work_label_list.city[0],
            image: this.form.image,
            skill: this.form.experience.skill,
            practice: this.form.experience.practice,
            award: this.form.experience.award,
            salary: this.form.salary,
            birth: this.formatDate(this.form.birth),
            gender: this.form.gender.gender,
          })
              .then(res => {
                ElMessage({
                  showClose: true,
                  message: "简历上传" + res.data.message,
                  type: 'success',
                })
                this.$router.push({
                  name: 'resume', params: {
                    account: localStorage.getItem('account')
                  }
                })
                window.location.reload();
              })
              .catch(error => {
                ElMessage({
                  showClose: true,
                  message: "简历上传" + error.response.data.message,
                  type: 'error',
                })
              })
        } else {
          return false
        }
      })
    },
  },
  created() {
    this.$axios.get("/student/resume/" + this.$route.params.account).then(res => {
      const data = res.data.result
      if (data) {
        this.form.user_info_list.name = res.data.result.name || ''
        this.form.email = res.data.result.email || ''
        this.form.user_info_list.phone = res.data.result.phone || ''
        this.form.user_edu_list.education = [res.data.result.education] || ['']
        this.form.user_edu_list.major = [res.data.result.major] || ['']
        this.form.work_label_list.work = [res.data.result.work] || ['']
        this.form.work_label_list.city = [res.data.result.city] || ['']
        this.form.image = res.data.result.image || ''
        this.form.experience.skill = res.data.result.skill || ''
        this.form.experience.practice = res.data.result.practice || ''
        this.form.experience.award = res.data.result.award || ''
        this.form.salary = res.data.result.salary || [5000, 9000]
        this.form.birth = res.data.result.birth || this.$moment(new Date(2000, 0, 1))
      }
    })
  }
}
</script>