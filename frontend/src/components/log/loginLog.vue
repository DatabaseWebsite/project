<template>
  <el-container>
    <el-header style="overflow-y:scroll;overflow-x:hidden;height:110px">
      <el-form :inline="true" :model="searchInfo" label-width="60px" size="small">
        <el-form-item label="姓名" style="width: 180px;">
          <el-input v-model="searchInfo.username" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="登录ip" style="width: 180px;">
          <el-input v-model="searchInfo.ip" placeholder="请输入登录ip"></el-input>
        </el-form-item>
        <el-form-item label="时间" style="width: 500px">
          <el-date-picker
            v-model="searchInfo.duration"
            type="datetimerange"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            date-format="YYYY/MM/DD ddd"
            time-format="A hh:mm:ss"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitSearchForm"> <el-icon><Search/></el-icon>查询 </el-button>
          <el-button type="info" @click="resetSearchForm"> <el-icon><Refresh/></el-icon>重置 </el-button>
        </el-form-item>
      </el-form>
      <div style="font-size:12px; color: dimgray">
        tips: 每月1号凌晨0点会自动清除上个月的日志
      </div>
    </el-header>
    <el-main>
      <el-table :data="tableData" border>
        <el-table-column prop="id" label="序号" width="70"/>
        <el-table-column prop="username" label="登录用户名" min-width="140"/>
        <el-table-column prop="ip" label="登录ip" min-width="160"/>
        <el-table-column prop="address" label="登陆地址" min-width="180"/>
        <el-table-column prop="browser" label="浏览器" min-width="180"/>
        <el-table-column fixed="right" prop="time" label="登录时间" min-width="180"/>
      </el-table>
      <div>
        <el-pagination layout="prev, pager, next" :page-count="totalPage" :current-page="curPage" page-size=10 @current-change="changePage" style="margin: 10px;"/>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import {get_login_log_api, search_login_log_api} from "@/api/api.ts";
import {ElMessage} from "element-plus";
import {Search, Refresh} from "@element-plus/icons-vue";

export default {
  name: "loginLog",
  components: {Search, Refresh},
  data() {
    return {
      searchInfo: {
        username: '',
        ip: '',
        duration: [],
      },
      tableData: [
        { // loginLog
          id: 1,
          username: 'admin',
          ip: '218.192.13.231',
          address: '北京市海淀区',
          time: '2021-01-01 14:00:00',
          browser: 'Chrome 119.0.0'
        }, {
          id: 2,
          username: '程钱佳',
          ip: '218.29.221.16',
          address: '北京市海淀区',
          time: '2021-01-01 14:00:00',
          browser: 'Chrome 119.0.0'
        }
      ],
      curPage: 1,
      totalPage: 1,
      isSearching: false,
    }
  },
  methods: {
    getRequest() {
      const result = {}
      const query = window.location.href.split('?')[1]
      if (query) {
        const queryArr = query.split('&')
        queryArr.forEach(item => {
          const value = decodeURIComponent(item.split('=')[1])
          console.log(value)
          const key = item.split('=')[0]
          const results = result as any
          results[key] = value
        })
      }
      if (result['ip'] != null) {
        this.isSearching = true
        this.searchInfo.ip = result['ip']
        this.searchInfo.username = result['username']
        this.searchInfo.duration[0] = this.stringToDate(result['startTime'])
        this.searchInfo.duration[1] = this.stringToDate(result['endTime'])
        this.curPage = result['page']
      } else {
        this.isSearching = false
        this.curPage = result['page']
      }
    },
    dateToString(date: Date) {
      let year = date.getFullYear()
      let month: string | number = date.getMonth() + 1
      let day: string | number = date.getDate()
      let hour: string | number = date.getHours()
      let minute: string | number = date.getMinutes()
      let second: string | number = date.getSeconds()
      month = month < 10 ? ('0' + month) : month
      day = day < 10 ? ('0' + day) : day
      hour = hour < 10 ? ('0' + hour) : hour
      minute = minute < 10 ? ('0' + minute) : minute
      second = second < 10 ? ('0' + second) : second
      return year + '-' + month + '-' + day + 'A' + hour + ':' + minute + ':' + second
    },
    stringToDate(str: string) {
      let [datePart, timePart] = str.split('A');
      let [year, month, day] = datePart.split('-').map(Number);
      let [hour, minute, second] = timePart.split(':').map(Number);

      // 创建日期对象并指定时区为中国上海
      return new Date(Date.UTC(year, month - 1, day, hour, minute, second) - 8 * 60 * 60 * 1000);
    },
    async queryLog() {
      if (this.isSearching) {
        window.location.href = `/#/loginLog?username=${this.searchInfo.username}&ip=${this.searchInfo.ip}&startTime=${this.dateToString(this.searchInfo.duration[0])}&endTime=${this.dateToString(this.searchInfo.duration[1])}&page=${this.curPage}`
        await search_login_log_api(this.searchInfo.username, this.searchInfo.ip, this.dateToString(this.searchInfo.duration[0]), this.dateToString(this.searchInfo.duration[1]), this.curPage).then(res => {
          this.tableData = res.data['result']
          this.totalPage = res.data['total_page']
        })
      } else {
        const page = this.curPage || 1
        window.location.href = `/#/loginLog?page=${page}`
        await get_login_log_api(page).then(res => {
          this.tableData = res.data['result']
          this.totalPage = res.data['total_page']
        })
      }
    },
    async submitSearchForm() {
      if (this.searchInfo.username=='' && this.searchInfo.ip=='' && this.searchInfo.duration==[]) {
        ElMessage.warning({
          message: '查询条件不能全为空',
          type: 'warning'
        })
        return
      }
      console.log(this.searchInfo.duration)
      this.curPage = 1
      this.isSearching = true
      await this.queryLog()
    },
    resetSearchForm() {
      this.isSearching = false
      this.searchInfo = {
        username: '',
        ip: '',
        duration: [],
      }
      this.curPage = 1
      this.queryLog()

    },
    async changePage(currentPage) {
      this.curPage = currentPage
      await this.queryLog()
    },
  },
  mounted() {
    this.getRequest()
    this.queryLog()
  }
}
</script>

<style scoped>

</style>