<template>
  <el-table ref="filterTable" :data="items" style="width: 100%">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" width="auto">
      <template #default="scope" v-if="column.prop==='image'">
        <img :src="scope.row.image" alt="" width="100" height="100">
      </template>
      <template #default="scope" v-else-if="column.prop==='introduce'">
        {{ this.shortDesc(scope.row.introduce) }}
      </template>
      <template #default="scope" v-else-if="column.prop==='user_type'">
        {{ user_map[scope.row.user_type] }}
      </template>
    </el-table-column>
    <el-table-column prop="account" label="编辑" width="auto">
      <template #default="scope">
        <el-button @click="editUser(scope.row.account)" type="primary">
          编辑
        </el-button>
      </template>
    </el-table-column>
    <el-table-column prop="account" label="删除" width="auto">
      <template #default="scope">
        <el-button @click="deleteUser(scope.row.account)" type="danger">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination v-model="currentPage" :total="total"
                 @current-change="handleCurrentChange" :page-size="10"
                 style="background-color: white; padding-bottom: 10px; padding-top: 5px">
  </el-pagination>
  <el-dialog v-model="dialogVisible">
    <UserDetails :row-data="dialogData"></UserDetails>
  </el-dialog>
</template>

<script>
import UserDetails from "@/components/UserDetails";

export default {
  name: "UserList",
  components: {
    UserDetails
  },
  data() {
    return {
      dialogVisible: false,
      dialogData: [],
      columns: [
        {
          prop: "image",
          label: "头像"
        },
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
        {
          prop: "introduce",
          label: "自我介绍"
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
  methods: {
    deleteUser(user_account) {
      this.$confirm("此操作将永久删除该用户及其相关信息，是否继续？", '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.delete("admin/userAdmin",
            {
              data: {
                account: localStorage.getItem('account'),
                user_account: user_account
              }
            })
            .then(res => {
                  this.$message(
                      {
                        type: 'success',
                        message: res.data.message
                      }
                  )
                  this.$router.go("/")
                }
            )
            .catch(err => {
              this.$message({
                type: 'error',
                message: err.response.data.message
              })
            })
      })
          .catch(() => {
            this.$message(
                {
                  type: "warning",
                  message: '已取消删除'
                }
            )
          })

    },
    editUser(account) {
      this.$axios.get("user/account", {
        params: {
          account: account
        }
      })
          .then(res => {
            this.dialogData = res.data.result
            this.dialogVisible = true
          })
      .catch(error => {
        console.log(error)
      })
    },
    findUser(newPage) {
      this.$axios.get('admin/userAdmin', {
        params: {
          account: localStorage.getItem('account'),
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
    },
    handleCurrentChange(newPage) {
      this.findUser(newPage)
    },
  }
  ,
  created() {
    this.$axios.get('/admin/userAdmin', {
      params: {
        account: localStorage.getItem('account'),
      }
    })
        .then(res => {
          this.currentPage = res.data.page
          this.total = res.data.total
          this.items = res.data.result
        })
  }
  ,
  computed: {

    shortDesc() {
      return function (desc) {
        return desc.length > 30 ? desc.substring(0, 30) + "..." : desc;
      }
    }
  }
  ,
}
</script>