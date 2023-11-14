import './assets/main.css'
import "element-plus/theme-chalk/src/index.scss"
import { createApp, ref } from 'vue'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'

// Import the ACE editor stylesheet
import 'ace-builds/src-noconflict/theme-chrome'
import 'ace-builds/src-noconflict/theme-github'
import 'ace-builds/src-noconflict/mode-json'

export const global_socket = ref(null)

const app = createApp(App)

app.use(router)
app.use(ElementPlus)

app.provide('SOCKET', global_socket)
app.mount('#app')
