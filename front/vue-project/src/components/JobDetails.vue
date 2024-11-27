<template>
  <el-form :model="form" style="text-align: center; width: 100%;" ref="form">
    <el-card shadow="hover" style="width: 600px; margin: 20px auto;">
      <span>
      <h1>就业详情</h1>
      </span>
      <el-form-item v-for='item in form' :label="item.label"
                    :prop="item.prop" :rules="item.rules" label-width="80px"
                    style="margin: 10px auto;padding-left: 30px; width: 300px">
        <el-select v-model="item.value"
                   :placeholder="item.placeholder" class="custom-select-width"
                   v-if="['工作岗位', '工作城市'].includes(item.label)"
                   :disabled="is_worked">
          <el-option
              v-for="option in item.options"
              :key="option.value"
              :label="option.label"
              :value="option.value">
          </el-option>
        </el-select>
        <el-input v-model="item.value" style="width: 200px"
                  v-else-if="item.prop==='salary'" :disabled="is_worked"
                  type="number" :placeholder="item.placeholder"></el-input>
        <el-input v-model="item.value" style="width: 200px"
                  v-else :disabled="is_worked"
                  type="text" :placeholder="item.placeholder"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button v-if="!is_worked"
                   type="primary" @click="SubmitJob('form')"
                   style="margin: 10px auto; width: 100px;" size="large">
          提交工作信息
        </el-button>
      </el-form-item>
    </el-card>
  </el-form>
</template>

<script>
export default {
  name: "StudentJob",
  data() {
    return {
      is_worked: false,
      user_type: localStorage.getItem('user_type'),
      form: {
        salary: {
          value: 1000,
          label: '具体薪资',
          prop: "salary.value",
          placeholder: "请输入具体薪资",
          rules: [
            {required: true, message: '请选择薪资', trigger: 'blur'},
            {validator: this.validateSalary, trigger: 'blur'}
          ],
        },
        company_name: {
          value: "",
          label: "公司名称",
          prop: "company_name.value",
          placeholder: "请输入公司名称",
          rules: [
            {required: true, message: '请输入公司名称', trigger: 'blur'},
          ],
        },
        work_name: {
          value: "",
          label: "工作名称",
          prop: "work_name.value",
          placeholder: "请输入工作名称",
          rules: [
            {required: true, message: '请输入岗位名称', trigger: 'blur'},
          ],
        },
        work: {
          value: "",
          label: "工作岗位",
          prop: "work.value",
          placeholder: "请选择工作岗位",
          rules: [
            {required: true, message: '请选择工作岗位', trigger: 'blur'},
          ],
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
        },
        city: {
          value: "",
          label: "工作城市",
          prop: "city.value",
          placeholder: "请选择工作城市",
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
            {required: true, message: '请选择工作城市', trigger: 'blur'},
          ],
        },
      },
    }
  },
  methods: {
    validateSalary(rule, value, callback) {
      if (value >= 1000) {
        callback();
      } else {
        callback(new Error('薪水必须大于等于1000'));
      }
    },
    SubmitJob(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post("/student/work", {
            student: localStorage.getItem("account"),
            company_name: this.form.company_name.value,
            work_name: this.form.work_name.value,
            city: this.form.city.value,
            salary: this.form.salary.value,
            work: this.form.work.value,
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
    getJobDetails(account) {
      this.$axios.get('/student/work',
          {params: {student: account}})
          .then(res => {
            if (res.data.result) {
              this.form.company_name.value = res.data.result.company_name;
              this.form.work_name.value = res.data.result.work_name;
              this.form.city.value = res.data.result.city;
              this.form.salary.value = res.data.result.salary;
              this.form.work.value = res.data.result.work;
              this.is_worked = true;
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
  },
  created() {
    if (this.$route.params.account) {
      this.getJobDetails(this.$route.params.account)
    } else if (this.user_type === 'student') {
      this.getJobDetails(localStorage.getItem("account"))
    }
  }
}
</script>