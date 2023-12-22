<template>
  <el-timeline>
    <el-timeline-item
      v-for="(item, index) in arr2"
      :timestamp="displayTime(item.date)"
      placement="top"
    >
      <el-collapse v-model="activeID" accordion>
        <el-collapse-item :name="index">
          <template #title>
            <div class="header">
              <span style="font-size: 18px; font-weight: bold">{{item.title}}</span>
              <div style="margin-left: auto">
                <icon-edit :size="20" @click.stop="handleEdit(item)"/>
                <icon-delete :size="20" @click.stop="handleDelete(item)"/>
              </div>
            </div>
          </template>
          <div style="margin: 5px; border-radius: 10px; box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;">
            <md-preview :text="item.content"/>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-timeline-item>
  </el-timeline>
</template>

<script lang="ts">
import {
  Edit as IconEdit,
  Delete as IconDelete,
} from "@icon-park/vue-next";
import announceForm from "@/components/announce/announceForm.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";
export default {
  name: "announcement",
  components: {MdPreview, announceForm, IconEdit, IconDelete},
  data() {
    return {
      arr2:[
          {title:'gaosj', date: new Date(), content:'hello'},
          {title:'bianyc', date: new Date(), content:'good'},
          {title:'chengqj', date: new Date(), content:'great'}
      ],
      text: '',
      activeID: 0,
    }
  },
  methods: {
    displayTime(date: Date) {
      return date.toLocaleString().replaceAll('/', '-')
    },
    submit() {

    },
    handleEdit(item) {

    },
    handleDelete(item) {

    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>