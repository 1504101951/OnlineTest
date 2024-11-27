<template>
  <el-button @click="createClass()" type="primary" style="margin-left: 90%; margin-bottom: 10px">
    新增班级
  </el-button>
  <el-table ref="filterTable" :data="items" style="width: 100%">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" width="auto">
      <template #default="scope" v-if="column.prop==='create_time'">
        {{ $filters.formatDate(scope.row.create_time) }}
      </template>
      <template #default="scope" v-if="column.prop==='update_time'">
        {{ $filters.formatDate(scope.row.update_time) }}
      </template>
    </el-table-column>
    <el-table-column prop="id" label="查看详情" width="200px">
      <template #default="scope">
        <el-button @click="showClass(scope.row)" type="primary"
                   style="width: 100px">
          查看详情
        </el-button>
      </template>
    </el-table-column>
    <el-table-column prop="id" label="操作" width="200px">
      <template #default="scope">
        <el-button @click="editClass(scope.row)" type="warning"
                   style="width: 100px">
          编辑
        </el-button>
        <el-button @click="deleteClass(scope.row.id)" type="danger">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog v-model="dialogVisible" style="width: 1000px">
    <classUser :row-data="dialogData" :key="dialogKey"></classUser>
  </el-dialog>
  <el-pagination v-model="currentPage" :total="total"
                 @current-change="handleCurrentChange" :page-size="10"
                 style="background-color: white; padding-bottom: 10px; padding-top: 5px">
  </el-pagination>
</template>

<script>
import ClassUser from "@/components/ClassUser";

export default {
  name: "ClassList",
  components: {
    ClassUser
  },
  data() {
    return {
      dialogKey: "",
      dialogVisible: false,
      dialogData: [],
      class_info: {},
      columns: [
        {
          prop: "class_name",
          label: "班级"
        },
        {
          prop: "create_time",
          label: "创建时间"
        },
        {
          prop: "update_time",
          label: "更新时间"
        }
      ],
      currentPage: 0,
      limit: 10,
      total: 0,
      items: [],
    }
  },
  methods: {
    createClass() {
      this.$prompt('请输入班级名称', '新增班级', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({value}) => {
        this.$axios.post('admin/class', {
          class_name: value,
          account: localStorage.getItem('account')
        })
            .then(res => {
              this.$message({
                type: 'success',
                message: '创建' + res.data.message
              })
              this.$router.go('/')
            })
            .catch(err => {
              this.$message({
                type: 'danger',
                message: err.response.data.message
              })
            })
      })
          .catch(() => {
            this.$message({
              type: 'warning',
              message: "已取消删除"
            })
          })
    },
    showClass(row) {
      this.dialogData = row;
      this.dialogVisible = true;
      this.dialogKey = new Date();
    },
    editClass(row) {
      this.$prompt('请输入班级名称', '修改班级', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: row.class_name
      }).then(({value}) => {
        this.$axios.put('admin/class', {
          class_name: value,
          class_id: row.id,
          account: localStorage.getItem('account')
        })
            .then(res => {
              this.$message({
                type: 'success',
                message: '创建' + res.data.message
              })
              this.$router.go('/')
            })
            .catch(err => {
              this.$message({
                type: 'danger',
                message: err.response.data.message
              })
            })
      })
          .catch(() => {
            this.$message({
              type: 'warning',
              message: "已取消删除"
            })
          })
    },
    deleteClass(class_id) {
      this.$confirm("此操作将永久删除该班级及其相关信息，是否继续？", '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.delete("admin/userAdmin",
            {
              data: {
                account: localStorage.getItem('account'),
                class_id: class_id
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
    findClass(newPage) {
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
      this.findClass(newPage)
    },
  }
  ,
  created() {
    this.$axios.get('/admin/class', {
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