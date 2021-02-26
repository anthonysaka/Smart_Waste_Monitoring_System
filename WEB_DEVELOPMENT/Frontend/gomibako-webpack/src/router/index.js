import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '*',
    redirect:'/login'
  },
  {
    path: '/',
    redirect:'/login'
  },
  {
    path: '/login',
    name: 'Login',
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Login.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/detailbins',
    name: 'DetalBins',
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/DetailBin.vue'),
    meta: {
      requiresAuth: true
    },
    
  },
  {
    path: '/trucks',
    name: 'Truck',
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Truck.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/routing',
    name: 'Routes',
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Routing.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/globaladmin',
    name: 'AdminPanel',
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/GlobalAdmin.vue'),
    meta: {
      requiresAuth: true,
    }
  },
 
]



const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})



router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})


export default router
