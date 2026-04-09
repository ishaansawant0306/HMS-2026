<template>
  <div class="patient-dashboard">
    <header class="topbar">
      <div class="brand">MediZentrum</div>
      <h1 class="page-title">Patients' Dashboard</h1>
      <button class="btn btn-logout" @click="logout">Logout</button>
    </header>

    <main class="page-wrapper">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <section class="card welcome-card">
        <div class="welcome-row">
          <h2 class="section-title">Welcome {{ patientDisplayName }}</h2>
          <div class="top-links">
            <button class="link-btn" @click="openEditProfileModal">edit profile</button>
            <span>|</span>
            <button class="link-btn" @click="showHistoryModal = true">History</button>
            <span>|</span>
            <button class="link-btn" @click="startHistoryExport">Export History</button>
          </div>
        </div>
        <div v-if="exportTaskId" class="export-status-row">
          <div class="export-status">
            <strong>Export:</strong> {{ exportTaskStatus }}
            <span v-if="exportResult && exportResult.filename">• <a :href="downloadLink" target="_blank">Download {{ exportResult.filename }}</a></span>
          </div>
        </div>
      </section>

      <section class="card">
        <h2 class="section-title">Search for Doctor</h2>
        <div class="search-section">
          <div class="search-form">
            <input v-model="doctorSearchForm.name" type="text" placeholder="Doctor name" class="form-control" />
            <select v-model="doctorSearchForm.specialization" class="form-control">
              <option value="">All Specializations</option>
              <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
            </select>
            <button class="btn btn-blue" @click="searchDoctors">Search</button>
            <button class="btn btn-secondary" @click="resetDoctorSearch">Reset</button>
          </div>
        </div>
        <div v-if="searchDoctorsResults.length > 0" class="department-list" style="margin-top: 16px;">
          <div v-for="doctor in searchDoctorsResults" :key="doctor.id" class="department-row">
            <div>
              <div style="font-weight: 600; color: #333;">Dr. {{ doctor.name }}</div>
              <div style="font-size: 12px; color: #999;">{{ doctor.specialization }} | {{ doctor.email }}</div>
            </div>
            <button class="btn btn-blue btn-sm" @click="selectDoctorForBooking(doctor)">Book</button>
          </div>
        </div>
      </section>

      <section class="card">
        <h2 class="section-title">Available Specializations</h2>
        <div class="department-list">
          <div v-for="(dept, index) in departments" :key="index" class="department-row">
            <span class="dept-name">{{ dept }}</span>
            <button class="btn btn-blue" @click="selectedSpecialization = dept; filterDoctorsBySpecialization()">
              view doctors
            </button>
          </div>
        </div>
      </section>

      <section class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h2 class="section-title">Upcoming Appointments</h2>
          <button class="btn btn-blue" @click="openBookingModal">+ Book Appointment</button>
        </div>

        <div class="table-shell">
          <table class="appointments-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Doctor Name</th>
                <th>Specialty</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(appointment, index) in upcomingAppointments" :key="appointment.id">
                <td>{{ 1001 + index }}</td>
                <td>{{ appointment.doctor_name }}</td>
                <td>{{ appointment.specialization }}</td>
                <td>{{ appointment.date }}</td>
                <td>{{ appointment.time }}</td>
                <td><span class="badge badge-success">{{ appointment.status }}</span></td>
                <td>
                  <button class="btn btn-outline-blue btn-sm" @click="openRescheduleModal(appointment)">
                    reschedule
                  </button>
                  <button class="btn btn-outline-red btn-sm" @click="cancelAppointment(appointment.id)">
                    cancel
                  </button>
                </td>
              </tr>

              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="7" class="empty-cell">No upcoming appointments</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Booking Modal -->
      <div v-if="showBookingModal" class="modal-overlay" @click="closeBookingModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Book an Appointment</h3>
            <button class="close-btn" @click="closeBookingModal">&times;</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Doctor Specialization:</label>
              <select v-model="selectedSpecialization" @change="filterDoctorsBySpecialization" class="form-control">
                <option value="">All Specializations</option>
                <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
              </select>
            </div>

            <div class="form-group">
              <label>Select Doctor:</label>
              <select v-model="bookingForm.doctor_id" class="form-control">
                <option value="">-- Select a Doctor --</option>
                <option v-for="doctor in availableDoctors" :key="doctor.id" :value="doctor.id">
                  Dr. {{ doctor.name }} ({{ doctor.specialization }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Date:</label>
              <input v-model="bookingForm.date" type="date" class="form-control" :min="minDate" :max="maxDate" />
            </div>

            <div class="form-group">
              <label>Time:</label>
              <input v-model="bookingForm.time" type="time" class="form-control" />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeBookingModal">Cancel</button>
            <button class="btn btn-blue" @click="bookAppointment">Book Appointment</button>
          </div>
        </div>
      </div>

      <!-- Edit Profile Modal -->
      <div v-if="showEditProfileModal" class="modal-overlay" @click="closeEditProfileModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Edit Profile</h3>
            <button class="close-btn" @click="closeEditProfileModal">&times;</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Name:</label>
              <input v-model="profileForm.username" type="text" class="form-control" />
            </div>

            <div class="form-group">
              <label>Email:</label>
              <input v-model="profileForm.email" type="email" class="form-control" />
            </div>

            <div class="form-group">
              <label>Age:</label>
              <input v-model="profileForm.age" type="number" class="form-control" />
            </div>

            <div class="form-group">
              <label>Gender:</label>
              <select v-model="profileForm.gender" class="form-control">
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Contact Number:</label>
              <input v-model="profileForm.contact_number" type="text" class="form-control" />
            </div>

            <div class="form-group">
              <label>Address:</label>
              <input v-model="profileForm.address" type="text" class="form-control" />
            </div>

            <div class="form-group">
              <label>Height (cm):</label>
              <input v-model="profileForm.height" type="number" class="form-control" />
            </div>

            <div class="form-group">
              <label>Weight (kg):</label>
              <input v-model="profileForm.weight" type="number" class="form-control" />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeEditProfileModal">Cancel</button>
            <button class="btn btn-blue" @click="submitProfileUpdate">Save Changes</button>
          </div>
        </div>
      </div>

      <!-- Reschedule Modal -->
      <div v-if="showRescheduleModal" class="modal-overlay" @click="closeRescheduleModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Reschedule Appointment</h3>
            <button class="close-btn" @click="closeRescheduleModal">&times;</button>
          </div>

          <div class="modal-body">
            <p style="margin-bottom: 16px;"><strong>Current Appointment:</strong><br>
                Dr. {{ selectedRescheduleAppointment && selectedRescheduleAppointment.doctor_name }} - {{ selectedRescheduleAppointment && selectedRescheduleAppointment.date }} {{ selectedRescheduleAppointment && selectedRescheduleAppointment.time }}
            </p>

            <div class="form-group">
              <label>New Date:</label>
              <input v-model="rescheduleForm.date" type="date" class="form-control" :min="minDate" :max="maxDate" />
            </div>

            <div class="form-group">
              <label>New Time:</label>
              <input v-model="rescheduleForm.time" type="time" class="form-control" />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeRescheduleModal">Cancel</button>
            <button class="btn btn-blue" @click="submitReschedule">Reschedule</button>
          </div>
        </div>
      </div>

      <!-- History Modal -->
      <div v-if="showHistoryModal" class="modal-overlay" @click="showHistoryModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Appointment History & Medical Records</h3>
            <button class="close-btn" @click="showHistoryModal = false">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="pastAppointments.length === 0" class="empty-cell">No past appointments</div>
            <div v-for="appt in pastAppointments" :key="appt.id" class="history-item">
              <h4>Dr. {{ appt.doctor_name }} ({{ appt.specialization }})</h4>
              <p><strong>Date:</strong> {{ appt.date }}</p>
              <p v-if="appt.diagnosis"><strong>Diagnosis:</strong> {{ appt.diagnosis }}</p>
              <p v-if="appt.prescription"><strong>Prescription:</strong> {{ appt.prescription }}</p>
              <p v-if="appt.notes"><strong>Notes:</strong> {{ appt.notes }}</p>
              <hr />
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showHistoryModal = false">Close</button>
          </div>
        </div>
      </div>

      <!-- View Doctors Modal -->
      <div v-if="showDoctorsModal" class="modal-overlay" @click="closeDoctorsModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Doctors in {{ selectedSpecialization }}</h3>
            <button class="close-btn" @click="closeDoctorsModal">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="specializationDoctors.length === 0" class="empty-cell">No doctors found in this specialization</div>
            <div v-for="doctor in specializationDoctors" :key="doctor.id" class="doctor-row">
              <div>
                <div style="font-weight: 600; color: #333;">Dr. {{ doctor.name }}</div>
                <div style="font-size: 12px; color: #999;">{{ doctor.email }}</div>
              </div>
              <button class="btn btn-blue btn-sm" @click="selectDoctorForBooking(doctor); closeDoctorsModal()">Book</button>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeDoctorsModal">Close</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export default {
  name: "PatientDashboard",
  data() {
    return {
      patient: {
        name: "",
        email: "",
        age: "",
        gender: ""
      },
      departments: [],
      appointments: [],
      medicalHistory: [],
      availableDoctors: [],
      searchDoctorsResults: [],
      loading: true,
      error: null,
      showBookingModal: false,
      showHistoryModal: false,
      showEditProfileModal: false,
      showRescheduleModal: false,
      showDoctorsModal: false,
      exportLoading: false,
      exportTaskId: null,
      exportTaskStatus: "",
      exportResult: null,
      selectedSpecialization: "",
      selectedRescheduleAppointment: null,
      specializationDoctors: [],
      bookingForm: {
        doctor_id: "",
        date: "",
        time: ""
      },
      profileForm: {
        username: "",
        email: "",
        age: "",
        gender: "",
        contact_number: "",
        address: "",
        height: "",
        weight: ""
      },
      rescheduleForm: {
        date: "",
        time: ""
      },
      doctorSearchForm: {
        name: "",
        specialization: ""
      }
    };
  },
  computed: {
    minDate() {
      const d = new Date();
      return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().split('T')[0];
    },
    maxDate() {
      const d = new Date();
      d.setDate(d.getDate() + 7);
      return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().split('T')[0];
    },
    upcomingAppointments() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return this.appointments.filter(appt => {
        const apptDate = new Date(appt.date);
        return apptDate >= today && appt.status === "Booked";
      });
    },
    pastAppointments() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return this.appointments.filter(appt => {
        const apptDate = new Date(appt.date);
        return apptDate < today && appt.status === "Completed";
      });
    },
    patientDisplayName() {
      const rawName = this.patient.name || this.patient.email || "";
      if (!rawName) return "";
      if (rawName.includes("@")) {
        const firstSegment = rawName.split("@")[0];
        const firstName = firstSegment.split(/[._\- ]+/)[0] || firstSegment;
        return firstName.charAt(0).toUpperCase() + firstName.slice(1);
      }
      return rawName.split(" ")[0] || rawName;
    },
    downloadLink() {
      return this.exportResult?.filename
        ? `${API_BASE_URL}/api/patient/export/download/${encodeURIComponent(this.exportResult.filename)}`
        : "";
    }
  },
  mounted() {
    this.fetchDashboardData();
    this.fetchAppointments();
    this.fetchMedicalHistory();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_BASE_URL}/api/patient/dashboard`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.patient = response.data.patient;
        // Only show specializations that have non-blacklisted doctors
        this.departments = response.data.specializations || [];
        
        // Load profile form with patient data
        this.profileForm = {
          username: this.patient.name,
          email: this.patient.email,
          age: this.patient.age,
          gender: this.patient.gender,
          contact_number: this.patient.contact_number || "",
          address: this.patient.address || "",
          height: this.patient.height || "",
          weight: this.patient.weight || ""
        };
        
        this.error = null;
      } catch (err) {
        this.error = "Failed to load dashboard data";
        console.error("Error fetching dashboard:", err);
      } finally {
        this.loading = false;
      }
    },

    async fetchAppointments() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_BASE_URL}/api/patient/appointments`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.appointments = response.data.appointments || [];
      } catch (err) {
        console.error("Error fetching appointments:", err);
      }
    },

    async fetchMedicalHistory() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_BASE_URL}/api/patient/medical-history`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.medicalHistory = response.data.medical_history || [];
      } catch (err) {
        console.error("Error fetching medical history:", err);
      }
    },

    async fetchAvailableDoctors(specialization = "") {
      try {
        const token = localStorage.getItem("token");
        let url = `${API_BASE_URL}/api/patient/doctors/available`;
        if (specialization) {
          url += `?specialization=${encodeURIComponent(specialization)}`;
        }
        
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.availableDoctors = response.data.doctors || [];
      } catch (err) {
        console.error("Error fetching available doctors:", err);
      }
    },

    async searchDoctors() {
      try {
        const token = localStorage.getItem("token");
        let url = `${API_BASE_URL}/api/patient/doctors/available`;
        const params = [];
        
        if (this.doctorSearchForm.specialization) {
          params.push(`specialization=${encodeURIComponent(this.doctorSearchForm.specialization)}`);
        }
        if (this.doctorSearchForm.name) {
          params.push(`name=${encodeURIComponent(this.doctorSearchForm.name)}`);
        }
        
        if (params.length > 0) {
          url += `?${params.join('&')}`;
        }
        
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.searchDoctorsResults = response.data.doctors || [];
      } catch (err) {
        console.error("Error searching doctors:", err);
        this.error = "Failed to search doctors";
      }
    },

    resetDoctorSearch() {
      this.doctorSearchForm = {
        name: "",
        specialization: ""
      };
      this.searchDoctorsResults = [];
    },

    selectDoctorForBooking(doctor) {
      this.bookingForm.doctor_id = doctor.id;
      this.openBookingModal();
    },

    openBookingModal() {
      this.showBookingModal = true;
      this.fetchAvailableDoctors();
    },

    closeBookingModal() {
      this.showBookingModal = false;
      this.bookingForm = { doctor_id: "", date: "", time: "" };
      this.selectedSpecialization = "";
    },

    openEditProfileModal() {
      this.showEditProfileModal = true;
    },

    closeEditProfileModal() {
      this.showEditProfileModal = false;
    },

    openRescheduleModal(appointment) {
      this.selectedRescheduleAppointment = appointment;
      this.rescheduleForm = { date: appointment.date, time: appointment.time };
      this.showRescheduleModal = true;
    },

    closeRescheduleModal() {
      this.showRescheduleModal = false;
      this.selectedRescheduleAppointment = null;
      this.rescheduleForm = { date: "", time: "" };
    },

    async submitProfileUpdate() {
      try {
        const token = localStorage.getItem("token");
        await axios.put(
          `${API_BASE_URL}/api/patient/profile`,
          {
            username: this.profileForm.username,
            email: this.profileForm.email,
            age: this.profileForm.age,
            gender: this.profileForm.gender,
            contact_number: this.profileForm.contact_number,
            address: this.profileForm.address,
            height: this.profileForm.height,
            weight: this.profileForm.weight
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        alert("Profile updated successfully!");
        this.closeEditProfileModal();
        this.fetchDashboardData();
      } catch (err) {
        console.error("Profile update error:", err);
        alert(err.response?.data?.error || err.response?.data?.message || "Failed to update profile");
      }
    },

    async bookAppointment() {
      if (!this.bookingForm.doctor_id || !this.bookingForm.date || !this.bookingForm.time) {
        alert("Please fill all required fields");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          `${API_BASE_URL}/api/patient/appointments/book`,
          {
            doctor_id: parseInt(this.bookingForm.doctor_id),
            date: this.bookingForm.date,
            time: this.bookingForm.time
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Optimistically add the appointment to local state for immediate UI update
        if (response.data.appointment) {
          this.appointments.push({
            id: response.data.appointment.id,
            doctor_name: response.data.appointment.doctor_name,
            specialization: response.data.appointment.specialization,
            date: response.data.appointment.date,
            time: response.data.appointment.time,
            status: response.data.appointment.status
          });
        }
        
        alert("Appointment booked successfully!");
        this.closeBookingModal();
        
        // Still fetch appointments to ensure consistency (cache should be cleared on backend)
        this.fetchAppointments();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to book appointment");
      }
    },

    async submitReschedule() {
      if (!this.rescheduleForm.date || !this.rescheduleForm.time) {
        alert("Please fill all required fields");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/patient/appointments/${this.selectedRescheduleAppointment.id}/reschedule`,
          { 
            date: this.rescheduleForm.date, 
            time: this.rescheduleForm.time 
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Optimistically update the appointment in local state
        const appointmentIndex = this.appointments.findIndex(appt => appt.id === this.selectedRescheduleAppointment.id);
        if (appointmentIndex !== -1) {
          this.appointments[appointmentIndex].date = this.rescheduleForm.date;
          this.appointments[appointmentIndex].time = this.rescheduleForm.time;
        }
        
        alert("Appointment rescheduled successfully!");
        this.closeRescheduleModal();
        
        // Still fetch appointments to ensure consistency
        this.fetchAppointments();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to reschedule appointment");
      }
    },

    async cancelAppointment(id) {
      if (!confirm("Are you sure you want to cancel this appointment?")) {
        return;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/patient/appointments/${id}/cancel`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Optimistically remove the appointment from local state
        this.appointments = this.appointments.filter(appt => appt.id !== id);
        
        alert("Appointment cancelled successfully!");
        
        // Still fetch appointments to ensure consistency
        this.fetchAppointments();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to cancel appointment");
      }
    },

    async fetchDoctorsBySpecialization(specialization) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_BASE_URL}/api/patient/doctors/available?specialization=${encodeURIComponent(specialization)}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.specializationDoctors = response.data.doctors || [];
      } catch (err) {
        console.error("Error fetching doctors by specialization:", err);
      }
    },
    async startHistoryExport() {
      try {
        const token = localStorage.getItem("token");
        this.exportLoading = true;
        this.exportTaskId = null;
        this.exportTaskStatus = "Starting";
        this.exportResult = null;

        const response = await axios.post(
          `${API_BASE_URL}/api/patient/export/treatment-history`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const taskId = response.data.task_id;
        this.exportTaskId = taskId;
        this.exportTaskStatus = response.data.task_status || "PENDING";

        const pollInterval = setInterval(async () => {
          try {
            const statusResponse = await axios.get(`${API_BASE_URL}/api/patient/export/status/${taskId}`, {
              headers: { Authorization: `Bearer ${token}` }
            });

            this.exportTaskStatus = statusResponse.data.task_status;
            this.exportResult = statusResponse.data.task_result;

            if (["SUCCESS", "FAILURE", "REVOKED"].includes(this.exportTaskStatus)) {
              clearInterval(pollInterval);
              this.exportLoading = false;
              if (this.exportTaskStatus === "SUCCESS") {
                alert("Export completed! Download the CSV file from the link shown.");
              } else {
                alert("Export failed or was cancelled. Please try again later.");
              }
            }
          } catch (err) {
            console.error("Error checking export status:", err);
            clearInterval(pollInterval);
            this.exportLoading = false;
            this.exportTaskStatus = "ERROR";
            alert("Failed to check export status. Please try again.");
          }
        }, 3000);
      } catch (err) {
        this.exportLoading = false;
        this.exportTaskStatus = "ERROR";
        console.error("Error starting export:", err);
        alert(err.response?.data?.error || "Failed to start export");
      }
    },

    closeDoctorsModal() {
      this.showDoctorsModal = false;
      this.specializationDoctors = [];
    },

    filterDoctorsBySpecialization() {
      this.fetchDoctorsBySpecialization(this.selectedSpecialization);
      this.showDoctorsModal = true;
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
  z-index: 1000;
}

.brand {
  position: absolute;
  left: 30px;
  font-size: 22px;
  font-weight: 700;
  color: #1f1f1f;
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

.btn-logout:hover {
  background: #d43d3d;
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

.export-status-row {
  margin-top: 12px;
}

.export-status {
  padding: 10px 14px;
  background: #f0f8ff;
  border: 1px solid #c7def9;
  border-radius: 8px;
  color: #334d6e;
  font-size: 14px;
}

.link-btn {
  text-decoration: underline;
}

.link-btn:hover {
  color: #333;
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

.search-section {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-form {
  display: flex;
  gap: 12px;
  width: 100%;
  flex-wrap: wrap;
}

.search-form .form-control {
  flex: 1;
  min-width: 150px;
}

.search-form .btn {
  min-width: 100px;
}

.btn {
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
  text-transform: lowercase;
  transition: all 0.2s;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
  margin-right: 4px;
}

.btn-blue {
  background: #2f80ed;
  border-color: #2f80ed;
  color: white;
}

.btn-blue:hover {
  background: #1f6fda;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-outline-blue {
  background: #fff;
  color: #2f80ed;
  border: 1px solid #2f80ed;
}

.btn-outline-blue:hover {
  background: #f0f6ff;
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
  padding: 20px;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-warning {
  background: #fff3cd;
  color: #856404;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.alert-danger {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 500px;
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
  font-size: 28px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
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

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: #2f80ed;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.1);
}

.history-item {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  background: #fafafa;
}

.history-item h4 {
  margin: 0 0 8px 0;
  color: #2f80ed;
  font-size: 15px;
}

.history-item p {
  margin: 4px 0;
  font-size: 14px;
  color: #555;
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

  .modal-content {
    max-width: 95%;
  }
}
</style>