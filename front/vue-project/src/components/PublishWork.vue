<template>
  <el-form :model="form"
           style="text-align: center; width: 100%;" ref="form" :rules="rules">
    <el-card shadow="hover" style="width: 1000px; margin: 0 auto;">
      <span>
      <h1 v-if="is_edit" style="margin: 0 auto 5px auto">发布招聘公告</h1>
      <h1 v-else>岗位详情</h1>
      </span>
      <div style="text-align: center; margin: 0 auto; width: 600px;">
        <div style="display: flex; flex-direction: row;text-align: center">
          <p v-if="form.company"
             style="color: grey; font-size: 12px; margin: 0 auto 5px auto">
            发布公司:{{ form.company }}
          </p>
          <p v-if="form.update_time"
             style="color: grey; font-size: 12px; margin: 0 auto 5px auto">
            更新时间:{{ this.$moment(form.update_time).format('YYYY-MM-DD') }}
          </p>
        </div>
        <span style="width: 600px">
          <el-form-item label="岗位标题" label-width="100px" prop="title"
                        style="margin: 0 auto 5px auto">
            <el-input v-model="form.title"
                      style="width: 500px; margin: 0 auto; padding:0"
                      :disabled="!is_edit"></el-input>
          </el-form-item>
              <span
                  style="display: flex; flex-direction: row; width: 600px;flex-wrap: wrap;">
          <el-form-item required
                        v-for="item in form.work_info"
                        :prop="item.prop"
                        style="margin: 5px 0;" :label="item.label"
                        :rules="item.rules"
                        label-width="100px">
          <el-cascader
              v-model="form.work_info[Object.keys(item)[0]]"
              :options="item.options"
              style="width: 200px"
              :placeholder="item.label" :disabled="!is_edit">
          </el-cascader>
        </el-form-item>
              </span>
        </span>
      </div>
      <el-form-item label="薪资待遇" prop="salary" label-width="100px"
                    style="text-align: center; margin: 5px auto; width: 600px;">
        <el-slider
            v-if="is_edit" v-model="form.salary" range :marks="form.marks"
            :min="3000" :max="18000" :step="1000"
            style="padding-left: 10px; width: 500px; margin-bottom: 10px">
        </el-slider>
        <span style="display: flex; flex-direction: row" v-else>
          <el-input :value="form.salary[0]" disabled
                    style="width: 200px"></el-input>
          <p style="margin: 0 0; width: 100px; text-align: center; font-size: 20px"> — </p>
          <el-input :value="form.salary[1]" disabled
                    style="width: 200px"></el-input>
        </span>
      </el-form-item>
      <el-form-item v-for="item in form.work" :prop="item.prop"
                    label-width="100px" :label="item.label" :rules="item.rules"
                    style="text-align: center; margin: 10px auto 5px auto; width: 600px;">
        <el-input v-model="form.work[Object.keys(item)[0]]"
                  :placeholder="item.placeholder"
                  style="width: 580px; margin: 0 auto;" type="textarea"
                  :autosize="{ minRows: 3 }" resize="none" :disabled="!is_edit">
        </el-input>
      </el-form-item>
      <span style="width: 600px">
          <el-form-item prop="image"
                        style="width: 600px; margin: 0 auto" label="公司照片"
                        required label-width="100px">
                    <el-card style="width: 500px; height: 150px"
                             :body-style="{padding: '0px'}"
                             shadow="never">
                        <el-upload v-if="is_edit" class="avatar-uploader"
                                   action="http://localhost:3100/user/image"
                                   :show-file-list="false"
                                   :on-success="handleAvatarSuccess"
                                   style="padding: 0">
                            <i-ep-plus v-if="form.image === ''"
                                       style="margin: auto auto; width: 150px;
                                 height: 50px; padding-top: 50px">
                            </i-ep-plus>
                            <img v-else-if="form.image!=='default.jpg'"
                                 :src="form.image"
                                 class="avatar"
                                 style="width: 500px; height: 150px">
                            <img v-else
                                 :src="require('@/assets/imgs/default/default.jpg')"
                                 class="avatar"
                                 style="width: 500px; height: 150px">
                        </el-upload>
                      <span v-else>
                           <i-ep-plus v-if="form.image === ''"
                                      style="margin: auto auto; width: 150px;
                                 height: 100px; padding-top: 50%">
                            </i-ep-plus>
                            <img v-else-if="form.image!=='default.jpg'"
                                 :src="form.image"
                                 class="avatar"
                                 style="width: 500px; height: 150px">
                            <img v-else
                                 :src="require('@/assets/imgs/default/default.jpg')"
                                 class="avatar"
                                 style="width: 500px; height: 150px">
                      </span>
                    </el-card>
            </el-form-item>
              </span>

      <el-form-item>
        <el-button v-if="is_edit"
                   type="primary" @click="PublishWork('form')"
                   style="margin: 10px auto; width: 100px;" size="large">
          发布/编辑岗位
        </el-button>
        <div v-else-if="!is_edit && (user_type ==='admin' || is_owner)"
             style="margin: 0 auto; width: 400px">
          <el-button
              type="primary" @click="is_edit=true"
              style="margin: 10px 20px 10px 20px; width: 100px;" size="large">
            编辑岗位
          </el-button>
          <el-button
              type="danger" @click="deleteWork(form.id)"
              style="margin: 10px 20px 10px 20px; width: 100px;" size="large">
            删除岗位
          </el-button>
        </div>
        <el-button v-else-if="!is_edit && user_type==='student'"
                   type="primary" @click="submitResume()"
                   style="margin: 10px auto; width: 100px;" size="large">
          投递简历
        </el-button>
      </el-form-item>
    </el-card>
  </el-form>
