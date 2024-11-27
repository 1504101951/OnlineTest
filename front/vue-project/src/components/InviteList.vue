<template>
  <el-table ref="filterTable" :data="items" style="width: 100%">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" style="width: auto">
      <template #default="scope" v-if="column.prop==='is_read'">
        {{ scope.row.is_read ? '是' : '否' }}
      </template>
      <template #default="scope"
                v-else-if="column.prop==='create_time' || column.prop==='date'">
        {{ $filters.formatDate(scope.row.create_time) }}
      </template>
    </el-table-column>
    <el-table-column style="margin: 0 auto" label="面试进度">
      <template #default="scope">
        <el-tag :type="status[scope.row.status].tag">
          {{ status[scope.row.status].label }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column prop="id" label="查看详情" width="auto">
      <template #default="scope">
        <el-button @click="showResume(scope.row.id)" type="primary">
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
      status: {
        0: {
          label: "等待公司确认",
          tag: "info"
        },
        1: {
          label: "请确认",
          tag: ""
        },
        2: {
          label: "等待面试结果",
          tag: "warning"
        },
        3: {
          label: "已拒绝",
          tag: "danger"
        },
        4: {
          label: "面试通过，请确认是否入职",
          tag: ""
        },
        5: {
          label: "面试未通过，删除会话",
          tag: "danger"
        },
        6: {
          label: "已接受入职",
          tag: "success"
        },
        7: {
          label: "已放弃入职",
          tag: "danger"
        },
        8: {
          label: "已签订合同，等待公司删除",
          tag: "danger"
        }
      },
      row: [],
      dialogVisible: false,
      dialogData: [],
      columns: [
        {
          prop: "work_name",
          label: "工作标题"
        },
        {
          prop: 'place',
          label: "面试地点"
        },
        {
          prop: "company_name",
          label: "公司"
        },
        {
          prop: "date",
          label: "面试时间"
        },
        {
          prop: "is_read",
          label: "是否已读"
        }
      ],
      currentPage: 0,
      limit: 10,
      total: 0,
      items: [],
      keywords: "",
    }
  },
  methods: {
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
    this.$axios.get('/student/invite', {
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