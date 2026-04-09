<template>
  <div class="login-page">

    <!-- nav -->
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

    <!-- main -->
    <main class="login-main">
      <div class="login-card">

        <!-- left side -->
        <div class="panel-left">
          <h2>Patient Login</h2>
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

        <!-- right side -->
        <div class="panel-right">
          <h1>Sign In</h1>

          <div v-if="error" class="error-alert">{{ error }}</div>

          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="email">Email or Username</label>
              <input
                v-model="form.email"
                type="text"
                id="email"
                placeholder="Email or Username"
                required
              />
            </div>

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
              <div class="forgot-row">
                <a href="#">Forgot Password?</a>
              </div>
            </div>

            <button type="submit" class="btn-login">Login</button>
          </form>

          <div class="register-row">
            <small>
              Patient?
              <router-link to="/register">Register here</router-link>
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
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      error: '',
      showPassword: false
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
          localStorage.setItem('adminId', '1')
          this.$router.push('/admin')
        } else if (data.user.role === 'doctor') {
          localStorage.setItem('doctorId', data.user.id)
          this.$router.push('/doctor')
        } else if (data.user.role === 'patient') {
          this.$router.push('/patient')
        } else {
          this.error = 'Unknown role received from server'
        }
      } catch (err) {
        this.error = err.response?.data?.message || err.response?.data?.error || err.message || 'Login failed'
      }
    }
  }
}
</script>


<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #edf0f4;
  font-family: 'Inter', 'Helvetica Neue', sans-serif;
}


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


.login-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}


.login-card {
  display: flex;
  width: 100%;
  max-width: 760px;
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
  background: #ffffff;
}


.panel-left {
  background: #1a6fd4;
  padding: 2.5rem 2rem;
  flex: 0 0 42%;
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


.panel-right {
  flex: 1;
  padding: 2.5rem 2.2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.panel-right h1 {
  font-size: 1.55rem;
  font-weight: 700;
  color: #1a1a2e;
  text-align: center;
  margin-bottom: 1.4rem;
  letter-spacing: -0.3px;
}


.error-alert {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
  border-radius: 0.5rem;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}


.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 0.35rem;
}

.input-wrap {
  position: relative;
}

.form-group input {
  width: 100%;
  padding: 0.62rem 0.9rem;
  background: #f3f6fb;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #1a1a2e;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s;
  font-family: inherit;
}
.form-group input::placeholder { color: #b0b8c4; }
.form-group input:focus {
  border-color: #1a6fd4;
  box-shadow: 0 0 0 3px rgba(26, 111, 212, 0.13);
}

.show-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.8rem;
  font-weight: 600;
  color: #1a6fd4;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  font-family: inherit;
}
.show-btn:hover { color: #1558b0; }

.forgot-row {
  text-align: right;
  margin-top: 0.35rem;
}
.forgot-row a {
  font-size: 0.78rem;
  font-weight: 500;
  color: #f59c1a;
  text-decoration: none;
}
.forgot-row a:hover { text-decoration: underline; }

.btn-login {
  display: block;
  width: 100%;
  padding: 0.72rem;
  margin-top: 1.2rem;
  background: #f59c1a;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 700;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: background 0.18s, transform 0.1s;
  letter-spacing: 0.2px;
  font-family: inherit;
}
.btn-login:hover  { background: #e08800; }
.btn-login:active { transform: scale(0.985); }


.register-row {
  text-align: center;
  margin-top: 1rem;
  color: #6b7280;
  font-size: 0.85rem;
}
.register-row a {
  color: #1a6fd4;
  text-decoration: none;
  font-weight: 500;
}
.register-row a:hover { text-decoration: underline; }


@media (max-width: 600px) {
  .login-card { flex-direction: column; }
  .panel-left { flex: none; padding: 1.75rem 1.5rem; }
  .panel-right { padding: 1.75rem 1.5rem; }
  .nav-links li:nth-child(1),
  .nav-links li:nth-child(2) { display: none; }
}
</style>