<template>
  <span style="width: 300px; height: 200px; text-align: center;">
        <div>
            <img v-if="rowData.image" :src="rowData.image" class="image"
                 style="width: 200px; height: 200px; margin: 0 auto;">
        </div>
    </span>
  <el-descriptions class="margin-top" :column="3" border
                   style=" margin: 10px auto;">
    <div v-for="(item, key) in labels">
      <el-descriptions-item :key="key"
                            :label="item"
                            v-if="rowData[key]">
        <div v-if="key==='birth'">
          {{ formatDate(rowData[key]) }}
        </div>
        <div v-else-if="key==='session.create_time'">
          {{ $filters.formatDate(rowData[key]) }}
        </div>
        <div v-else-if="key==='salary'">
          {{ formatSalary(rowData[key]) }}
        </div>
        <div v-else>
          {{ rowData[key] }}
        </div>
      </el-descriptions-item>
      <el-descriptions-item
          v-else-if="['skill', 'practice', 'award', 'introduction'].includes(key)"
          :key="'else_' + key"
          :label="item"
          :span="3">
        <div>
          {{ rowData[key] }}
        </div>
      </el-descriptions-item>
    </div>
  </el-descriptions>
  <div style="margin: 0 auto; display: flex; flex-direction: row;">
    <span style="margin: 0 auto">
      <span v-if="(rowData.status===0 || !rowData.status)">
        <el-button @click="invite()" type="primary"
                   v-if="user_type==='company'">
          邀请面试
        </el-button>
        <el-button type="warning" disabled
                   v-else-if="user_type==='student'">
          等待公司确认
        </el-button>
      </span>
        <span v-else-if="rowData.status===1">
          <span v-if="user_type==='company'">
            <el-button @click="invite(rowData)" type="warning" disabled>
              等待学生确认
            </el-button>
          </span>
          <span v-else-if="user_type==='student'">
            <el-button @click="processInterview(rowData, 2)" type="primary">
              接受
            </el-button>
            <el-button @click="processInterview(rowData, 3)" type="danger">
              拒绝
            </el-button>
          </span>
        </span>
      <span v-else-if="rowData.status===2">
        <span v-if="user_type==='company'">
        <el-button @click="processInterview(rowData, 4)" type="primary">
          面试通过
        </el-button>
        <el-button @click="processInterview(rowData, 5)" type="danger">
          面试不通过
        </el-button>
        </span>
        <el-button type="warning" disabled
                   v-else-if="user_type==='student'">
          等待面试结果
        </el-button>
      </span>
      <span v-else-if="rowData.status===3">
        <el-button @click="deleteSession(rowData)" type="danger"
                   v-if="user_type==='company'">
          学生已拒绝，删除会话
        </el-button>
        <el-button type="danger" disabled v-else-if="user_type==='student'">
          已拒绝
        </el-button>
      </span>
      <span v-else-if="rowData.status===4">
        <span v-if="user_type==='company'">
          <el-button type="warning" disabled>
            面试通过，等待确认
          </el-button>
        </span>
        <span v-else-if="user_type==='student'">
          <el-button type="primary"
                     @click="salaryDialogVisible=!salaryDialogVisible">
            确认入职
          </el-button>
          <el-button type="danger" @click="processInterview(rowData, 7)">
            放弃入职
          </el-button>
        </span>
      </span>
      <span v-else-if="rowData.status===5">
        <span v-if="user_type==='student'">
          <el-button
              type="success" @click="deleteSession(rowData)">
            面试不通过，删除会话
          </el-button>
        </span>
        <span v-else-if="user_type==='company'">
          <el-button type="danger" @click="deleteSession(rowData)" disabled>
            面试不通过
          </el-button>
        </span>
      </span>
    <span v-else-if="rowData.status===6">
          <el-button type="success" disabled>
            招聘完成
          </el-button>
      </span>

    <span v-else-if="rowData.status===7">
        <span v-if="user_type==='company'">
          <el-button type="danger" @click="deleteSession(rowData)">
            学生放弃入职，删除会话
          </el-button>
        </span>
        <span v-else-if="user_type==='student'">
          <el-button type="danger" disabled>
            已放弃入职
          </el-button>
        </span>
      </span>
    <span v-else-if="rowData.status===8">
        <span v-if="user_type==='company'">
          <el-button type="danger" @click="deleteSession(rowData)">
            学生已有工作，删除会话
          </el-button>
        </span>
        <span v-else-if="user_type==='student'">
          <el-button type="danger" disabled>
            已签订合同，等待公司删除会话
          </el-button>
        </span>
    </span>
    </span>
    <el-dialog v-model="interviewDialogVisible" style="width: 400px">
      <el-form style="width: 400px; padding: 0; margin: 0"
               ref="interview" :model="interview">
        <el-form-item
            style="margin: 10px auto; width: 400px; padding-left: 30px"
            :label="interview.work.label" required
            label-width="80px"
            :prop="interview.work.prop"
            :rules="interview.work.rules">
          <el-select v-model="interview.work.value"
                     :placeholder="interview.work.placeholder" disabled
                     v-if="!options" class="custom-select-width">
          </el-select>
          <el-select v-model="interview.work.value"
                     placeholder="请选择工作岗位" class="custom-select-width"
                     v-else>
            <el-option
                v-for="option in options"
                :key="option.value"
                :label="option.label"
                :value="option.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="interview.date.label" required label-width="80px"
                      style="margin: 10px auto;padding-left: 30px"
                      :prop="interview.date.prop"
                      :rules="interview.date.rules">
          <el-date-picker style="width: 200px;"
                          v-model="interview.date.value"
                          type="datetime"
                          :disabledDate="disabledDate"
                          :placeholder="interview.date.placeholder">
          </el-date-picker>
        </el-form-item>
        <el-form-item :label="interview.place.label" required label-width="80px"
                      style="margin: 10px auto;padding-left: 30px"
                      :prop="interview.place.prop"
                      :rules="interview.place.rules">
          <el-input v-model="interview.place.value" style="width: 200px"
                    :placeholder="interview.place.placeholder"
                    type="textarea"
                    resize="none"
                    :autosize="{ minRows: 3 }"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button style="margin: 0 auto; width: 80px" type="primary"
                     @click="submit('interview')">确认
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog v-model="salaryDialogVisible" width="400px">
      <el-form ref="accurateSalary" :model="accurateSalary">
        <el-form-item :label="accurateSalary.salary.label" required
                      label-width="80px"
                      style="margin: 10px auto;padding-left: 30px"
                      :prop="accurateSalary.salary.prop"
                      :rules="accurateSalary.salary.rules">
          <el-input v-model="accurateSalary.salary.value"
                    :placeholder="accurateSalary.salary.placeholder"
                    style="width: 250px;"
                    type="number" min="1000">
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button style="margin: 0 auto; width: 80px" type="primary"
                     @click="entryWork('accurateSalary', rowData, accurateSalary.salary.value)">
            确认
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<style>
.custom-select-width .el-input {
  width: 200px;
}
</style>
<script>
import moment from 'moment-timezone';

