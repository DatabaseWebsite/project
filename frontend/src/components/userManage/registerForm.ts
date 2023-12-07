import {reactive} from "vue";
import {FormRules} from "element-plus";

interface RegisterRuleForm {
  personId: string,
  username: string,
  grade: string,
  course: string,
  identity: string,
}

export const registerUser = reactive<RegisterRuleForm>({
  personId: '',
  username: '',
  grade: '',
  course: '',
  identity: '',
})

export const registerRules = reactive<FormRules<RegisterRuleForm>>({
  personId: [
    {required: true, message: '请输入学号', trigger: 'blur'},
  ],
  username: [
    {required: true, message: '请输入姓名', trigger: 'blur'},
    {min: 2, max: 10, message: '姓名长度为2-10位', trigger: 'blur'}
  ],
  grade: [
    // {required: true, message: '请输入年级,如2021', trigger: 'blur'},
    {min: 4, max: 4, message: '年级长度为4位', trigger: 'blur'}
  ],
  course: [
    {required: true, message: '请选择课程', trigger: 'change'},
  ],
  identity: [
    {required: true, message: '请选择身份', trigger: 'change'},
  ]
})