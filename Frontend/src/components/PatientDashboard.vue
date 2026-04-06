<template>
  <div class="patient-page">
    <nav class="top-nav">
      <div class="nav-inner">
        <span class="logo">MediZentrum</span>
        <ul class="nav-links">
          <li><a href="#">Products</a></li>
          <li><a href="#">Resources</a></li>
          <li><a href="#">Company</a></li>
          <li><a href="#" class="btn-demo">Book a Demo</a></li>
          <li><button class="nav-logout" @click="logout">Logout</button></li>
        </ul>
      </div>
    </nav>

    <main class="patient-main">
      <div class="patient-card">
        <div class="panel-left">
          <h2>Patient Dashboard</h2>
          <p>Welcome back, {{ patient.name || 'Patient' }}.</p>
          <p>Use this page to see your upcoming appointments and profile summary.</p>
        </div>

        <div class="panel-right">
          <h1>Welcome, {{ patient.name || 'Patient' }}</h1>
          <div v-if="error" class="error-alert">{{ error }}</div>
          <div v-if="loading" class="info-alert">Loading dashboard...</div>

          <div v-if="!loading && !error">
            <div class="stats-row">
              <div class="stat-box">
                <strong>{{ appointments.length }}</strong>
                <span>Upcoming appointments</span>
              </div>
              <div class="stat-box">
                <strong>{{ specializations.length }}</strong>
                <span>Available specializations</span>
              </div>
            </div>

            <section class="section-block">
              <h2>Profile</h2>
              <div class="profile-grid">
                <div><strong>Email</strong><p>{{ patient.email }}</p></div>
                <div><strong>Age</strong><p>{{ patient.age }}</p></div>
                <div><strong>Gender</strong><p>{{ patient.gender }}</p></div>
              </div>
            </section>

            <section class="section-block">
              <h2>Upcoming Appointments</h2>
              <div v-if="appointments.length === 0" class="empty-state">
                No upcoming appointments yet.
              </div>
              <ul v-else class="appointments-list">
                <li v-for="appointment in appointments" :key="appointment.id">
                  <strong>{{ appointment.doctor_name }}</strong>
                  <span>{{ appointment.specialization }}</span>
                  <span>{{ appointment.date }} · {{ appointment.time }}</span>
                  <span class="status">{{ appointment.status }}</span>
                </li>
              </ul>
            </section>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PatientDashboard',
  data() {
    return {
      patient: {},
      appointments: [],
      specializations: [],
      loading: false,
      error: ''
    }
  },
  mounted() {
    this.fetchDashboard()
  },
  methods: {
    async fetchDashboard() {
      this.error = ''
      this.loading = true

      const token = localStorage.getItem('token')
      if (!token) {
        return this.$router.push('/login')
      }

      try {
        const response = await axios.get('http://127.0.0.1:5000/api/patient/dashboard', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.patient = response.data.patient || {}
        this.appointments = response.data.upcoming_appointments || []
        this.specializations = response.data.specializations || []
      } catch (err) {
        this.error = err.response?.data?.message || err.response?.data?.error || 'Unable to load dashboard.'
        if (err.response?.status === 401 || err.response?.status === 403) {
          localStorage.removeItem('token')
          localStorage.removeItem('role')
          localStorage.removeItem('user')
          this.$router.push('/login')
        }
      } finally {
        this.loading = false
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.patient-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}
.patient-card {
  display: flex;
  width: 100%;
  max-width: 860px;
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
  background: #ffffff;
}
.panel-left {
  background: #1a6fd4;
  padding: 2.5rem 2rem;
  flex: 0 0 40%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  color: #ffffff;
}
.panel-left h2 {
  font-size: 1.45rem;
  font-weight: 700;
}
.panel-left p {
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(255,255,255,0.92);
}
.panel-right {
  flex: 1;
  padding: 2.5rem 2.2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.panel-right h1 {
  font-size: 1.55rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a2e;
}
.error-alert,
.info-alert {
  border-radius: 0.5rem;
  padding: 0.8rem 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.error-alert {
  background: #fee2e2;
  border: 1px solid #fca5a5;
  color: #b91c1c;
}
.info-alert {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
}
.stats-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.9rem;
  padding: 1rem;
}
.stat-box strong {
  display: block;
  font-size: 1.4rem;
  margin-bottom: 0.35rem;
}
.stat-box span {
  color: #475569;
}
.section-block {
  margin-bottom: 1.5rem;
}
.section-block h2 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}
.profile-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}
.profile-grid div {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.8rem;
  padding: 1rem;
}
.profile-grid strong {
  display: block;
  margin-bottom: 0.35rem;
  color: #334155;
}
.profile-grid p {
  color: #475569;
  margin: 0;
}
.appointments-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.75rem;
}
.appointments-list li {
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  display: grid;
  gap: 0.25rem;
}
.appointments-list strong {
  color: #0f172a;
}
.appointments-list span {
  color: #475569;
  font-size: 0.9rem;
}
.status {
  color: #1a6fd4;
  font-weight: 600;
}
.empty-state {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.85rem;
  color: #475569;
}
@media (max-width: 768px) {
  .patient-card { flex-direction: column; }
  .panel-left, .panel-right { padding: 1.5rem; }
  .profile-grid { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: 1fr; }
}
</style>