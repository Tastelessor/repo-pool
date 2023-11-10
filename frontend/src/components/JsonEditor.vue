<template>
    <div class="whole">
        <div class="title">
            <el-form :model="form" class="form" label-width="120px" style="margin-top: 5px;">
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
                <el-button>老师我写完了</el-button>
            </el-form-item>
            <el-form-item label="恢复配置:">
                <el-button>老板给我换一张纸</el-button>
            </el-form-item>
            <el-form-item label="请点击全屏:">
                <el-button>没想到吧，随便你怎么滑动，编辑器就是不变小</el-button>
            </el-form-item>
        </el-form>
        </div>
        <VAceEditor class="editor"
            :theme="current_theme"
            v-model="jsonContent"
            lang="json"
            value="asd"
        />
    </div>
</template>
  
<script setup lang="ts">
import { VAceEditor } from 'vue3-ace-editor'
import 'ace-builds/src-noconflict/theme-chrome'
import 'ace-builds/src-noconflict/theme-github'
import 'ace-builds/src-noconflict/mode-json'
import { ace_available_themes } from '@/scripts/themes'
import { ref, onMounted } from 'vue'

/**
 * change theme
 */
const current_theme = ref("chrome")
function load_theme() {
    const stored_theme = sessionStorage.getItem('ace_editor_theme')
    if (stored_theme != null) {
        current_theme.value = stored_theme
    }
}
function change_theme() {
    console.log("Current theme: ", current_theme.value)
    sessionStorage.setItem('ace_editor_theme', current_theme.value)
}
onMounted(()=>{
    load_theme()
})
const jsonContent = ref('{"key": "value"}');
</script>

<style scoped>
@import url('@/styles/horizontal-list.css');
@import url('@/styles/el-form.css');
@import url('@/styles/el-button.css');
@import url('@/styles/ace-editor.css');
</style>
  