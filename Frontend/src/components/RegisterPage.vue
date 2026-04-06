<template>
  <div class="container py-5" style="max-width: 500px;">
    <div class="card shadow-sm border-0">
      <div class="card-body p-4">

        <h2 class="mb-1 text-center">MediZentrum</h2>
        <p class="text-center text-muted mb-4">Care, appointments, and records in one place.</p>
        <h5 class="mb-3 text-center">Patient Registration</h5>

        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="form.username" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Contact Number</label>
            <input v-model="form.contact_number" type="tel" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Age</label>
            <input v-model.number="form.age" type="number" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Gender</label>
            <select v-model="form.gender" class="form-select" required>
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Height (cm)</label>
            <input v-model.number="form.height" type="number" step="0.1" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Weight (kg)</label>
            <input v-model.number="form.weight" type="number" step="0.1" class="form-control" required />
          </div>

          <button type="submit" class="btn btn-success w-100">Register</button>
        </form>

        <div class="text-center mt-3">
          <router-link to="/login">← Back to Login</router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PatientRegister',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        contact_number: '',
        age: null,
        gender: '',
        height: null,
        weight: null
      },
      error: '',
      successMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.error = ''
      this.successMessage = ''

      try {
        await axios.post('http://127.0.0.1:5000/api/auth/register', this.form)
        this.successMessage = 'Registration successful! Please login.'
        this.$router.push('/login')
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
      }
    }
  }
}
</script>