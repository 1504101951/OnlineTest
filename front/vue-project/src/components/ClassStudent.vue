<template>
  <el-table ref="filterTable" :data="items" style="width: 100%; min-height: 600px">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" width="auto">
      <template #default="scope" v-if="column.prop==='image'">
        <img :src="scope.row.image" alt="" width="100" height="100">
      </template>
      <template #default="scope" v-else-if="column.prop==='create_time'">
        {{ $filters.formatDate(scope.row.create_time) }}
      </template>
      <template #default="scope" v-else-if="column.prop==='salary'">
        {{ formatSalary(rowData[key]) }}
      </template>
      <template #default="scope" v-else-if="column.prop==='is_worked'">
        <el-tag type="danger" v-if="!scope.row.is_worked">
          暂无工作
        </el-tag>
        <el-tag type="primary" v-else>
          已经就业
        </el-tag>
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
      dialogVisible: false,
      dialogData: [],
      columns: [
        {
          prop: "image",
          label: "头像"
        },
        {
          prop: "username",
          label: "用户名"
        },
        {
          prop: 'name',
          label: "姓名"
        },
        {
          prop: 'phone',
          label: "手机号"
        },
        {
          prop: 'email',
          label: "邮箱"
        },
        {
          prop: "create_time",
          label: "投递时间"
        },
        {
          prop: "is_worked",
          label: '是否就业'
        }
      ],
      currentPage: 1,
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
    showResume(session_id) {
      this.$axios.get("company/session/" + session_id,
          {
            params: {
              account: localStorage.getItem('account')
            }
          })
          .then(res => {
                this.dialogData = res.data.result
                this.dialogVisible = !this.dialogVisible
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
    this.$axios.get('/teacher/class', {
      params: {
        account: localStorage.getItem('account'),
        page: this.currentPage,
        limit: this.limit,
      }
    })
        .then(res => {
          this.class_name = res.data.class_name
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