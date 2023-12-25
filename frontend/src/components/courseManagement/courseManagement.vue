  <template>  
    <el-container>
      <el-header style="text-align: right;">
        <el-button  link type="primary" @click="dialogVisible = true">
          添加课程
        </el-button>
      </el-header>
      <el-main>
        <div v-for="(item, index) in courseInfo">
          <div class="item">
            <div class="left-section">
              <div class="id">{{ index }}</div>
              <div class="name-time">
                <p class="name">{{ item.name }}</p>
                <p class="upload-time">{{ item.duration }}</p>
                <p class="upload-time">{{ item.description }}</p>
              </div>
            </div>
            <div class="right-section">
              <el-button link type="primary" @click="showCourseInfo(item.course_id)">详细信息</el-button>
            </div>
          </div>
          <el-divider style="margin: 0; padding: 0"/>
        </div>
      </el-main>
    </el-container>  
    <el-dialog  
      v-model="dialogVisible"
      title="添加课程"
      width="600px">
      <el-form  ref="courseRef" :model="course" :rules="courseRules" label-width="80px">
        <el-form-item label="课程名" prop="name" style="width: 500px">
          <el-input v-model="course.name" placeholder="请输入课程名"></el-input>
        </el-form-item>
        <el-form-item label="开课时间" style="width: 500px" prop="duration">
          <el-date-picker
            v-model="course.duration"
            type="datetimerange"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            date-format="YYYY/MM/DD ddd"
            time-format="A hh:mm:ss"
          />
        </el-form-item>
        <el-form-item label="课程介绍" style="width: 500px" prop="description">
          <el-input v-model="course.description" placeholder="请输入课程介绍"></el-input>
        </el-form-item>
      </el-form>
        <template #footer>  
          <span class="dialog-footer">  
            <el-button type="primary" @click="submitCreate(courseRef)">  确认添加  </el-button>
          </span>  
        </template>  
    </el-dialog>
  </template>  
    
<script lang="ts">
import {create_course_api, all_course_info_api, get_course_list_api} from "@/api/api.ts";
import courseForm from "@/components/courseManagement/courseDetail.vue";
import {onMounted, reactive, ref} from "vue";
import {FormInstance, FormRules} from "element-plus";
import {useRouter} from "vue-router";
import useAuthStore from "@/store/user.ts";
interface Course {
  name: string,
  duration: Date[],
  description: string
}
export default {
  name: "courseManagement",
  components: { courseForm },
  setup() {
    const dialogVisible = ref(false)
    const courseInfo = ref([])
    const course = reactive<Course>({
      name: '',
      duration: [],
      description: '',
    })
    const courseRef = ref<FormInstance>()
    const router = useRouter()
    const user = useAuthStore().getUser
    const submitCreate = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        if (valid) {
          // 调用api
          await create_course_api(course.name,course.description,course.duration[0].toISOString(),course.duration[1].toISOString());
          console.log("success addCourse", course.name,course.description,course.duration[0],course.duration[1]);
          await getCoursesInfo();
        } else {
          console.log('错误提交！！')
        }
      })
    }
    const getCoursesInfo = async () => {
      await get_course_list_api().then(res => {
        courseInfo.value = res.data.result

      })
    }
    const showCourseInfo = (id) => {
      router.push({path: `/courseManagement/course`, query:{id: id} })
    }
    onMounted(() => {
      if (user['identity'] === 'TEACHER' || user['identity'] === 'ASSISTANT') {
        router.push({path: `/courseManagement/course`, query:{id: user['course_id']} })
      }
      getCoursesInfo()
    })
    const courseRules = reactive<FormRules<Course>>({
      name: [
        {required: true, message: '请输入课程名', trigger: 'blur'},
      ],
      duration: [
        {required: true, message: '请选择开课时间', trigger: 'change'},
        { type: 'array', len: 2, message: '请选择开始和结束时间', trigger: 'change' },
      ],
      description: [
        {min: 0, max: 50, message: '长度不能超过50字', trigger: 'blur'}
      ]
    })
    return {
      dialogVisible,
      course,
      courseInfo,
      courseRules,
      courseRef,
      submitCreate,
      showCourseInfo
    }
  }
}
</script>
  
<style scoped>
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 0;
  box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;
}

.left-section {
  display: flex;
  align-items: center;
}

.id {
  font-family: "Microsoft YaHei",cursive;
  font-size: 30px;
  font-weight: bold;
  padding: 0;
  margin: 0 20px 0 20px;
}
.name {
  font-family: "Microsoft YaHei",cursive;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
  margin: 10px 0 0 0;
  text-align: left;
}
.upload-time {
  font-family: "Times New Roman", Times, serif;
  font-size: 14px;
  color: gray;
  padding: 0;
  margin: 0 0 10px 0;
  text-align: left;
}
.name-time {
  display: flex;
  flex-direction: column;
}

.right-section {
  display: flex;
  text-align: right;
  align-items: center;
}
</style>