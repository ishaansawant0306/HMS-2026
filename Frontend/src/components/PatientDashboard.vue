<template>
  <div class="patient-dashboard">
    <header class="topbar">
      <div class="brand">MediZentrum</div>
      <h1 class="page-title">Patients' Dashboard</h1>
      <button class="btn btn-logout" @click="logout">Logout</button>
    </header>

    <main class="page-wrapper">
      <section class="card welcome-card">
        <div class="welcome-row">
          <h2 class="section-title">Welcome {{ patient.name }}</h2>
          <div class="top-links">
            <button class="link-btn">edit profile</button>
            <span>|</span>
            <button class="link-btn">History</button>
            <span>|</span>
            <button class="link-btn" @click="logout">logout</button>
          </div>
        </div>
      </section>

      <section class="card">
        <h2 class="section-title">Departments</h2>

        <div class="department-list">
          <div v-for="(dept, index) in departments" :key="index" class="department-row">
            <span class="dept-name">{{ dept }}</span>
            <button class="btn btn-blue">view details</button>
          </div>
        </div>
      </section>

      <section class="card">
        <h2 class="section-title">Upcoming Appointments</h2>

        <div class="table-shell">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Doctor Name</th>
                <th>Deptt</th>
                <th>Date</th>
                <th>Time</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(appointment, index) in appointments" :key="appointment.id">
                <td>{{ 1001 + index }}</td>
                <td>{{ appointment.doctor }}</td>
                <td>{{ appointment.department }}</td>
                <td>{{ appointment.date }}</td>
                <td>{{ appointment.time }}</td>
                <td>
                  <button class="btn btn-outline-red" @click="cancelAppointment(appointment.id)">
                    cancel
                  </button>
                </td>
              </tr>

              <tr v-if="appointments.length === 0">
                <td colspan="6" class="empty-cell">No upcoming appointments</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "PatientDashboard",
  data() {
    return {
      patient: {
        name: "Pqrst",
        email: "leon@gmail.com"
      },
      departments: ["Cardiology", "Oncology", "General"],
      appointments: [
        {
          id: 1,
          doctor: "Dr. abcde",
          department: "general",
          date: "24/09/2025",
          time: "08 am - 12 pm"
        }
      ]
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("user");
      this.$router.push("/login");
    },
    cancelAppointment(id) {
      this.appointments = this.appointments.filter((appt) => appt.id !== id);
    }
  }
};
</script>

<style scoped>
.patient-dashboard {
  min-height: 100vh;
  background: #f4f8ff;
  font-family: Georgia, "Times New Roman", serif;
  padding-top: 80px;
}

.topbar {
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

.brand {
  position: absolute;
  left: 30px;
  font-size: 22px;
  font-weight: 700;
  color: #1f1f1f;
}

.logout-btn {
  border: 1px solid #d7d7d7;
  background: #fff;
  color: #333;
  border-radius: 999px;
  padding: 10px 22px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-logout {
  position: absolute;
  right: 30px;
  background: #e35757;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #2d2d2d;
}

.page-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 30px 30px 40px 30px;
}

.card {
  background: #fff;
  border: 1px solid #eaf0e8;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(20, 20, 20, 0.05);
  padding: 18px;
  margin-bottom: 18px;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.welcome-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.section-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 14px;
  color: #222;
}

.welcome-card .section-title {
  margin: 0;
}

.top-links {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #555;
  font-size: 14px;
}

.link-btn {
  background: transparent;
  border: none;
  color: #555;
  cursor: pointer;
  font-size: 14px;
}

.department-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.department-row {
  border: 1px solid #ececec;
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
}

.dept-name {
  font-size: 16px;
  color: #444;
}

.btn {
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
  text-transform: lowercase;
}

.btn-blue {
  background: #2f80ed;
  border-color: #2f80ed;
  color: white;
}

.btn-blue:hover {
  background: #1f6fda;
}

.btn-outline-red {
  background: #fff;
  color: #e25454;
  border: 1px solid #efb2b2;
}

.btn-outline-red:hover {
  background: #fff6f6;
}

.table-shell {
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  overflow: hidden;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table thead {
  background: #fafbfc;
}

.appointments-table th,
.appointments-table td {
  padding: 14px 16px;
  text-align: left;
  font-size: 15px;
  color: #444;
  border-bottom: 1px solid #ececec;
}

.appointments-table th {
  color: #333;
  font-weight: 700;
}

.empty-cell {
  text-align: center;
  color: #888;
  font-style: italic;
}

@media (max-width: 768px) {
  .topbar {
    padding: 0 16px;
  }

  .brand {
    font-size: 20px;
  }

  .page-title {
    font-size: 28px;
  }

  .welcome-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .department-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .appointments-table th,
  .appointments-table td {
    font-size: 13px;
    padding: 10px;
  }
}
</style>