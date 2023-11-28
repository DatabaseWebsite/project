import {reactive} from "vue";

interface EditRuleForm {
  id: number,
  personId: string,
  username: string,
  grade: string,
}

export const editUserInfo = reactive<EditRuleForm>({
  id: null,
  personId: '',
  username: '',
  grade: '',
})

export const editRules = reactive({
  personId: [
    {required: true, message: '请输入学号', trigger: 'blur'},
  ],
  username: [
    {required: true, message: '请输入姓名', trigger: 'blur'},
    {min: 2, max: 10, message: '姓名长度为2-10位', trigger: 'blur'}
  ],
  grade: [
    {required: true, message: '请输入年级', trigger: 'blur'},
    {min: 4, max: 4, message: '年级长度为4位', trigger: 'blur'}
  ]
})