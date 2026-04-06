<template>
  <div class="doctor-page">
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

    <main class="doctor-main">
      <div class="doctor-card">
        <div class="panel-left">
          <h2>Doctor Dashboard</h2>
          <p>This dashboard is populated with hardcoded test doctor information.</p>
          <p>Use it to validate the doctor view and data layout.</p>
        </div>

        <div class="panel-right">
          <h1>{{ doctor.name }}</h1>
          <p class="doctor-meta">ID: {{ doctor.id }} · {{ doctor.specialization }} · {{ doctor.availability }}</p>

          <section class="section-block">
            <h2>Summary</h2>
            <div class="summary-grid">
              <div class="summary-card">
                <strong>{{ doctor.upcoming_appointments }}</strong>
                <span>Upcoming appointments</span>
              </div>
              <div class="summary-card">
                <strong>{{ doctor.patients_count }}</strong>
                <span>Assigned patients</span>
              </div>
              <div class="summary-card">
                <strong>{{ doctor.completed_appointments }}</strong>
                <span>Completed visits</span>
              </div>
            </div>
          </section>

          <section class="section-block">
            <h2>Upcoming Appointments</h2>
            <ul class="appointments-list">
              <li v-for="appt in appointments" :key="appt.id">
                <strong>{{ appt.patient_name }}</strong>
                <span>{{ appt.date }} · {{ appt.time }}</span>
                <span class="status">{{ appt.status }}</span>
              </li>
            </ul>
          </section>

          <section class="section-block">
            <h2>Recent Patients</h2>
            <div class="patient-list">
              <div v-for="patient in patients" :key="patient.id" class="patient-card">
                <h3>{{ patient.name }}</h3>
                <p>{{ patient.email }}</p>
                <p>{{ patient.age }} yrs · {{ patient.gender }}</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'DoctorDashboard',
  data() {
    return {
      doctor: {
        id: 101,
        name: 'Dr. Test Doctor',
        email: 'testdoctor@hospital.com',
        specialization: 'General Medicine',
        availability: 'Mon-Fri 9AM - 5PM',
        upcoming_appointments: 4,
        patients_count: 8,
        completed_appointments: 12
      },
      appointments: [
        { id: 1, patient_name: 'Test Patient One', date: '2026-04-10', time: '09:00', status: 'Booked' },
        { id: 2, patient_name: 'Test Patient Two', date: '2026-04-11', time: '10:30', status: 'Booked' },
        { id: 3, patient_name: 'Test Patient Three', date: '2026-04-12', time: '14:00', status: 'Booked' }
      ],
      patients: [
        { id: 1, name: 'Test Patient One', email: 'patient1@example.com', age: 30, gender: 'Female' },
        { id: 2, name: 'Test Patient Two', email: 'patient2@example.com', age: 26, gender: 'Male' },
        { id: 3, name: 'Test Patient Three', email: 'patient3@example.com', age: 42, gender: 'Female' }
      ]
    }
  },
  methods: {
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
.doctor-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}
.doctor-card {
  display: flex;
  width: 100%;
  max-width: 900px;
  border-radius: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
  background: #ffffff;
}
.panel-left {
  background: #1a6fd4;
  padding: 2.5rem 2rem;
  flex: 0 0 35%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  color: #fff;
}
.panel-left h2 {
  font-size: 1.55rem;
  font-weight: 700;
}
.panel-right {
  flex: 1;
  padding: 2.5rem 2.2rem;
  display: flex;
  flex-direction: column;
}
.panel-right h1 {
  margin-bottom: 0.25rem;
}
.doctor-meta {
  margin-bottom: 1.5rem;
  color: #475569;
}
.section-block {
  margin-bottom: 1.5rem;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}
.summary-card {
  padding: 1rem;
  border-radius: 0.85rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}
.summary-card strong {
  display: block;
  font-size: 1.5rem;
  margin-bottom: 0.35rem;
}
.appointments-list,
.patient-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.85rem;
}
.appointments-list li,
.patient-card {
  padding: 1rem;
  border-radius: 0.85rem;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
}
.appointments-list strong {
  display: block;
  margin-bottom: 0.4rem;
}
.status {
  color: #1a6fd4;
  font-weight: 600;
}
.patient-card h3 {
  margin-bottom: 0.35rem;
}
.nav-logout {
  border: none;
  background: transparent;
  color: #1a6fd4;
  cursor: pointer;
  font-weight: 600;
}
@media (max-width: 800px) {
  .doctor-card { flex-direction: column; }
  .panel-left, .panel-right { padding: 1.5rem; }
  .summary-grid { grid-template-columns: 1fr; }
}
</style>
