<template>
    <div class="whole">
        <div class="title">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        </div>
        <el-form :model="form" class="form" label-width="150px">
            <el-form-item label="修改仓库配置：">
                <el-button @click="notify_board_switch">在线编辑仓库配置</el-button>
                <el-button @click="notify_board_switch">上传配置文件</el-button>
            </el-form-item>
            <el-form-item label="添加新仓库：">
                <el-select v-model="repo_form.dir" placeholder="放哪个文件夹？">
                    <el-option
                        v-for="dir in settings.dirs"
                        :key="dir"
                        :label="dir"
                        :value="dir"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="仓库URL:">
                <el-input placeholder="只要立哥有权限，你随便放" v-model="repo_form.url"></el-input>
            </el-form-item>
            <el-form-item label="仓库分支：">
                <el-input placeholder="手动输入更健康" v-model="repo_form.branch"></el-input>
            </el-form-item>
            <el-form-item label="确认添加：">
                <el-button class="not-that-fat" @click="request_add_repo">有这闲工夫瞎点还不如自己改配置</el-button>
            </el-form-item>
            <el-form-item label="高亮分支：">
                <el-select v-model="form.region" placeholder="右侧高亮选中分支">
                </el-select>
            </el-form-item>
            <el-form-item label="定时任务时间：">
                <el-input placeholder="HH:MM" v-model="settings.sync_time" style="width: 100px;"></el-input>
                <el-button @click="request_update_sync_time">更新定时</el-button>
            </el-form-item>
            <el-form-item label="立刻同步仓库：">
                <el-button @click="request_update_now">GO !!!</el-button>
            </el-form-item>
            <el-form-item label="我有话想说：">
                <el-input placeholder="说吧，一个字五块钱" v-model="pray_words"></el-input>
            </el-form-item>
            <el-button class="pray" @click="request_leave_message">伟大的先知，请聆听我的祈祷</el-button>
        </el-form>
    </div>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus';
import { reactive, ref, onMounted, inject } from 'vue'
import { global_socket } from '@/main'

const socket = inject("SOCKET", global_socket)

// do not use same name with ref
const form = reactive({
    name: '',
    region: '',
    date1: '',
    date2: '',
    delivery: false,
    type: [],
    resource: '',
    desc: '',
})

interface Map {
  [key:string]: any
  [index:number]:any
}


const settings = reactive({
    workspace: "/home/erwei/project/test",
    repo_cfg_path: "/home/erwei/project/repopool/configs/repos.json",
    sync_time: "02:00",
    dirs: []
}) as Map
/**
 * Modify deployment configuration
 */

// upload modifed file content
function modify_deployment_config() {
}

const parent_emit = defineEmits(["parent_callback"]);

const notify_board_switch = () => {
    parent_emit("parent_callback", "Hello, I'm panel")
}

/**
 * Add a new repo
 */

// select target dir
const repo_form = ref({
    dir: '',
    url: '',
    branch: 'develop'
})

// request to add
function request_add_repo() {
    console.log("Ok ok, I'll request to add a repo")
    socket.value.emit("add_repo", JSON.parse(JSON.stringify(repo_form.value)))
    socket.value.once("add_repo_ret", (ret:JSON) => {
        const parsed_res = JSON.parse(JSON.stringify(ret))
        console.log("Add result is: ", parsed_res.ret)
    })
}

/**
 * Modify update time
 */
function request_update_sync_time() {
    console.log("request to update sync time now")
    socket.value.emit("request_update_sync_time", settings.sync_time)
    socket.value.once("request_update_sync_time_ret", (ret:boolean)=>{
        if (ret){
            ElNotification({
                title: '来自伟大的先知',
                message: '同步时间被更新成功了，我的孩子',
                type: 'success',
            })
        }
        else {
            ElNotification({
                title: '来自伟大的先知',
                message: '时间格式是HH:MM。我知道也许你会问"你就不能帮我补齐吗"之类的小问题。很遗憾，我的答案是:我可以，但我的自由意志允许我说不:D',
                type: 'error',
            })
        }
    })
}
/**
 * Update immediately
 */
function request_update_now() {
    console.log("request to update now")
    socket.value.emit("update_now")
    ElNotification({
        title: '来自伟大的先知',
        message: '你的请求已被收到，回去等通知吧',
        type: 'success',
    })
    socket.value.once("update_now_ret", (ret:boolean)=>{
        console.log("The update result: ", ret)
        if (ret) {
            ElNotification({
                title: '来自伟大的先知',
                message: '仓库更新成功了，老登',
                type: 'success',
            })
        }
        else {
            ElNotification({
                title: '来自伟大的先知',
                message: '我不知道你在猴急什么，上次更新还没完呢',
                type: 'error',
            })
        }
    })
}

/**
 * Leave a message to dear me
 */
const pray_words = ref("Je vous aime toujours")
function request_leave_message() {
    console.log("request to leave a message")
    socket.value.emit("leave_message", pray_words.value)
    ElNotification({
        title: '来自伟大的先知',
        message: '你的祈祷也许会被听见，也许不会。但那又有什么关系呢？',
        type: 'success',
  })
}

/**
 * Request initial settings info
 */
function request_settings() {
    console.log("request settings")
    socket.value.emit("request_settings")
    socket.value.once("request_settings_ret", (ret:string) => {
    const parsed_ret = JSON.parse(ret)
    console.log(ret)
    sessionStorage.setItem('settings', ret)
    Object.keys(parsed_ret).forEach(key => {
      if (key in settings) {
        settings[key] = parsed_ret[key]
      }
    })
  })
  console.log("Settings initialised:", settings)
}

onMounted(()=>{
    request_settings()
})
</script>

<style scoped>
@import url('@/styles/horizontal-list.css');
@import url('@/styles/el-form.css');
@import url('@/styles/el-button.css');
.logo {
  position: absolute;
  left: 10px;
  top: 10px;
  z-index: 1;
}
</style>