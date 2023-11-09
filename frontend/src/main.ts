import './assets/main.css'
import "element-plus/theme-chalk/src/index.scss";
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.mount('#app')
