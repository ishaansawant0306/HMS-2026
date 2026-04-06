<template>
  <div class="doctor-page">
    <!-- NAVBAR -->
    <nav class="top-nav">
      <div class="nav-inner">
        <span class="logo">MediZentrum</span>
        <button class="nav-logout" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- MAIN -->
    <main class="dashboard">

      <!-- WELCOME -->
      <div class="card">
        <h2>Welcome {{ doctor.name }}</h2>
      </div>

      <!-- APPOINTMENTS -->
      <div class="card">
        <h2>Upcoming Appointments</h2>

        <table class="appt-table">
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Patient Name</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(appt, index) in appointments" :key="appt.id">
              <td>{{ index + 1 }}</td>
              <td>{{ appt.patient_name }}</td>
              <td class="status">{{ appt.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PATIENTS -->
      <div class="card">
        <h2>Assigned Patients</h2>

        <div class="patient-row" v-for="patient in patients" :key="patient.id">
          <span>{{ patient.name }}</span>
          <button class="view-btn">View</button>
        </div>

        <button class="availability-btn">Provide Availability</button>
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
        name: 'Dr. Abcde'
      },
      appointments: [
        { id: 1, patient_name: 'Mr. abcde', status: 'Booked' }
      ],
      patients: [
        { id: 1, name: 'Mr. abcde' },
        { id: 2, name: 'Miss. Pqrst' }
      ]
    }
  },
  methods: {
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>

/* PAGE */
.dashboard {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
}

/* NAVBAR */
.top-nav {
  background: white;
  padding: 12px 20px;
  border-bottom: 1px solid #ddd;
}
.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-weight: 700;
  font-size: 18px;
}
.nav-logout {
  border: 1px solid #ccc;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  background: white;
}

/* CARDS */
.card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* TABLE */
.appt-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.appt-table th,
.appt-table td {
  border-bottom: 1px solid #eee;
  padding: 10px;
  text-align: left;
}
.status {
  color: green;
  font-weight: 600;
}

/* PATIENT LIST */
.patient-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 10px;
}

/* BUTTONS */
.view-btn {
  background: #1a6fd4;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.availability-btn {
  margin-top: 10px;
  background: green;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  float: right;
}

</style>