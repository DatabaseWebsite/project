<template>
  <vue-office-excel :src="excel" @rendered="rendered"/>
</template>

<script lang="ts">
import VueOfficeExcel from '@vue-office/excel'
export default {
  name: "excelPreview",
  components: {VueOfficeExcel},
  props: {
    excel: {
      type: String,
      required: true
    }
  },
  methods: {
    rendered() {
      console.log('rendered')
    }
  }
}
</script>

<style scoped>

</style>