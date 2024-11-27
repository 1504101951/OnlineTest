<template>
  <div style="display: flex; flex-direction: row;
  width: 1200px; text-align: center; margin: 0 auto">
    <p style="margin: 0; padding: 0; line-height: 35px">按条件筛选:</p>
    <span v-for="item in filters" class="formHeader">
    <el-input v-if="item.label === '名称'"
              v-model="filters[Object.keys(item)[0]]"
              :placeholder="item.placeholder"
              style="width: 150px; margin: 0 10px">
    </el-input>
    <el-select v-else clearable
               v-model="filters[Object.keys(item)[0]]"
               :placeholder="item.placeholder"
               style="width: auto; margin: 0 10px">
      <el-option
          v-for="option in item.options"
          :key="option.value"
          :label="option.label"
          :value="option.value">
      </el-option>
    </el-select>
      </span>
    <el-button type="primary" @click="findPersonnel('form')"
               style="margin: 0 auto; width: 100px;">查询
    </el-button>
  </div>
  <el-table ref="filterTable" :data="items" style="width: 100%">
    <el-table-column v-for="column in columns" :prop="column.prop"
                     :label="column.label" width="auto">
      <template #default="scope" v-if="column.prop==='image'">
        <img :src="scope.row.image" alt="" width="100" height="100">
      </template>
      <template #default="scope" v-else-if="column.prop==='salary'">
        {{ formatSalary(scope.row.salary) }}
      </template>
    </el-table-column>
    <el-table-column prop="major" label="专业需求" width="auto">
      <template #default="scope">
        <el-tag :type="tags[scope.row.major].type"
                :effect="tags[scope.row.major].effect"
                disable-transitions>{{ scope.row.major }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="id" label="查看详情" width="auto">
      <template #default="scope">
        <el-button @click="showResume(scope.row.account)" type="primary">
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

<style>
.formHeader .el-select .el-input {
  border-color: #409EFF;
  width: 120px;
  margin: 0;
  padding: 0;
  flex-grow: unset;
}
</style>

<script>
import ReadResume from "@/components/ReadResume";

export default {
  name: "ResumeList",
  components: {
    ReadResume
  },
  data() {
    return {
      dialogVisible: false,
      dialogData: [],
      filters: [
        {
          education: '',
          placeholder: '学历',
          label: '学历',
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
        },
        {
          city: '',
          placeholder: '城市',
          label: '城市',
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
        },
        {
          work: "",
          placeholder: '岗位',
          label: "岗位",
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
        {
          major: '',
          placeholder: '专业',
          label: '专业',
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

        },
        {
          name: '',
          placeholder: '名字',
          label: '名字',
        },
      ],

      columns: [
        {
          prop: "image",
          label: "头像"
        },
        {
          prop: "name",
          label: "名称"
        },
        {
          prop: 'education',
          label: "学历"
        },
        {
          prop: "major",
          label: "专业"
        },
        {
          prop: "work",
          label: "期望岗位"
        },
        {
          prop: "city",
          label: "期望城市"
        },
        {
          prop: "salary",
          label: "期望薪资"
        },
      ],
      currentPage: 1,
      limit: 10,
      total: 0,
      items: [],
      keywords: "",
      tags:
          {
            '计算机科学与技术': {'type': "", "effect": "plain"},
            '电子商务': {'type': "success", "effect": "plain"},
            '汉语言文学': {'type': "danger", "effect": "plain"},
            '国际贸易': {'type': "warning", "effect": "plain"},
            '土木工程': {'type': "success", "effect": "dark"},
            '机械工程': {'type': "info", "effect": "plain"},
            '不限': {'type': "warning", "effect": "dark"}
          }
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
    showResume(account) {
      this.$axios.get("student/resume/" + account,
          {})
          .then(res => {
                this.dialogData = res.data.result
                this.dialogVisible = !this.dialogVisible
              }
          )
    },
    findPersonnel() {
      this.$axios.get('/company/resume', {
        params: {
          work: this.filters.work,
          city: this.filters.city,
          education: this.filters.education,
          major: this.filters.major,
          name: this.filters.name,
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
        this.$axios.get('/company/resume', {
          params: {
            work: this.filters.work,
            city: this.filters.city,
            education: this.filters.education,
            major: this.filters.major,
            name: this.filters.name,
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
        this.$axios.get('company/resume', {
          params: {
            page: newPage,
            limit: this.limit,
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
    this.$axios.get('/company/resume',
        {
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
        return desc.length > 20 ? desc.substring(0, 20) + "..." : desc;
      }
    }
  },
  mounted() {
    this.keywords = this.$route.params.search_key;
    this.form = this.$route.params.form;
  }
}
</script>