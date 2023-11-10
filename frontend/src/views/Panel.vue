<template>
    <div class="whole">
        <div class="title">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        </div>
        <el-form :model="form" class="form" label-width="200px">
            <el-form-item label="修改仓库配置：">
                <el-button @click="modify_deployment_config">修改部署配置</el-button>
                <el-button @click="notify_board_switch">上传配置文件</el-button>
            </el-form-item>
            <el-form-item label="添加新仓库：">
                <el-select v-model="repo_form.dir" placeholder="放哪个文件夹？">
                    <el-option
                        v-for="dir in dirs"
                        :key="dir"
                        :label="dir"
                        :value="dir"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="仓库URL:">
                <el-input placeholder="只要立哥有权限，你随便放"></el-input>
            </el-form-item>
            <el-form-item label="仓库分支：">
                <el-input placeholder="手动输入更健康"></el-input>
            </el-form-item>
            <el-form-item label="确认添加：">
                <el-button @click="request_add_repo">有这闲工夫瞎点，还不如自己改配置</el-button>
            </el-form-item>
            <el-form-item label="高亮分支：">
                <el-select v-model="form.region" placeholder="右侧高亮选中分支">
                </el-select>
            </el-form-item>
            <el-form-item label="修改定时任务时间：">

            </el-form-item>
            <el-form-item label="立刻更新：">
                <el-button @click="request_update_now">立刻更新</el-button>
            </el-form-item>
            <el-form-item label="我有话想说：">
                <el-input placeholder="说吧，一个字五块钱"></el-input>
            </el-form-item>
            <el-button @click="request_leave_message">伟大的先知，请聆听我的祈祷</el-button>
        </el-form>
    </div>
</template>

<script lang="ts" setup>
import { emitChangeFn } from 'element-plus';
import { reactive, ref, onMounted, getCurrentInstance } from 'vue'
import { io } from 'socket.io-client'
import { result } from 'lodash';

const socket = ref(null)
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

// Establish websocket connection
function connect() {
    socket.value = io('http://localhost:9926')
    socket.value.on("connect", ()=>{
        console.log("CONNECT successfully!")
    })
}

/**
 * Modify deployment configuration
 */
function modify_deployment_config() {
    console.log("Modify deployment configuration wanted!")
    if (socket.value == null){
        console.log("Failed to connect to socket")
    }
    else {
        socket.value.emit('modify_deployment_config', {})
        console.log("I did it")
        socket.value.once("shutup", (data) => {
            console.log("I received: ", data)
        })
    }
}

const parent_emit = defineEmits(["parent_callback"]);

const notify_board_switch = () => {
    parent_emit("parent_callback", "Hello, I'm panel")
}

/**
 * Add a new repo
 */

// select target dir
const dirs = ref([])
const repo_form = ref({
    dir: '',
    url: '',
    branch: 'develop'
})

function request_dirs() {
    dirs.value = ["ABC", "EFH"]
}

// request to add
function request_add_repo() {
    console.log("Ok ok, I'll request to add a repo")
    socket.value.emit("add_repo", JSON.parse(JSON.stringify(repo_form.value)))
    socket.value.once("add_repo_ret", (ret) => {
        const parsed_res = JSON.parse(JSON.stringify(ret))
        console.log("Add result is: ", parsed_res.ret)
    })
}

/**
 * Update immediately
 */
function request_update_now() {
    console.log("request to update now")
    socket.value.emit("update_now")
    socket.value.once("update_now_ret", (ret)=>{
        console.log("The update result: ", ret)
    })
}

/**
 * Leave a message to dear me
 */
const pray_words = ref("Allez tout droit mes amis")
function request_leave_message() {
    console.log("request to leave a message")
    socket.value.emit("leave_message", pray_words.value)
}

const onSubmit = () => {
    console.log('submit!')
}

onMounted(()=>{
    connect()
    request_dirs()
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