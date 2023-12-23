<template>
    <!-- Your existing template code -->
  </template>
  
  <script setup lang="ts">
  import { ref, defineProps, defineEmits, withDefaults } from 'vue';
  import { ElMessage } from 'element-plus';
  
  interface Student {
    id: number;
    name: string;
    identity: string;
  }
  
  interface UserInfo {
    personId: string;
    username: string;
    identity: string;
  }
  
  interface ChangeInfo {
    identity: string;
  }
  
  const emits = defineEmits();
  
  const props = withDefaults(defineProps(['item']), {
    students: ref<Array<Student>>([
      { id: 1, name: 'gaosj', identity: '老师' },
      { id: 2, name: 'byc', identity: '学生' },
    ]),
  });
  
  const courseInfoVisible = ref(false);
  const createVisible = ref(false);
  const changeVisible = ref(false);
  const editFormRef = ref<any>([]); // Change 'any' to the actual form type if available
  const createUserInfo = ref<UserInfo>({
    personId: '',
    username: '',
    identity: '',
  });
  const changeInfo = ref<ChangeInfo>({
    identity: '',
  });
  
  const submitCreate = async (formEl: any) => {
    if (!formEl) return;
    await formEl.validate(async (valid: boolean, fields: any) => {
      if (valid) {
        // Handle form submission logic here
        // Example: await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade);
        // ElMessage.success('修改成功！');
        // this.resetForm();
        // this.editVisible = false;
      } else {
        ElMessage.warning('错误提交！');
      }
    });
    createVisible.value = false;
  };
  
  const submitChange = async (editFormRef: any) => {
    if (!editFormRef) return;
    await editFormRef.validate(async (valid: boolean, fields: any) => {
      if (valid) {
        // Handle form submission logic here
        // Example: await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade);
        // ElMessage.success('修改成功！');
        // this.resetForm();
        console.log('id identity ', object.value.id, editFormRef.identity);
        // change_user_identity_api(object.id,formEl.identity)
      } else {
        ElMessage.warning('错误提交！');
      }
    });
    changeVisible.value = false;
  };
  
  const deleteStudent = () => {
    // Handle delete student logic here
    props.students.value = []; // TODO: delete_student_api(courseid, student.id)
  };
  
  const changeStudent = (index: number, row: Student) => {
    // Handle change student logic here
    changeVisible.value = true;
    console.log('type ', typeof props.students);
    console.log('index row ', index, row.id);
    props.students.value = [{ id: 3, name: 'cqj', identity: '老师' }]; // TODO: add_student_api(courseid, student.id)
    object.value = row;
  };
  
  const cancelDialog = () => {
    courseInfoVisible.value = false;
  };
  
  const confirmDialog = () => {
    courseInfoVisible.value = false;
  };
  
  </script>
  
  <style scoped>
    /* Your existing styles */
  </style>