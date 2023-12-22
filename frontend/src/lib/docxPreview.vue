<template>
  <vue-office-docx :src="docx" @rendered="rendered"/>
</template>

<script>
import VueOfficeDocx from '@vue-office/docx'
export default {
  name: "docxPreview",
  components: {VueOfficeDocx},
  props: {
    docx: {
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