<template>
  <div class="doctor-dashboard">
    <!-- top nabar -->
    <div class="top-navbar">
      <div class="nav-left">MediZentrum</div>
      <div class="nav-center">Doctor Dashboard</div>
      <div class="nav-right">
        <button class="btn btn-logout" @click="logout">Logout</button>
      </div>
    </div>

    <div class="page-wrapper">
      <!-- alerts -->
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

      <!-- welcome card -->
      <section class="top-card">
        <div class="welcome-section">
          <h1 class="welcome-title">Welcome {{ doctor.name }}</h1>
          <p class="doctor-info">{{ doctor.specialization }}</p>
        </div>
        <button class="btn btn-green large-btn" @click="openAvailabilityModal">
          Set Availability
        </button>
      </section>

      <!-- upcoming appointments  -->
      <section class="content-card">
        <h2 class="section-title">Upcoming Appointments ({{ appointments.length }})</h2>

        <div class="table-shell">
          <table class="dashboard-table">
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Patient Name</th>
                <th>Date & Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(appt, index) in appointments" :key="appt.id">
                <td>{{ 1001 + index }}</td>
                <td>{{ appt.patient_name }}</td>
                <td>{{ appt.date }} {{ appt.time }}</td>
                <td><span class="badge badge-booked">{{ appt.status }}</span></td>
                <td class="action-group">
                  <button class="btn btn-blue btn-sm" @click="openTreatmentModal(appt)">
                    Complete & Add Treatment
                  </button>
                  <button class="btn btn-red-outline btn-sm" @click="cancelAppointment(appt.id)">
                    Cancel
                  </button>
                </td>
              </tr>
              <tr v-if="appointments.length === 0">
                <td colspan="5" style="text-align: center; color: #999; padding: 20px;">
                  No upcoming appointments
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- assigned patients -->
      <section class="content-card">
        <h2 class="section-title">Assigned Patients ({{ patients.length }})</h2>

        <div class="patient-list">
          <div v-for="patient in patients" :key="patient.id" class="patient-row">
            <div class="patient-info">
              <span class="patient-name">{{ patient.name }}</span>
              <span class="patient-email">{{ patient.email }}</span>
            </div>
            <button class="btn btn-blue" @click="viewPatientHistory(patient.id)">
              View History
            </button>
          </div>
          <div v-if="patients.length === 0" style="text-align: center; color: #999; padding: 20px;">
            No assigned patients
          </div>
        </div>
      </section>

      <!-- pateint history modal-->
      <div v-if="showPatientHistoryModal" class="modal-overlay" @click="closePatientHistoryModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>Patient History - {{ (selectedHistoryPatient && selectedHistoryPatient.name) || 'Patient' }}</h3>
            <button class="close-btn" @click="closePatientHistoryModal">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="patientHistory.length === 0" class="empty-cell">No treatment history found.</div>
            <div v-for="item in patientHistory" :key="item.appointment_id" class="history-item">
              <h4>{{ item.date }} {{ item.time }}</h4>
              <div class="form-group">
                <label>Diagnosis:</label>
                <textarea v-model="item.diagnosis" rows="3" class="form-textarea"></textarea>
              </div>
              <div class="form-group">
                <label>Prescription:</label>
                <textarea v-model="item.prescription" rows="3" class="form-textarea"></textarea>
              </div>
              <div class="form-group">
                <label>Notes:</label>
                <textarea v-model="item.notes" rows="2" class="form-textarea"></textarea>
              </div>
              <div class="modal-actions">
                <button class="btn btn-outline-gray" @click="closePatientHistoryModal">Close</button>
                <button class="btn btn-green" @click="updateHistoryItem(item)">Save Changes</button>
              </div>
              <hr />
            </div>
          </div>
        </div>
      </div>

      <!-- treatment modal -->
      <div v-if="showTreatmentModal" class="modal-overlay" @click="closeTreatmentModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>Add Treatment Record</h3>
            <button class="close-btn" @click="closeTreatmentModal">&times;</button>
          </div>

          <div class="modal-body">
            <p style="color: #666; margin-bottom: 16px;">
              <strong>Patient:</strong> {{ selectedAppointment?.patient_name }}<br>
              <strong>Date:</strong> {{ selectedAppointment?.date }}
            </p>

            <div class="form-group">
              <label>Diagnosis: <span style="color: red;">*</span></label>
              <textarea v-model="treatmentForm.diagnosis" placeholder="Enter diagnosis" rows="3" class="form-textarea"></textarea>
            </div>

            <div class="form-group">
              <label>Prescription:</label>
              <textarea v-model="treatmentForm.prescription" placeholder="Enter prescription details" rows="3" class="form-textarea"></textarea>
            </div>

            <div class="form-group">
              <label>Notes:</label>
              <textarea v-model="treatmentForm.notes" placeholder="Additional notes" rows="2" class="form-textarea"></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline-gray" @click="closeTreatmentModal">Cancel</button>
            <button class="btn btn-green" @click="submitTreatment">Save & Mark Complete</button>
          </div>
        </div>
      </div>

      <!-- availability modal -->
      <div v-if="showAvailabilityModal" class="modal-overlay" @click="closeAvailabilityModal">
        <div class="modal-box modal-lg" @click.stop>
          <div class="modal-header">
            <h3>Set Your Weekly Availability</h3>
            <button class="close-btn" @click="closeAvailabilityModal">&times;</button>
          </div>

          <div class="modal-body availability-body">
            <div v-for="(config, day) in availabilityForm" :key="day" class="availability-row">
              <div class="day-name" style="width: auto; min-width: 140px;">{{ config.label || (day.charAt(0).toUpperCase() + day.slice(1)) }}</div>
              <label class="checkbox-label">
                <input type="checkbox" v-model="config.available" />
                Available
              </label>
              <div v-if="config.available" class="time-inputs">
                <input type="time" v-model="config.start_time" />
                <span>to</span>
                <input type="time" v-model="config.end_time" />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline-gray" @click="closeAvailabilityModal">Cancel</button>
            <button class="btn btn-green" @click="submitAvailability">Save Availability</button>
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
  name: "DoctorDashboard",
  data() {
    return {
      doctor: {
        id: null,
        name: "",
        email: "",
        specialization: ""
      },
      appointments: [],
      patients: [],
      loading: true,
      error: "",
      successMessage: "",
      
      // Modals
      showTreatmentModal: false,
      showAvailabilityModal: false,
      showPatientHistoryModal: false,
      patientHistory: [],
      selectedHistoryPatient: null,
      selectedAppointment: null,
      
      // Form data
      treatmentForm: {
        diagnosis: "",
        prescription: "",
        notes: ""
      },
      availabilityForm: {
        monday: { available: true, start_time: "09:00", end_time: "17:00" },
        tuesday: { available: true, start_time: "09:00", end_time: "17:00" },
        wednesday: { available: true, start_time: "09:00", end_time: "17:00" },
        thursday: { available: true, start_time: "09:00", end_time: "17:00" },
        friday: { available: true, start_time: "09:00", end_time: "17:00" },
        saturday: { available: false, start_time: "09:00", end_time: "17:00" },
        sunday: { available: false, start_time: "09:00", end_time: "17:00" }
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

        
        const dashRes = await axios.get(`${API_BASE_URL}/api/doctor/dashboard`, { headers });
        this.doctor = dashRes.data.doctor || {};
        this.appointments = dashRes.data.upcoming_appointments || [];
        this.patients = dashRes.data.assigned_patients || [];

        this.error = "";
        this.loading = false;
      } catch (err) {
        if (err.response?.status === 403) {
          this.error = err.response.data.error || "Access denied";
          
          setTimeout(() => {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
          }, 3000);
        } else {
          this.error = "Failed to load dashboard data";
        }
        this.loading = false;
      }
    },

    openTreatmentModal(appointment) {
      this.selectedAppointment = appointment;
      this.treatmentForm = { diagnosis: "", prescription: "", notes: "" };
      this.showTreatmentModal = true;
    },

    closeTreatmentModal() {
      this.showTreatmentModal = false;
      this.selectedAppointment = null;
    },

    async submitTreatment() {
      if (!this.treatmentForm.diagnosis) {
        alert("Diagnosis is required");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/doctor/appointments/${this.selectedAppointment.id}/complete`,
          this.treatmentForm,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.successMessage = "Treatment recorded successfully!";
        this.closeTreatmentModal();
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        alert(err.response?.data?.error || "Failed to record treatment");
      }
    },

    async cancelAppointment(appointmentId) {
      if (!confirm("Are you sure you want to cancel this appointment?")) return;

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/doctor/appointments/${appointmentId}/cancel`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.successMessage = "Appointment cancelled successfully!";
        this.fetchDashboardData();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        alert(err.response?.data?.error || "Failed to cancel appointment");
      }
    },

    openAvailabilityModal() {
      const newForm = {};
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      for (let i = 0; i < 7; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const dateStr = String(d.getDate()).padStart(2, '0');
        const value = `${year}-${month}-${dateStr}`; // "YYYY-MM-DD"
        
        const options = { weekday: 'short', month: 'short', day: 'numeric' };
        let label = d.toLocaleDateString(undefined, options);
        if (i === 0) label = "Today, " + label;
        else if (i === 1) label = "Tmw, " + label;
        
        const dayOfWeek = d.getDay();
        const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

        newForm[value] = {
          available: !isWeekend,
          start_time: "09:00",
          end_time: "17:00",
          label: label
        };
      }
      this.availabilityForm = newForm;
      this.showAvailabilityModal = true;
    },

    closeAvailabilityModal() {
      this.showAvailabilityModal = false;
    },

    async submitAvailability() {
      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/doctor/availability`,
          this.availabilityForm,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.successMessage = "Availability updated successfully!";
        this.closeAvailabilityModal();
        setTimeout(() => { this.successMessage = ""; }, 3000);
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update availability");
      }
    },

    async viewPatientHistory(patientId) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `${API_BASE_URL}/api/doctor/patient/${patientId}/history`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.selectedHistoryPatient = response.data.patient || null;
        this.patientHistory = (response.data.history || []).map(item => ({
          ...item,
          diagnosis: item.diagnosis || "",
          prescription: item.prescription || "",
          notes: item.notes || ""
        }));
        this.showPatientHistoryModal = true;
      } catch (err) {
        alert(err.response?.data?.error || "Failed to load patient history");
      }
    },

    async closePatientHistoryModal() {
      this.showPatientHistoryModal = false;
      this.patientHistory = [];
      this.selectedHistoryPatient = null;
    },

    async updateHistoryItem(item) {
      if (!item.diagnosis) {
        alert("Diagnosis is required to save history updates.");
        return;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          `${API_BASE_URL}/api/doctor/appointments/${item.appointment_id}/complete`,
          {
            diagnosis: item.diagnosis,
            prescription: item.prescription,
            notes: item.notes
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        alert("History updated successfully!");
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update history");
      }
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

.page-wrapper {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 30px;
}

/* alerts */
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

/* cards */
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
  gap: 20px;
}

.welcome-section {
  flex: 1;
}

.welcome-title {
  margin: 0 0 6px;
  font-size: 26px;
  font-weight: 700;
  color: #1f1f1f;
}

.doctor-info {
  margin: 0;
  font-size: 14px;
  color: #666;
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

/*  tables */
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

.dashboard-table tbody tr:hover {
  background: #f9f9f9;
}

.action-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* patient list */
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
  transition: background 0.2s;
}

.patient-row:hover {
  background: #f9f9f9;
}

.patient-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.patient-name {
  color: #222;
  font-size: 16px;
  font-weight: 600;
}

.patient-email {
  color: #999;
  font-size: 12px;
}

/* buttons */
.btn {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-transform: lowercase;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.large-btn {
  padding: 10px 18px;
}

.btn-green {
  background: #16c341;
  color: white;
}

.btn-green:hover {
  background: #11ad39;
}

.btn-blue {
  background: #2f80ed;
  color: white;
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

.btn-outline-gray {
  background: white;
  color: #565656;
  border: 1px solid #cfcfcf;
}

.btn-outline-gray:hover {
  background: #f5f5f5;
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

/* modal */
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
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-box.modal-lg {
  max-width: 600px;
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

.availability-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.availability-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 6px;
}

.day-name {
  width: 80px;
  font-weight: 600;
  color: #333;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  white-space: nowrap;
}

.checkbox-label input {
  cursor: pointer;
}

.time-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.time-inputs input {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 13px;
}

.time-inputs span {
  font-size: 13px;
  color: #999;
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

.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}

.form-textarea:focus {
  outline: none;
  border-color: #2f80ed;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .top-card {
    flex-direction: column;
    align-items: flex-start;
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

  .action-group {
    width: 100%;
  }

  .availability-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .time-inputs {
    margin-left: 0;
    width: 100%;
  }
}
</style>