<template>
  <div class="container py-5" style="max-width: 500px;">
    <div class="card shadow-sm border-0">
      <div class="card-body p-4">
        <h2 class="mb-1 text-center">MediZentrum</h2>
        <p class="text-center text-muted mb-4">Care, appointments, and records in one place.</p>
        <h5 class="mb-3 text-center">Login</h5>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>

          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>

        <div class="text-center mt-3">
          <small>
            Patient?
            <router-link to="/register">Register here</router-link>
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
          email: this.form.email,
          password: this.form.password
        })

        const data = response.data

        localStorage.setItem('token', data.access_token)
        localStorage.setItem('role', data.user.role)
        localStorage.setItem('user', JSON.stringify(data.user))

        if (data.user.role === 'admin') {
          this.$router.push('/admin')
        } else if (data.user.role === 'doctor') {
          this.$router.push('/doctor')
        } else if (data.user.role === 'patient') {
          this.$router.push('/patient')
        } else {
          this.error = 'Unknown role received from server'
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
      }
    }
  }
}
</script>