</template>

<script>
export default {
  name: "PublishWork",
  data() {
    return {
      is_owner: false,
      user_type: localStorage.getItem('user_type'),
      is_edit: true,
      rules: {
        salary: [
          {required: true, message: '请选择意向薪资', trigger: 'blur'}
        ],
        image: [
          {required: true, message: '请上传公司照片', trigger: 'blur'}
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
        title: [
          {required: true, message: '请输入标题简介', trigger: 'blur'},
        ]
      },
      form: {
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
        work: [
          {
            responsibility: '',
            prop: 'work.responsibility',
            label: '工作职责',
            placeholder: '请输入工作职责',
            rules: [{required: true, message: '请输入工作职责', trigger: 'blur'}]
          },
          {
            requirement: '',
            prop: 'work.requirement',
            placeholder: '请输入工作需求',
            label: '工作需求',
            rules: [{required: true, message: '请输入工作需求', trigger: 'blur'}]
          },
          {
            welfare: '',
            label: '福利待遇',
            prop: 'work.welfare',
            placeholder: '请输入工作福利待遇',
            rules: [{required: true, message: '请输入福利待遇', trigger: 'blur'}]
          },
        ],
        title: '',
        work_info: [
          {
            education: '',
            label: "学历要求",
            placeholder: "请选择教育背景",
            prop: 'work_info.education',
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
            label: "专业要求",
            placeholder: '请选择专业',
            prop: "work_info.major",
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
            ],
            rules: [
              {required: true, message: '请选择专业', trigger: 'blur'},
            ],
          },
          {
            work: '',
            label: "招聘岗位",
            prop: 'work_info.work',
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
            label: "工作城市",
            prop: 'work_info.city',
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

        ],
      },
    }
  },
  methods: {
    convertRangeStringToNumbers(rangeString) {
      // 使用正则表达式提取数字部分
      const matches = rangeString.match(/(\d+)k-(\d+)k/);
      if (!matches || matches.length !== 3) {
        throw new Error('Invalid range string format');
      }

      // 提取出的数字部分
      const start = parseInt(matches[1]) * 1000; // 将 "3k" 转换为 3000
      const end = parseInt(matches[2]) * 1000;   // 将 "5k" 转换为 5000

      return [start, end];
    },
    handleAvatarSuccess(res) {
      this.form.image = res.image
    },
    submitResume() {
      this.$axios.post("/company/session", {
        student: localStorage.getItem("account"),
        company_name: this.form.company_name,
        work_id: this.form.id,
        work_name: this.form.title,
        company_id: this.form.company_id,
      })
          .then(res => {
            ElMessage({
              showClose: true,
              message: "简历上传" + res.data.message,
              type: 'success',
            })
            this.$router.push('/work/workCenter')
          })
          .catch(error => {
            ElMessage({
              showClose: true,
              message: error.response.data.message,
              type: 'error',
            })
          })
    },
    PublishWork(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post("/company/work", {
            id: this.form.id || null,
            account: localStorage.getItem("account"),
            company: localStorage.getItem("username"),
            title: this.form.title,
            education: this.form.work_info.education[0],
            major: this.form.work_info.major[0],
            work: this.form.work_info.work[0],
            city: this.form.work_info.city[0],
            welfare: this.form.work.welfare,
            responsibility: this.form.work.responsibility,
            requirement: this.form.work.requirement,
            image: this.form.image,
            salary: this.form.salary,
          })
              .then(res => {
                ElMessage({
                  showClose: true,
                  message: '操作' + res.data.message,
                  type: 'success',
                })
                window.location.reload();
              })
              .catch(error => {
                ElMessage({
                  showClose: true,
                  message: error.response.data.message,
                  type: 'error',
                })
              })
        } else {
          return false
        }
      })
    },
    getWorkDetails(work_id) {
      this.$axios.get('/company/work/' + work_id)
          .then(res => {
            this.form.id = res.data.result.id || ''
            this.form.title = res.data.result.title || ''
            this.form.work_info.education = [res.data.result.education] || ['']
            this.form.work_info.major = [res.data.result.major] || ['']
            this.form.work_info.education = [res.data.result.education] || ['']
            this.form.work_info.city = [res.data.result.city] || ['']
            this.form.work_info.work = [res.data.result.work] || ['']
            this.form.image = res.data.result.image || ''
            this.form.work.responsibility = res.data.result.responsibility || ''
            this.form.work.requirement = res.data.result.requirement || ''
            this.form.work.welfare = res.data.result.welfare || ''
            this.form.salary = this.convertRangeStringToNumbers(res.data.result.salary) || [5000, 9000]
            this.form.company_id = res.data.result.company_id || ''
            this.form.company_name = res.data.result.company_name || ''
            this.form.update_time = res.data.result.update_time || new Date()
            if (localStorage.getItem('account') === res.data.result.company_id) {
              this.is_owner = true
            }
          })
          .catch(error => {
                console.log(error)
                if (error.response && error.response.data && error.response.data.message) {
                  ElMessage({
                    showClose: true,
                    message: error.response.data.message,
                    type: 'error',
                  })
                } else {
                  ElMessage({
                    showClose: true,
                    message: '未知报错',
                    type: 'error',
                  })
                }
              }
          )

    },
    deleteWork(work_id) {
      this.$axios.delete('/company/work/' + work_id,
          {
            data: {
              account: localStorage.getItem("account")
            }
          })
          .then(res => {
            ElMessage({
              showClose: true,
              message: "岗位删除" + res.data.message,
              type: 'success',
            })
            const now_time = new Date().toLocaleString();
            this.$router.push({
              name: 'workCenter',
              params: {
                date: now_time
              }
            })
          })
          .catch(error => {
            ElMessage({
              showClose: true,
              message: error.response.data.message,
              type: 'error',
            })
          })
    }
  },
  created() {
    if (this.$route.path === '/work/workDetails/' + this.$route.params.id) {
      if (this.$route.params.id) {
        this.getWorkDetails(this.$route.params.id)
        this.is_edit = false
      } else {
        ElMessage({
          showClose: true,
          message: '找不到该岗位',
          type: 'error',
        })
      }
    }
  }
}
</script>