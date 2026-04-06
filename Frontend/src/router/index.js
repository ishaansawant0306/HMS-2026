import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/LoginPage.vue'
import PatientRegister from '../components/RegisterPage.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import PatientDashboard from '../components/PatientDashboard.vue'
import DoctorDashboard from '../components/DoctorDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: PatientRegister
  },
  {
    path: '/patient',
    name: 'PatientDashboard',
    component: PatientDashboard,
    meta: { requiresAuth: true, role: 'patient' }
  },
  {
    path: '/doctor',
    name: 'DoctorDashboard',
    component: DoctorDashboard,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
    } else if (to.meta.role && to.meta.role !== role) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router