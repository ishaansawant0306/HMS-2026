<template>
  <div class="register-page">

    <!-- NAV -->
    <nav class="top-nav">
      <div class="nav-inner">
        <span class="logo">MediZentrum</span>
        <ul class="nav-links">
          <li><a href="#">About Us</a></li>
          <li><a href="#">Specialities</a></li>
          <li><a href="#">Services</a></li>
          <li><a href="#">Patient's Care</a></li>
          <li><a href="#">Contact us</a></li>
        </ul>
      </div>
    </nav>

    <!-- MAIN -->
    <main class="register-main">
      <div class="register-card">

        <!-- LEFT PANEL -->
        <div class="panel-left">
          <h2>Patient Registration</h2>
          <ul class="feature-list">
            <li>
              <span class="check-icon">
                <svg viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2.5">
                  <polyline points="2,6 5,9 10,3"/>
                </svg>
              </span>
              Anesthesiology
            </li>
            <li>
              <span class="check-icon">
                <svg viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2.5">
                  <polyline points="2,6 5,9 10,3"/>
                </svg>
              </span>
              Audiology and speech therapy
            </li>
            <li>
              <span class="check-icon">
                <svg viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2.5">
                  <polyline points="2,6 5,9 10,3"/>
                </svg>
              </span>
              chest medicine
            </li>
            <li>
              <span class="check-icon">
                <svg viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2.5">
                  <polyline points="2,6 5,9 10,3"/>
                </svg>
              </span>
              Diabetology
            </li>
            <li>
              <span class="check-icon">
                <svg viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2.5">
                  <polyline points="2,6 5,9 10,3"/>
                </svg>
              </span>
              Colorectal surgery
            </li>
          </ul>
        </div>

        <!-- RIGHT PANEL -->
        <div class="panel-right">
          <h1>Sign Up</h1>

          <div v-if="error" class="error-alert">{{ error }}</div>
          <div v-if="success" class="success-alert">{{ success }}</div>

          <form @submit.prevent="handleRegister">

            <!-- First Name + Last Name -->
            <div class="form-row">
              <div class="form-group">
                <label for="firstName">First Name</label>
                <input
                  v-model="form.firstName"
                  type="text"
                  id="firstName"
                  placeholder="First Name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="lastName">Last Name</label>
                <input
                  v-model="form.lastName"
                  type="text"
                  id="lastName"
                  placeholder="Last Name"
                  required
                />
              </div>
            </div>

            <!-- Age -->
            <div class="form-group">
              <label for="age">Age</label>
              <input
                v-model="form.age"
                type="number"
                id="age"
                placeholder="Age"
                min="1"
                max="120"
                required
              />
            </div>

            <!-- Location -->
            <div class="form-group">
              <label for="location">Where are you from?</label>
              <input
                v-model="form.location"
                type="text"
                id="location"
                placeholder="City, Country"
                required
              />
            </div>

            <!-- Email -->
            <div class="form-group">
              <label for="email">Email or User Id</label>
              <input
                v-model="form.email"
                type="email"
                id="email"
                placeholder="Email or User Id"
                required
              />
              <span class="field-hint">Note - Email will be used as username</span>
            </div>

            <!-- Password -->
            <div class="form-group">
              <label for="password">Password</label>
              <div class="input-wrap">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  placeholder="Password"
                  required
                />
                <button type="button" class="show-btn" @click="showPassword = !showPassword">
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <div class="btn-register-wrap">
              <button type="submit" class="btn-register" :disabled="loading">
                {{ loading ? 'Registering…' : 'Register' }}
              </button>
            </div>
          </form>

          <div class="login-row">
            <small>
              Already have an account?
              <router-link to="/login">Login</router-link>
            </small>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'RegisterPage',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        age: '',
        location: '',
        email: '',
        password: ''
      },
      error: '',
      success: '',
      loading: false,
      showPassword: false
    }
  },
  methods: {
    async handleRegister() {
      this.error = ''
      this.success = ''
      this.loading = true

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/register/patient', {
          firstName: this.form.firstName,
          lastName: this.form.lastName,
          age: this.form.age,
          location: this.form.location,
          email: this.form.email,
          password: this.form.password
        })

        this.success = response.data.message || 'Registration successful! You can now log in.'
        setTimeout(() => {
          this.$router.push('/login')
        }, 1500)
      } catch (err) {
        this.error = err.response?.data?.message || err.response?.data?.error || err.message || 'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>


<style scoped>
/* ── PAGE ── */
.register-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #edf0f4;
  font-family: 'Inter', 'Helvetica Neue', sans-serif;
}

