<template>
  <div class="admin-dashboard">
    <!-- TOP NAVBAR -->
    <div class="top-navbar">
      <div class="nav-left">MediZentrum</div>
      <div class="nav-center">Admin Dashboard</div>
      <div class="nav-right">
        <button class="btn btn-logout" @click="logout">Logout</button>
      </div>
    </div>

    <div class="page-wrapper">
      <!-- ALERTS -->
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

      <!-- WELCOME & SEARCH CARD -->
      <div class="card welcome-card">
        <div class="welcome-content">
          <h2 class="card-title">Search</h2>
          <div class="search-container">
            <select v-model="searchType" class="search-select">
              <option value="doctors">Doctors</option>
              <option value="patients">Patients</option>
            </select>
            <input
              v-model="searchTerm"
              type="text"
              class="search-input"
              placeholder="Search..."
              @keyup.enter="search"
            />
            <button class="btn btn-green" @click="search">Search</button>
            <button class="btn btn-outline-gray" @click="searchTerm = ''; search()">Reset</button>
          </div>
        </div>
      </div>

      <!-- DOCTORS SECTION -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Registered Doctors ({{ allDoctors.length }})</h2>
          <button class="btn btn-green" @click="openAddDoctorModal">+ Create Doctor</button>
        </div>

        <div class="simple-list">
          <div v-for="doctor in allDoctors" :key="doctor.id" class="list-row" :class="{ 'blacklisted-row': doctor.is_blacklisted }">
            <div class="list-info">
              <div class="list-name" :class="{ strikethrough: doctor.is_blacklisted }">{{ doctor.name || doctor.username }}</div>
              <div class="list-subtext">{{ doctor.specialization }} | {{ doctor.email }}</div>
            </div>
            <div class="list-actions">
              <button v-if="!doctor.is_blacklisted" class="btn btn-outline-yellow btn-sm" @click="editDoctor(doctor)">edit</button>
              <button v-if="!doctor.is_blacklisted" class="btn btn-outline-red btn-sm" @click="deleteDoctor(doctor.id)">delete</button>
              <button v-if="!doctor.is_blacklisted" class="btn btn-outline-gray btn-sm" @click="blacklistDoctor(doctor.id)">blacklist</button>
              <button v-if="doctor.is_blacklisted" class="btn btn-outline-blue btn-sm" @click="unblacklistDoctor(doctor.id)">unblacklist</button>
              <button class="btn btn-outline-blue btn-sm" @click="showDoctorDetails(doctor)">details</button>
            </div>
          </div>

          <div v-if="allDoctors.length === 0" class="list-row empty-row">
            <span>No doctors found</span>
          </div>
        </div>
      </div>

      <!-- PATIENTS SECTION -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Registered Patients ({{ filteredPatients.length }})</h2>
        </div>

        <div class="simple-list">
          <div class="list-row" v-for="patient in filteredPatients" :key="patient.id" :class="{ 'blacklisted-row': patient.is_blacklisted }">
            <div class="list-info">
              <div class="list-name" :class="{ strikethrough: patient.is_blacklisted }">{{ patient.name || patient.username }}</div>
              <div class="list-subtext">{{ patient.email }}</div>
            </div>
            <div class="list-actions">
              <button v-if="!patient.is_blacklisted" class="btn btn-outline-blue btn-sm" @click="showPatientDetails(patient)">details</button>
              <button v-if="!patient.is_blacklisted" class="btn btn-outline-yellow btn-sm" @click="editPatient(patient)">edit</button>
              <button v-if="patient.is_blacklisted" class="btn btn-outline-blue btn-sm" @click="unblacklistPatient(patient.id)">unblacklist</button>
            </div>
          </div>
          <div v-if="filteredPatients.length === 0" class="list-row empty-row">
            <span>No patients found</span>
          </div>
        </div>
      </div>

      <!-- APPOINTMENTS SECTION -->
      <div class="card">
        <div class="card-header no-button">
          <h2 class="card-title">Upcoming Appointments ({{ upcomingAppointments.length }})</h2>
        </div>

        <div class="table-shell">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(a, index) in upcomingAppointments" :key="a.id">
                <td>{{ index + 1 }}</td>
                <td>{{ a.patient_name }}</td>
                <td>{{ a.doctor_name }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td><span :class="['badge', 'badge-' + (a.status.toLowerCase())]">{{ a.status }}</span></td>
              </tr>
              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="6" class="empty-cell">No upcoming appointments</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PAST APPOINTMENTS SECTION -->
      <div class="card">
        <div class="card-header no-button">
          <h2 class="card-title">Past Appointments ({{ pastAppointments.length }})</h2>
        </div>

        <div class="table-shell">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(a, index) in pastAppointments" :key="a.id">
                <td>{{ index + 1 }}</td>
                <td>{{ a.patient_name }}</td>
                <td>{{ a.doctor_name }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td><span :class="['badge', 'badge-' + (a.status.toLowerCase())]">{{ a.status }}</span></td>
              </tr>
              <tr v-if="pastAppointments.length === 0">
                <td colspan="6" class="empty-cell">No past appointments</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ADD/EDIT DOCTOR MODAL -->
      <div v-if="showModal" class="modal-overlay" @click="closeDoctorModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>{{ isEditMode ? 'Edit Doctor' : 'Add New Doctor' }}</h3>
            <button class="close-btn" @click="closeDoctorModal">&times;</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Username:</label>
              <input v-model="doctorForm.username" placeholder="Doctor's name" class="form-input" />
            </div>

            <div class="form-group">
              <label>Email:</label>
              <input v-model="doctorForm.email" type="email" placeholder="Email" class="form-input" />
            </div>

            <div v-if="!isEditMode" class="form-group">
              <label>Password:</label>
              <input v-model="doctorForm.password" type="password" placeholder="Password" class="form-input" />
            </div>

            <div class="form-group">
              <label>Specialization:</label>
              <input v-model="doctorForm.specialization" placeholder="e.g., Cardiology" class="form-input" />
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline-gray" @click="closeDoctorModal">Cancel</button>
            <button class="btn btn-green" @click="submitDoctorForm">{{ isEditMode ? 'Update' : 'Create' }}</button>
          </div>
        </div>
      </div>

      <!-- EDIT PATIENT MODAL -->
      <div v-if="showPatientModal" class="modal-overlay" @click="closePatientModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>Edit Patient</h3>
            <button class="close-btn" @click="closePatientModal">&times;</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Username:</label>
              <input v-model="patientForm.username" placeholder="Patient's name" class="form-input" />
            </div>

            <div class="form-group">
              <label>Email:</label>
              <input v-model="patientForm.email" type="email" placeholder="Email" class="form-input" />
            </div>

            <div class="form-group">
              <label>Age:</label>
              <input v-model="patientForm.age" type="number" placeholder="Age" class="form-input" />
            </div>

            <div class="form-group">
              <label>Gender:</label>
              <select v-model="patientForm.gender" class="form-input">
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Contact Number:</label>
              <input v-model="patientForm.contact_number" placeholder="Contact number" class="form-input" />
            </div>

            <div class="form-group">
              <label>Address:</label>
              <input v-model="patientForm.address" placeholder="Address" class="form-input" />
            </div>

            <div class="form-group">
              <label>Height:</label>
              <input v-model="patientForm.height" type="number" placeholder="Height (cm)" class="form-input" />
            </div>

            <div class="form-group">
              <label>Weight:</label>
              <input v-model="patientForm.weight" type="number" placeholder="Weight (kg)" class="form-input" />
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline-gray" @click="closePatientModal">Cancel</button>
            <button class="btn btn-green" @click="submitPatientForm">Update</button>
          </div>
        </div>
      </div>

      <!-- DETAILS MODAL -->
      <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>{{ detailsTitle }}</h3>
            <button class="close-btn" @click="closeDetailsModal">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="detailsType === 'doctor'">
              <p><strong>Name:</strong> {{ selectedDetails.name }}</p>
              <p><strong>Email:</strong> {{ selectedDetails.email }}</p>
              <p><strong>Specialization:</strong> {{ selectedDetails.specialization }}</p>
              <p><strong>Status:</strong> <span :class="{ 'text-danger': selectedDetails.is_blacklisted, 'text-success': !selectedDetails.is_blacklisted }">
                {{ selectedDetails.is_blacklisted ? 'Blacklisted' : 'Active' }}
              </span></p>
            </div>
            <div v-else-if="detailsType === 'patient'">
              <p><strong>Name:</strong> {{ selectedDetails.name }}</p>
              <p><strong>Email:</strong> {{ selectedDetails.email }}</p>
              <p><strong>Age:</strong> {{ selectedDetails.age }}</p>
              <p><strong>Gender:</strong> {{ selectedDetails.gender }}</p>
              <p><strong>Contact:</strong> {{ selectedDetails.contact_number }}</p>
              <p><strong>Address:</strong> {{ selectedDetails.address || 'N/A' }}</p>
              <p><strong>Height:</strong> {{ selectedDetails.height }} cm</p>
              <p><strong>Weight:</strong> {{ selectedDetails.weight }} kg</p>
              <p><strong>Status:</strong> <span :class="{ 'text-danger': selectedDetails.is_blacklisted, 'text-success': !selectedDetails.is_blacklisted }">
                {{ selectedDetails.is_blacklisted ? 'Blacklisted' : 'Active' }}
              </span></p>
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline-gray" @click="closeDetailsModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export default {
  name: "AdminDashboard",
  data() {
    return {
      dashboardStats: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0,
        appointments_booked: 0,
        appointments_completed: 0,
        appointments_cancelled: 0
      },
      doctors: [],
      allDoctors: [],
      patients: [],
      appointments: [],
      filteredDoctors: [],
      filteredPatients: [],
      upcomingAppointments: [],
      pastAppointments: [],
      
      searchTerm: "",
      searchType: "doctors", // 'doctors' or 'patients'
      
      error: "",
      successMessage: "",
      showModal: false,
      showPatientModal: false,
      showDetailsModal: false,
      isEditMode: false,
      detailsType: "", // 'doctor' or 'patient'
      detailsTitle: "",
      selectedDetails: {},
      loading: true,

      doctorForm: {
        id: null,
        username: "",
        email: "",
        password: "",
        specialization: ""
      },
      patientForm: {
        id: null,
        username: "",
        email: "",
        age: "",
        gender: "",
        contact_number: "",
        address: "",
        height: "",
        weight: ""
      }
    };
  },

  mounted() {
    this.fetchDashboardData();
  },

  methods: {
    async fetchDashboardData() {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        // Fetch dashboard stats
        const statsRes = await axios.get(`${API_BASE_URL}/api/admin/dashboard`, { headers });
        this.dashboardStats = statsRes.data.data || statsRes.data.dashboard || statsRes.data;

        // Fetch doctors including blacklisted ones
        const doctorsRes = await axios.get(`${API_BASE_URL}/api/admin/doctors?include_blacklisted=true`, { headers });
        this.allDoctors = doctorsRes.data.doctors || [];
        this.filteredDoctors = this.allDoctors;

        // Fetch patients including blacklisted ones
        const patientsRes = await axios.get(`${API_BASE_URL}/api/admin/patients?include_blacklisted=true`, { headers });
        this.patients = patientsRes.data.patients || [];
        this.filteredPatients = this.patients;

        // Fetch appointments
        const appointmentsRes = await axios.get(`${API_BASE_URL}/api/admin/appointments`, { headers });
        this.appointments = appointmentsRes.data.appointments || [];
        
        // Separate upcoming and past appointments
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        this.upcomingAppointments = this.appointments.filter(a => {
          const apptDate = new Date(a.date);
          return apptDate >= today && a.status === 'Booked';
        });
        
        this.pastAppointments = this.appointments.filter(a => {
          return a.status === 'Completed' || a.status === 'Cancelled';
        });

        this.error = "";
        this.loading = false;
      } catch (err) {
        this.error = "Failed to load dashboard data";
        console.error("Error fetching dashboard:", err);
        this.loading = false;
      }
    },

    async search() {
      if (!this.searchTerm.trim()) {
        this.filteredDoctors = this.allDoctors;
        this.filteredPatients = this.patients;
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        if (this.searchType === "doctors") {
          const res = await axios.get(
            `${API_BASE_URL}/api/admin/doctors?search=${encodeURIComponent(this.searchTerm)}&include_blacklisted=true`,
            { headers }
          );
          this.filteredDoctors = res.data.doctors || [];
        } else {
          const res = await axios.get(
            `${API_BASE_URL}/api/admin/patients?search=${encodeURIComponent(this.searchTerm)}&include_blacklisted=true`,
            { headers }
          );
          this.filteredPatients = res.data.patients || [];
        }
      } catch (err) {
        this.error = "Search failed";
      }
    },

    openAddDoctorModal() {
      this.isEditMode = false;
      this.resetDoctorForm();
      this.showModal = true;
    },

    closeDoctorModal() {
      this.showModal = false;
    },

    editDoctor(doctor) {
      this.isEditMode = true;
      this.doctorForm = {
        id: doctor.id,
        username: doctor.name || doctor.username,
        email: doctor.email,
        password: "",
        specialization: doctor.specialization || ""
      };
      this.showModal = true;
    },

    editPatient(patient) {
      this.patientForm = {
        id: patient.id,
        username: patient.name || patient.username,
        email: patient.email,
        age: patient.age,
        gender: patient.gender,
        contact_number: patient.contact_number,
        address: patient.address || "",
        height: patient.height || "",
        weight: patient.weight || ""
      };
      this.showPatientModal = true;
    },

    closePatientModal() {
      this.showPatientModal = false;
    },

    showDoctorDetails(doctor) {
      this.detailsType = 'doctor';
      this.detailsTitle = `Doctor Details - ${doctor.name}`;
      this.selectedDetails = doctor;
      this.showDetailsModal = true;
    },

    showPatientDetails(patient) {
      this.detailsType = 'patient';
      this.detailsTitle = `Patient Details - ${patient.name}`;
      this.selectedDetails = patient;
      this.showDetailsModal = true;
    },

    closeDetailsModal() {
      this.showDetailsModal = false;
    },

    async deleteDoctor(id) {
      if (!confirm("Are you sure you want to delete this doctor?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.delete(`${API_BASE_URL}/api/admin/doctors/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.successMessage = "Doctor deleted successfully";
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to delete doctor";
      }
    },

    async blacklistDoctor(id) {
      if (!confirm("Are you sure you want to blacklist this doctor?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.post(`${API_BASE_URL}/api/admin/doctors/${id}/blacklist`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.successMessage = "Doctor blacklisted successfully";
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to blacklist doctor";
      }
    },

    async unblacklistDoctor(id) {
      if (!confirm("Are you sure you want to unblacklist this doctor?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.post(`${API_BASE_URL}/api/admin/doctors/${id}/unblacklist`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.successMessage = "Doctor unblacklisted successfully";
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to unblacklist doctor";
      }
    },

    async submitDoctorForm() {
      if (!this.doctorForm.username || !this.doctorForm.email || !this.doctorForm.specialization) {
        alert("Please fill all required fields");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        if (this.isEditMode) {
          await axios.put(`${API_BASE_URL}/api/admin/doctors/${this.doctorForm.id}`, {
            username: this.doctorForm.username,
            email: this.doctorForm.email,
            specialization: this.doctorForm.specialization
          }, { headers });
          this.successMessage = "Doctor updated successfully";
        } else {
          if (!this.doctorForm.password) {
            alert("Password is required for new doctors");
            return;
          }

          await axios.post(`${API_BASE_URL}/api/admin/doctors`, {
            username: this.doctorForm.username,
            email: this.doctorForm.email,
            password: this.doctorForm.password,
            specialization: this.doctorForm.specialization
          }, { headers });
          this.successMessage = "Doctor created successfully";
        }

        this.closeDoctorModal();
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        this.error = err.response?.data?.error || "Operation failed";
      }
    },

    async submitPatientForm() {
      if (!this.patientForm.username || !this.patientForm.email) {
        alert("Please fill all required fields");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        await axios.put(`${API_BASE_URL}/api/admin/patients/${this.patientForm.id}`, {
          username: this.patientForm.username,
          email: this.patientForm.email,
          age: this.patientForm.age,
          gender: this.patientForm.gender,
          contact_number: this.patientForm.contact_number,
          address: this.patientForm.address,
          height: this.patientForm.height,
          weight: this.patientForm.weight
        }, { headers });
        
        this.successMessage = "Patient updated successfully";
        this.closePatientModal();
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        this.error = err.response?.data?.error || "Operation failed";
      }
    },

    resetDoctorForm() {
      this.doctorForm = {
        id: null,
        username: "",
        email: "",
        password: "",
        specialization: ""
      };
    },

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
.admin-dashboard {
  min-height: 100vh;
  background: #f4f8ff;
  padding: 80px 0 40px;
  font-family: Georgia, "Times New Roman", serif;
}

.page-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
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
  z-index: 1000;
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
  background: #e35757 !important;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.btn-logout:hover {
  background: #d43d3d !important;
}

/* ALERTS */
.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  border-left: 4px solid;
}

.alert-danger {
  background: #f8d7da;
  color: #721c24;
  border-left-color: #f5c6cb;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border-left-color: #c3e6cb;
}

/* STATISTICS CARDS */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #2f80ed;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

/* CARDS */
.card {
  background: #ffffff;
  border: 1px solid #ebefe8;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(25, 25, 25, 0.05);
  padding: 18px;
  margin-bottom: 18px;
}

.welcome-card {
  margin-top: 16px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header.no-button {
  justify-content: flex-start;
}

.card-title {
  font-size: 22px;
  font-weight: 700;
  color: #222;
  margin: 0;
}

.search-container {
  display: flex;
  gap: 10px;
  flex: 1;
  min-width: 300px;
}

.search-select,
.search-input {
  flex: 1;
  height: 42px;
  border: 1px solid #dfe4dc;
  border-radius: 8px;
  background: #f8f8f8;
  padding: 0 14px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #2f80ed;
  background: white;
}

/* BUTTONS */
.btn {
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
  margin-right: 4px;
}

.btn-green {
  background: #4944d7;
  color: white;
}

.btn-green:hover {
  background: #3a3ab5;
}

.btn-outline-yellow {
  background: white;
  color: #d9b126;
  border: 1px solid #efd76f;
}

.btn-outline-yellow:hover {
  background: #fffbf0;
}

.btn-outline-red {
  background: white;
  color: #e35757;
  border: 1px solid #efb1b1;
}

.btn-outline-red:hover {
  background: #fff6f6;
}

.btn-outline-gray {
  background: white;
  color: #565656;
  border: 1px solid #cfcfcf;
}

.btn-outline-gray:hover {
  background: #f5f5f5;
}

/* LIST */
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
  background: #fff;
  transition: background 0.2s;
}

.list-row:hover {
  background: #f9f9f9;
}

.list-row.empty-row {
  justify-content: center;
  color: #999;
  font-style: italic;
}

.list-row.blacklisted-row {
  background: #f5f5f5;
  opacity: 0.8;
}

.strikethrough {
  text-decoration: line-through;
  color: #999;
}

.text-danger {
  color: #e35757;
  font-weight: 600;
}

.text-success {
  color: #28a745;
  font-weight: 600;
}

.list-info {
  flex: 1;
}

.list-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.list-subtext {
  font-size: 12px;
  color: #999;
}

.list-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* TABLE */
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
  text-align: left;
  font-size: 14px;
}

.appointments-table th {
  background: #f8f9fb;
  font-weight: 700;
  color: #333;
}

.appointments-table tbody tr:hover {
  background: #f9f9f9;
}

.empty-cell {
  text-align: center;
  color: #999;
  padding: 20px !important;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.badge-booked {
  background: #cfe2ff;
  color: #084298;
}

.badge-completed {
  background: #d1e7dd;
  color: #0f5132;
}

.badge-cancelled {
  background: #f8d7da;
  color: #842029;
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-box {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 450px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #2f80ed;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
  }

  .list-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .list-actions {
    width: 100%;
  }

  .appointments-table th,
  .appointments-table td {
    padding: 10px 8px;
    font-size: 12px;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>