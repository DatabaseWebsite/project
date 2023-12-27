<template>
  <div @click="drawer=true" class="notification-icon-container">
    <el-badge :is-dot="unreadCounts['total'] > 0" style="margin-top: 10px">
     <icon-comments :size="30" style="padding: 0; margin-left: 15px; margin-right: 10px;"/>
    </el-badge>
    <el-drawer
      v-model="drawer"
      :with-header="false"
      direction="ttb">
      <el-container>
        <el-aside style="width: 150px; height: 300px">
          <el-menu @select="handleMenuSelect" default-active="1" style="margin: 0; padding: 0">
            <el-menu-item index="1">
              <el-badge :is-dot="unreadCounts['class'] > 0" style="margin-top: 10px">
                <icon-classroom size="20" style="margin-right: 5px"/>
              </el-badge>
              课程组通知
            </el-menu-item>
            <el-menu-item index="2">
              <el-badge :is-dot="unreadCounts['work'] > 0" style="margin-top: 10px">
                <icon-notebook size="20" style="margin-right: 5px"/>
              </el-badge>
              作业通知
            </el-menu-item>
            <el-menu-item index="3">
              <el-badge :is-dot="unreadCounts['discussion'] > 0" style="margin-top: 10px">
                <icon-topic size="20" style="margin-right: 5px"/>
              </el-badge>
              讨论区通知
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main style="padding-top: 0">
          <div v-for="(item, index) in data" :key="index" @click="open(item)">
            <el-badge :is-dot="!item['unread']" style="margin-top: 5px">
              <div style="font-weight: bold">{{ item.title }}</div>
            </el-badge>
            <div style="font-size: 12px; color: #909399">{{ displayTime(item.time) }}</div>
            <el-text style="font-family: '楷体','楷体_GB2312'; font-size: 15px" truncated>{{ item.content }}</el-text>
            <el-divider style="margin: 0; padding: 0"/>
          </div>
        </el-main>
      </el-container>
    </el-drawer>
  </div>
</template>

<script lang="ts">
import {h, onMounted, watch} from 'vue'
import {
  Comments as IconComments,
  Classroom as IconClassroom,
  Notebook as IconNotebook,
  Topic as IconTopic,
} from "@icon-park/vue-next";
import {ref} from "vue";
import {ElMessageBox} from "element-plus";
import {get_messages_api, get_unread_messages_count_api, read_message_by_id} from "@/api/api.ts";
export default {
  name: "message",
  components: { IconComments, IconClassroom, IconNotebook, IconTopic },
  setup() {
    const drawer = ref(false)
    const activeID = ref(1)
    const data = ref([{
      id: 1,
      title: "课程组通知",
      unread: false,
      time: new Date(),
      content: "课程组通知内容",
    }, {
      id: 2,
      title: "作业通知",
      time: new Date(),
      content: "作业通知内容",
    }, {
      id: 3,
      title: "讨论区通知",
      time: new Date(),
      content: "讨论区通知内容",
    }])
    const unreadCounts = ref([])
    const handleMenuSelect = async (index) => {
      let type = null
      switch (index) {
        case "1":
          type = 'CLASS';
          break
        case "2":
          type = 'WORK';
          break
        case "3":
          type = 'DISCUSSION';
          break
      }
      await get_messages_api(type).then((res) => {
        data.value = res.data.result
        data.value.forEach((item) => {
          item.time = new Date(item.time)
        })
      })
    }
    const displayTime = (time) => {
      return time.toLocaleDateString() + ' ' + time.toLocaleTimeString()
    }
    watch(drawer, async (newVal, oldVal) => {
      if (newVal) {
        console.log(newVal)
        await get_messages_api('CLASS').then((res) => {
          data.value = res.data.result
          console.log(data)
        })
      }
    })
    const open = async (item) => {
      await read_message_by_id(item.id).then((res) => {
        data.value.forEach((one) => {
          if (one.id === item.id) {
            one['unread'] = true
            unreadCounts.value[item.type.toLowerCase()] -= 1
            unreadCounts.value['total'] -= 1
          }
        })
      })
      await ElMessageBox({
        title: item.title,
        message: h('div', {style: 'font-family: \'楷体\',\'楷体_GB2312\'; font-size: 15px'}, [
          h('p', {style: 'font-size: 12px; color: #909399'}, displayTime(item.time)),
          h('p', null, item.content),
        ]),
        showCancelButton: false,
        showConfirmButton: false,
      })
    }
    onMounted(async () => {
      await get_unread_messages_count_api().then(res => {
        unreadCounts.value = res.data.result
        data.value.forEach((item) => {
          item.time = new Date(item.time)
        })
      })
    })
    return {
      drawer,
      activeID,
      data,
      handleMenuSelect,
      open,
      displayTime,
      unreadCounts,
    }
  }
}
</script>

<style scoped>
</style>