/* ── NAV ── */
.top-nav {
  background: #ffffff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 2rem;
  flex-shrink: 0;
}

.nav-inner {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 1.35rem;
  font-weight: 800;
  color: #1a6fd4;
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.75rem;
  margin-left: auto;
  list-style: none;
  padding: 0;
  margin-bottom: 0;
}

.nav-links a {
  font-size: 0.9rem;
  font-weight: 500;
  color: #1a1a2e;
  text-decoration: none;
  transition: color 0.18s;
}
.nav-links a:hover { color: #1a6fd4; }

.btn-demo {
  display: inline-flex;
  align-items: center;
  padding: 0.45rem 1.1rem;
  background: #1a6fd4 !important;
  color: #fff !important;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 9999px;
  text-decoration: none;
  transition: background 0.18s;
  white-space: nowrap;
}
.btn-demo:hover { background: #1558b0 !important; color: #fff !important; }

.nav-login {
  font-size: 0.9rem;
  font-weight: 500;
  color: #1a1a2e !important;
}

/* ── MAIN ── */
.register-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

/* ── CARD ── */
.register-card {
  display: flex;
  width: 100%;
  max-width: 820px;
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
  background: #ffffff;
}

/* ── LEFT PANEL ── */
.panel-left {
  background: #1a6fd4;
  padding: 2.5rem 2rem;
  flex: 0 0 40%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.4rem;
}

.panel-left h2 {
  font-size: 1.45rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.25;
}

.feature-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.93);
}

.check-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-icon svg {
  width: 11px;
  height: 11px;
}

/* ── RIGHT PANEL ── */
.panel-right {
  flex: 1;
  padding: 2.2rem 2.2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.panel-right h1 {
  font-size: 1.55rem;
  font-weight: 700;
  color: #1a1a2e;
  text-align: center;
  margin-bottom: 1.2rem;
  letter-spacing: -0.3px;
}

/* ── ALERTS ── */
.error-alert {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
  border-radius: 0.5rem;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  margin-bottom: 0.9rem;
}

.success-alert {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #86efac;
  border-radius: 0.5rem;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  margin-bottom: 0.9rem;
}

/* ── FORM ── */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.form-group {
  margin-bottom: 0.85rem;
}

.form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 0.3rem;
}

.form-group input {
  width: 100%;
  padding: 0.58rem;
  border: 1px solid #d0d5dd;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1a1a2e;
  transition: border-color 0.18s;
}

.form-group input:focus {
  outline: none;
  border-color: #1a6fd4;
  box-shadow: 0 0 0 3px rgba(26, 111, 212, 0.1);
}

.field-hint {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.3rem;
}

/* ── INPUT WRAP ── */
.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrap input {
  padding-right: 2.5rem;
}

.show-btn {
  position: absolute;
  right: 0.6rem;
  background: none;
  border: none;
  color: #1a6fd4;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
  transition: color 0.18s;
}

.show-btn:hover {
  color: #1558b0;
}

.show-btn:active {
  color: #0f3d7a;
}

/* ── BUTTON ── */
.btn-register-wrap {
  display: flex;
  justify-content: center;
  margin-top: 1.2rem;
}

.btn-register {
  width: 100%;
  padding: 0.65rem 1.5rem;
  background: #f9931e;
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
}

.btn-register:hover:not(:disabled) {
  background: #e68419;
}

.btn-register:active:not(:disabled) {
  background: #d47614;
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ── LOGIN ROW ── */
.login-row {
  text-align: center;
  margin-top: 0.8rem;
}

.login-row small {
  font-size: 0.8rem;
  color: #6b7280;
}

.login-row a {
  color: #1a6fd4;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.18s;
}

.login-row a:hover {
  color: #1558b0;
}
</style>