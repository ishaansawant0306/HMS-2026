<template>
  <div class="doctor-dashboard">
    <!-- TOP NAVBAR -->
    <div class="top-navbar">
      <div class="nav-left">MediZentrum</div>
      <div class="nav-center">Doctor Dashboard</div>
      <div class="nav-right">
        <button class="btn btn-logout" @click="logout">Logout</button>
      </div>
    </div>

    <div class="page-wrapper">
      <section class="top-card">
        <h1 class="welcome-title">Welcome {{ doctor.name }}</h1>
      </section>

      <section class="content-card">
        <h2 class="section-title">Upcoming Appointments</h2>

        <div class="table-shell">
          <table class="dashboard-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Patient Name</th>
                <th>Patient History</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(appt, index) in appointments" :key="appt.id">
                <td>{{ 1001 + index }}.</td>
                <td>{{ appt.patient_name }}</td>
                <td>
                  <button class="btn btn-blue">update</button>
                </td>
                <td class="action-group">
                  <button class="btn btn-green">mark as complete</button>
                  <button class="btn btn-red-outline">cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="content-card">
        <h2 class="section-title">Assigned Patients</h2>

        <div class="patient-list">
          <div v-for="patient in patients" :key="patient.id" class="patient-row">
            <span class="patient-name">{{ patient.name }}</span>
            <button class="btn btn-blue">view</button>
          </div>
        </div>

        <div class="bottom-action">
          <button class="btn btn-green large-btn">Provide Availability</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "DoctorDashboard",
  data() {
    return {
      doctor: {
        id: 101,
        name: "Dr. Abcde",
        email: "testdoctor@hospital.com",
        specialization: "General Medicine",
        availability: "Mon-Fri 9AM - 5PM"
      },
      appointments: [
        { id: 1, patient_name: "Mr. abcde", date: "2026-04-10", time: "09:00", status: "Booked" }
      ],
      patients: [
        { id: 1, name: "Mr. abcde" },
        { id: 2, name: "Miss. Pqrst" }
      ]
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("user");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.doctor-dashboard {
  min-height: 100vh;
  background: #f4f8ff;
  padding: 80px 0 40px;
  font-family: Georgia, "Times New Roman", serif;
}

.top-navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: 60px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #eee;
}

.nav-left {
  position: absolute;
  left: 30px;
  font-size: 22px;
  font-weight: 700;
}

.nav-center {
  font-size: 24px;
  font-weight: 700;
}

.nav-right {
  position: absolute;
  right: 30px;
}

.btn-logout {
  background: #e35757;
  color: white;
}

.page-wrapper {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 30px;
}

.top-card,
.content-card {
  background: #ffffff;
  border: 1px solid #ebefe9;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.top-card {
  padding: 22px 24px;
  margin-bottom: 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-title {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: #1f1f1f;
}

.logout-btn {
  border: 1px solid #d8d8d8;
  background: #fff;
  color: #555;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 600;
}

.content-card {
  padding: 22px 22px 18px;
  margin-bottom: 22px;
}

.section-title {
  margin: 0 0 18px;
  font-size: 24px;
  font-weight: 700;
  color: #222;
}

.table-shell {
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  overflow: hidden;
}

.dashboard-table {
  width: 100%;
  border-collapse: collapse;
}

.dashboard-table thead {
  background: #f8f9fb;
}

.dashboard-table th,
.dashboard-table td {
  padding: 14px 18px;
  text-align: left;
  font-size: 15px;
  color: #3c3c3c;
  border-bottom: 1px solid #ececec;
}

.dashboard-table th {
  font-weight: 700;
  color: #2d2d2d;
}

.action-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.patient-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.patient-row {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  background: #fff;
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.patient-name {
  color: #444;
  font-size: 16px;
}

.bottom-action {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}

.btn {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
  text-transform: lowercase;
}

.large-btn {
  padding: 10px 18px;
}

.btn-green {
  background: #16c341;
  border-color: #16c341;
  color: #fff;
}

.btn-green:hover {
  background: #11ad39;
}

.btn-blue {
  background: #2f80ed;
  border-color: #2f80ed;
  color: #fff;
}

.btn-blue:hover {
  background: #1f6fd8;
}

.btn-red-outline {
  background: #fff;
  color: #e55353;
  border: 1px solid #efb3b3;
}

.btn-red-outline:hover {
  background: #fff5f5;
}

@media (max-width: 768px) {
  .top-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .dashboard-table th,
  .dashboard-table td {
    padding: 10px 12px;
    font-size: 13px;
  }

  .patient-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .bottom-action {
    justify-content: stretch;
  }

  .large-btn {
    width: 100%;
  }
}
</style>