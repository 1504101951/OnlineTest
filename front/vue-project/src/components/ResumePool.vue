<template>
  <el-table ref="filterTable" :data="items" style="width: 100%">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" width="auto">
      <template #default="scope" v-if="column.prop==='is_read'">
        {{ scope.row.is_read ? '是' : '否' }}
      </template>
      <template #default="scope" v-else-if="column.prop==='create_time'">
        {{ $filters.formatDate(scope.row.create_time) }}
      </template>
      <template #default="scope" v-else-if="column.prop==='salary'">
        {{ formatSalary(rowData[key]) }}
      </template>
    </el-table-column>
    <el-table-column label="状态">
      <template #default="scope">
        <el-tag :type="status[scope.row.status].tag">
          {{ status[scope.row.status].label }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column prop="work_id" label="查看详情" width="auto">
      <template #default="scope">
        <el-button @click="showResume(scope.row)" type="primary">
          查看详情
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog v-model="dialogVisible">
    <ReadResume :row-data="dialogData"></ReadResume>
  </el-dialog>
  <el-pagination v-model="currentPage" :total="total"
                 @current-change="handleCurrentChange" :page-size="10"
                 style="background-color: white; padding-bottom: 10px; padding-top: 5px">
  </el-pagination>
</template>

<script>
import ReadResume from "@/components/ReadResume";

export default {
  name: "ResumePool",
  components: {
    ReadResume
  },
  data() {
    return {
      row: [],
      status: {
        0: {
          label: "确认简历",
          tag: ""
        },
        1: {
          label: "等待学生确认",
          tag: "warning"
        },
        2: {
          label: "确认面试结果",
          tag: ""
        },
        3: {
          label: "学生拒绝，删除会话",
          tag: "danger"
        },
        4: {
          label: "面试通过，等待学生确认",
          tag: "warning"
        },
        5: {
          label: "面试不通过",
          tag: "danger"
        },
        6: {
          label: "学生已接受入职",
          tag: "success"
        },
        7: {
          label: "学生已放弃入职",
          tag: "danger"
        },
        8: {
          label: "学生已有工作，删除会话",
          tag: "danger"
        }
      },
      dialogVisible: false,
      dialogData: [],
      columns: [
        {
          prop: "work_name",
          label: "投递的工作"
        },
        {
          prop: 'student',
          label: "学生用户"
        },
        {
          prop: "create_time",
          label: "投递时间"
        },
        {
          prop: "is_read",
          label: "是否已读"
        },
      ],
      currentPage: 0,
      limit: 10,
      total: 0,
      items: [],
      keywords: "",
    }
  },
  methods: {
    formatSalary(value) {
      let temp = ""
      if (value) {
        temp = value.toString().replace(/\[|\]/g, '')
        temp = temp.replace(/,/g, '-')
        temp = temp.replace(/ /g, '')
      }
      return temp
    },
    read(session_id) {
      this.$axios.put("company/session/" + session_id, {
        account: localStorage.getItem('account'),
      })
    },
    showResume(row) {
      this.$axios.get("company/session/" + row.id,
          {
            params: {
              account: localStorage.getItem('account')
            }
          })
          .then(res => {
                this.dialogData = res.data.result
                this.dialogVisible = !this.dialogVisible
                if ([0, 2, 3, 7, 8].includes(row.status)) {
                  this.read(row.id)
                }
              }
          )
    },
    find_work() {
      this.$axios.get('company/work', {
        params: {
          work: this.filters.work,
          city: this.filters.city,
          education: this.filters.education,
          major: this.filters.major,
          company: localStorage.getItem('username'),
          title: this.filters.title,
          page: this.currentPage,
          limit: this.limit
        }
      })
          .then(res => {
            this.currentPage = res.data.page
            this.items = res.data.result
            this.total = res.data.total
            this.filter_cache = this.filters
          })
    },
    handleCurrentChange(newPage) {
      if (this.filter_cache) {
        this.$axios.get('company/work', {
          params: {
            work: this.filter_cache.work,
            city: this.filter_cache.city,
            education: this.filter_cache.education,
            major: this.filter_cache.major,
            company: localStorage.getItem('username'),
            title: this.filter_cache.title,
            page: newPage,
            limit: this.limit
          }
        })
            .then(res => {
              this.currentPage = res.data.page
              this.items = res.data.result
              this.total = res.data.total
            })
            .catch(error => {
              console.log(error)
            })
      } else {
        this.$axios.get('company/work', {
          params: {
            page: newPage,
            limit: this.limit,
            username: localStorage.getItem('username')
          }
        })
            .then(res => {
              this.currentPage = res.data.page
              this.items = res.data.result
              this.total = res.data.total
            })
            .catch(error => {
              console.log(error)
            })
      }
    },
  },
  created() {
    this.$axios.get('/company/session', {
      params: {
        account: localStorage.getItem('account'),
      }
    })
        .then(res => {
          this.currentPage = res.data.page
          this.total = res.data.total
          this.items = res.data.result
        })
  },
  computed: {
    shortDesc() {
      return function (desc) {
        return desc.length > 30 ? desc.substring(0, 30) + "..." : desc;
      }
    }
  },
}
</script>