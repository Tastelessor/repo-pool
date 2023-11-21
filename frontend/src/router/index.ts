import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../App.vue'
import InfoView from '../views/Info.vue'
import PanelView from '../views/Panel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/info',
      name: 'info',
      component: InfoView
    },
    {
      path: '/panel',
      name: 'panel',
      component: PanelView
    }
  ]
})

export default router
