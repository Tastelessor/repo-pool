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
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
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
