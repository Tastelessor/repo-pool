<template>
    <div class="whole">
        <div class="title">
            <el-form class="form" label-width="120px" style="margin-top: 5px;">
            <el-form-item label="选主题吧，老登:">
                <el-select v-model="current_theme" placeholder="选主题喽" @change="change_theme">
                    <el-option
                        v-for="theme in ace_available_themes"
                        :key="theme"
                        :label="theme"
                        :value="theme"    
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="保存配置:">
                <el-button @click="request_store_repo_cfg">老师我写完了</el-button>
            </el-form-item>
            <el-form-item label="恢复配置:">
                <el-button @click="request_load_repo_cfg">老板给我换一张纸</el-button>
            </el-form-item>
            <el-form-item label="请点击全屏:">
                <el-button>没想到吧，随便你怎么滑动，编辑器就是不变小</el-button>
            </el-form-item>
        </el-form>
        </div>
        <VAceEditor class="editor"
            :theme="current_theme"
            lang="json"
            v-model:value="repo_cfg_json"
        ></VAceEditor>
    </div>
</template>
  
<script setup lang="ts">
import { ElNotification } from 'element-plus'
import { VAceEditor } from 'vue3-ace-editor'
import 'ace-builds/src-noconflict/theme-chrome'
import 'ace-builds/src-noconflict/theme-github'
import 'ace-builds/src-noconflict/mode-json'
import { ace_available_themes } from '@/scripts/themes'
import { ref, onMounted, inject } from 'vue'
import { global_socket } from '@/main'

const socket = inject("SOCKET", global_socket)

/**
 * change theme
 */
const current_theme = ref("eclipse")
function load_theme() {
    const stored_theme = sessionStorage.getItem('ace_editor_theme')
    if (stored_theme != null) {
        current_theme.value = stored_theme
    }
}
function change_theme() {
    console.log("Current theme: ", current_theme.value)
    sessionStorage.setItem("ace_editor_theme", current_theme.value)
}

/**
 * load & store file
 */
const repo_cfg_json = ref("Failed to load the configuration file :D")

// load repo cfg
function request_load_repo_cfg() {
    console.log("request load repo cfg")
    socket.value.emit("request_load_repo_cfg")
    socket.value.once("request_load_repo_cfg_ret", (ret:JSON) => {
        repo_cfg_json.value = JSON.parse(JSON.stringify(ret))
    })
    console.log("Received repo_cfg: ", repo_cfg_json.value)
    sessionStorage.setItem("repo_cfg_json", repo_cfg_json.value)
}

// store repo cfg
function request_store_repo_cfg() {
    console.log("request store repo cfg: ", repo_cfg_json.value)
    socket.value.emit("request_store_repo_cfg", repo_cfg_json.value)
    socket.value.once("request_store_repo_cfg_ret", (ret:string) => {
        if (ret) {
            console.log("Successfully stored repo cfg!")
            ElNotification({
                title: '来自伟大的先知',
                message: '你的改动老师收到啦',
                type: 'success',
            })
            return
        } else {
            ElNotification({
                title: '来自伟大的先知',
                message: '写的什么玩意儿，不收',
                type: 'error',
            })
        }
        console.log("Failed to store repo cfg")
    })
    sessionStorage.setItem("repo_cfg_json", repo_cfg_json.value)
}

onMounted(()=>{
    load_theme()
    request_load_repo_cfg()
})
</script>

<style scoped>
@import url('@/styles/horizontal-list.css');
@import url('@/styles/el-form.css');
@import url('@/styles/el-button.css');
@import url('@/styles/ace-editor.css');
</style>
  