export default {
  name: "ReadResume",
  data() {
    return {
      salaryDialogVisible: false,
      interviewDialogVisible: false,
      interview: {
        place: {
          value: "",
          label: "面试地点",
          placeholder: "请输入面试地点",
          prop: "place.value",
          rules: [{required: true, message: '请输入面试地点', trigger: 'blur'}]
        },
        date: {
          value: new Date(),
          label: "面试时间",
          placeholder: "请输入面试时间",
          prop: "date.value",
          rules: [{required: true, message: '请输入面试时间', trigger: 'blur'}]
        },
        work: {
          value: this.rowData.work_name,
          label: "工作岗位",
          placeholder: "请选择工作岗位",
          prop: "work.value",
          rules: [{required: true, message: '请选择工作岗位', trigger: 'blur'}]
        }
      },
      accurateSalary:
          {
            salary: {
              value: 1000,
              label: "实际薪资",
              placeholder: '输入薪资',
              prop: 'salary.value',
              rules: [{required: true, message: '请输入薪资', trigger: 'blur'},
                {validator: this.validateSalary, trigger: 'blur'}]
            }
          },
      user_type: localStorage.getItem('user_type'),
      labels: {
        name: '姓名',
        email: "邮箱",
        phone: "手机号",
        education: '学历背景',
        major: '所学专业',
        work: '期望岗位',
        city: '期望城市',
        salary: "薪资",
        birth: "生日",
        skill: "擅长的技能",
        practice: "实习经历",
        award: '获得奖项',
        introduction: "自我介绍",
        work_name: "投递的工作",
        "session.create_time": "投递时间",
      },
    }
  },
  props: {
    visible: Boolean,
    rowData: Object
  },
  methods: {
    validateSalary(rule, value, callback) {
      if (value >= 1000) {
        callback();
      } else {
        callback(new Error('薪水必须大于等于1000'));
      }
    },
    processInterview(rowData, operate) {
      this.$axios.put("company/session",
          {
            account: localStorage.getItem('account'),
            session_id: rowData.id,
            status: operate
          })
          .then(res => {
                this.$message({
                  message: '确认面试邀请' + res.data.message,
                  type: 'success'
                })
                window.location.reload();
              }
          )
    }
    ,
    formatDate(value) {
      if (!value) return '';

      // 使用moment格式化日期
      return moment.utc(value).format('YYYY年M月');
    },
    formatSalary(value) {
      let temp = ""
      if (value) {
        temp = value.toString().replace(/\[|\]/g, '')
        temp = temp.replace(/,/g, '-')
        temp = temp.replace(/ /g, '')
      }
      return temp
    },
    invite() {
      this.interviewDialogVisible = !this.interviewDialogVisible
    },
    submit(formName) {
      this.$refs[formName].validate((valid) => {
            if (valid) {
              let work_name = ''
              let work_id = ''
              if (this.options) {
                work_id = this.interview.work.value
                work_name = this.work_map[work_id];
                this.$axios.post("/company/session", {
                  company_name: localStorage.getItem('username'),
                  company_id: localStorage.getItem('account'),
                  student: this.rowData.account,
                  date: this.interview.date.value,
                  place: this.interview.place.value,
                  work_name: work_name,
                  work_id: work_id,
                  status: 1,
                })
                    .then(res => {
                      this.$message({
                        message: '面试邀请发送' + res.data.message,
                        type: 'success'
                      });
                      const now_time = new Date().toLocaleString();
                      this.$router.push({
                        name: 'pool',
                        params: {
                          date: now_time
                        }
                      })
                    })
                    .catch(err => {
                      this.$message({
                        message: err.response.data.message,
                        type: 'error'
                      });
                    })
              } else {
                this.$axios.put('/company/session',
                    {
                      account: localStorage.getItem('account'),
                      session_id: this.rowData.id,
                      status: 1,
                      date: this.interview.date.value,
                      place: this.interview.place.value,
                    })
                    .then(res => {
                      this.$message({
                        message: '面试邀请发送' + res.data.message,
                        type: 'success'
                      });
                      const now_time = new Date().toLocaleString();
                      this.$router.push({
                        name: 'pool',
                        params: {
                          date: now_time
                        }
                      })
                    })
                    .catch(err => {
                      this.$message({
                        message: err.response.data.message,
                        type: 'error'
                      });
                    })
              }
            } else {
              return false
            }
          }
      )
    },
    deleteSession(rowData) {
      this.$axios.delete('/company/session', {
        data: {
          session_id: rowData.id,
          account: localStorage.getItem('account')
        }
      })
          .then(res => {
            this.$message({
              message: '删除会话' + res.data.message,
              type: 'success'
            });
            this.$router.go("/")

          })
    },
    entryWork(formName, rowData, salary) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('student/work',
              {
                session_id: rowData.id,
                student: localStorage.getItem('account'),
                company_name: rowData.company_name,
                work_name: rowData.work_name,
                city: rowData.city,
                salary: salary,
                work: rowData.work,
              })
              .then(res => {
                    this.$message({
                      message: '入职' + res.data.message,
                      type: 'success'
                    });
                    const now_time = new Date().toLocaleString()
                    this.$router.push(
                        {
                          name: '/',
                          params: {
                            date: now_time
                          }
                        }
                    )
                  }
              )
              .catch(
                  err => {
                    this.$message({
                      message: err.response.data.message,
                      type: 'error'
                    });
                  }
              )
        } else {
          return false
        }
      })
    },
    disabledDate(time) {
      return time.getTime() < Date.now();
    }
  },
  created() {
    if (!this.rowData.work_name || this.rowData.work_name === '') {
      this.$axios.get('/company/work',
          {params: {company: localStorage.getItem('username')}})
          .then(res => {
            const temp = []
            const temp_map = {}
            res.data.result.forEach(item => {
              temp.push(
                  {
                    label: item.title,
                    value: item.id,
                  }
              )
              temp_map[item.id] = item.title
            })
            this.work_map = temp_map
            this.options = temp
          })
    }
  }
}
</script>