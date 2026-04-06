<template>
  <div class="admin-dashboard">
    <!-- TOP NAVBAR -->
    <div class="top-navbar">
      <div class="nav-left">MediZentrum</div>
      <div class="nav-center">Admin Dashboard</div>
    </div>

      <div class="card welcome-card">
        <div class="welcome-content">
          <h2 class="card-title">Welcome Admin</h2>
          <div class="search-container">
            <input
              v-model="doctorSearch"
              type="text"
              class="search-input"
              placeholder="doctor, patient, department..."
            />
            <button class="btn btn-green" @click="searchDoctors">search</button>
          </div>
        </div>
      </div>

      <!-- DOCTORS -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Registered Doctors</h2>
          <button class="btn btn-green" @click="openAddDoctorModal">+ create</button>
        </div>

        <div class="simple-list">
          <div v-for="doctor in doctors" :key="doctor.id" class="list-row">
            <div class="list-name">{{ doctor.name }}</div>
            <div class="list-actions">
              <button class="btn btn-outline-yellow" @click="editDoctor(doctor)">edit</button>
              <button class="btn btn-outline-red" @click="deleteDoctor(doctor.id)">delete</button>
              <button class="btn btn-outline-gray" @click="blacklistDoctor(doctor.id)">blacklist</button>
            </div>
          </div>

          <div v-if="doctors.length === 0" class="list-row empty-row">
            <span>No doctors found</span>
          </div>
        </div>
      </div>

      <!-- PATIENTS -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Registered Patients</h2>
        </div>

        <div class="simple-list">
          <div class="list-row" v-for="p in patients" :key="p.id">
            <div class="list-name">{{ p.name }}</div>
            <div class="list-actions">
              <button class="btn btn-outline-yellow">edit</button>
              <button class="btn btn-outline-red">delete</button>
              <button class="btn btn-outline-gray">blacklist</button>
            </div>
          </div>
        </div>
      </div>

      <!-- APPOINTMENTS -->
      <div class="card">
        <div class="card-header no-button">
          <h2 class="card-title">Upcoming Appointments</h2>
        </div>

        <div class="table-shell">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Department</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(a, index) in appointments" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ a.patient }}</td>
                <td>{{ a.doctor }}</td>
                <td>{{ a.department }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ALERTS -->
      <div v-if="error" class="alert alert-danger fixed-alert">{{ error }}</div>
      <div v-if="successMessage" class="alert alert-success fixed-alert">{{ successMessage }}</div>

      <!-- SIMPLE MODAL -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal-box">
          <h3>{{ isEditMode ? 'Edit Doctor' : 'Add Doctor' }}</h3>

          <input v-model="doctorForm.username" placeholder="Username" />
          <input v-model="doctorForm.email" placeholder="Email" />

          <input
            v-if="!isEditMode"
            v-model="doctorForm.password"
            type="password"
            placeholder="Password"
          />

          <input v-model="doctorForm.specialization" placeholder="Specialization" />

          <div class="modal-actions">
            <button class="btn btn-outline-gray" @click="closeDoctorModal">Cancel</button>
            <button class="btn btn-green" @click="submitDoctorForm">Save</button>
          </div>
        </div>
      </div>
    </div>
  
</template>

<script>
export default {
  name: "AdminDashboard",

  data() {
    return {
      doctorSearch: "",
      doctors: [],
      patients: [],
      appointments: [],
      error: "",
      successMessage: "",
      showModal: false,
      isEditMode: false,

      doctorForm: {
        id: null,
        username: "",
        email: "",
        password: "",
        specialization: ""
      }
    };
  },

  methods: {
    searchDoctors() {
      const term = this.doctorSearch.toLowerCase();
      this.doctors = this.doctors.filter(d =>
        d.name.toLowerCase().includes(term)
      );
    },

    openAddDoctorModal() {
      this.isEditMode = false;
      this.resetForm();
      this.showModal = true;
    },

    closeDoctorModal() {
      this.showModal = false;
    },

    editDoctor(doctor) {
      this.isEditMode = true;
      this.doctorForm = { ...doctor };
      this.showModal = true;
    },

    deleteDoctor(id) {
      this.doctors = this.doctors.filter(d => d.id !== id);
      this.successMessage = "Doctor deleted";
    },

    blacklistDoctor(id) {
      this.successMessage = "Doctor blacklisted";
    },

    submitDoctorForm() {
      if (this.isEditMode) {
        const index = this.doctors.findIndex(d => d.id === this.doctorForm.id);
        this.doctors[index] = { ...this.doctorForm };
        this.successMessage = "Doctor updated";
      } else {
        this.doctors.push({
          ...this.doctorForm,
          id: Date.now(),
          name: this.doctorForm.username
        });
        this.successMessage = "Doctor added";
      }

      this.closeDoctorModal();
    },

    resetForm() {
      this.doctorForm = {
        id: null,
        username: "",
        email: "",
        password: "",
        specialization: ""
      };
    }
  },

  mounted() {
    // Dummy data (so UI shows immediately)
    this.doctors = [
      { id: 1, name: "Dr. Hori", specialization: "Cardiology" },
      { id: 2, name: "Dr. Miyamura", specialization: "Neurology" }
    ];

    this.patients = [
      { id: 1, name: "Mr. Tanaka" },
      { id: 2, name: "Miss. Yuki" }
    ];

    this.appointments = [
      {
        patient: "Tanaka",
        doctor: "Dr. Hori",
        department: "Cardiology"
      }
    ];
  }
};
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: #f4f8ff;
  padding: 80px 0 40px;
  font-family: Georgia, "Times New Roman", serif;
}

.top-brand {
  position: absolute;
  top: 18px;
  left: 26px;
  font-size: 28px;
  font-weight: 700;
  color: #1f1f1f;
}

.page-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 10px; 
}

.hero-header {
  text-align: center;
  margin-bottom: 18px;
}

.hero-title {
  font-size: 34px;
  font-weight: 700;
  color: #232323;
}

.card {
  background: #ffffff;
  border: 1px solid #ebefe8;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(25, 25, 25, 0.05);
  padding: 18px;
  margin-bottom: 18px;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.welcome-card {
  margin-top: 34px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.card-header.no-button {
  justify-content: flex-start;
}

.card-title {
  font-size: 22px;
  font-weight: 700;
  color: #222;
}

.search-container {
  display: flex;
  gap: 10px;
  width: 52%;
}

.search-input {
  flex: 1;
  height: 42px;
  border: 1px solid #dfe4dc;
  border-radius: 8px;
  background: #f8f8f8;
  padding: 0 14px;
}

.btn {
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-green {
  background: #4944d7;
  color: white;
}

.btn-outline-yellow {
  background: white;
  color: #d9b126;
  border: 1px solid #efd76f;
}

.btn-outline-red {
  background: white;
  color: #e35757;
  border: 1px solid #efb1b1;
}

.btn-outline-gray {
  background: white;
  color: #565656;
  border: 1px solid #cfcfcf;
}

.simple-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.list-row {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-actions {
  display: flex;
  gap: 8px;
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

.appointments-table th,
.appointments-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #ececec;
}

.appointments-table thead {
  background: #f8f9fb;
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-box input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
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

</style>