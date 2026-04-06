<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Admin Dashboard</h2>
      <button class="btn btn-primary" @click="openAddDoctorModal">Add Doctor</button>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="text-muted">Total Doctors</h6>
            <h3>{{ dashboard.total_doctors || 0 }}</h3>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="text-muted">Total Patients</h6>
            <h3>{{ dashboard.total_patients || 0 }}</h3>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="text-muted">Appointments</h6>
            <h3>{{ dashboard.total_appointments || 0 }}</h3>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="text-muted">Upcoming</h6>
            <h3>{{ dashboard.upcoming_appointments || 0 }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="mb-0">Doctors</h4>
          <input
            v-model="doctorSearch"
            @input="searchDoctors"
            type="text"
            class="form-control w-50"
            placeholder="Search by doctor name or specialization"
          />
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Specialization</th>
                <th>Availability</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doctor in doctors" :key="doctor.id">
                <td>{{ doctor.id }}</td>
                <td>{{ doctor.name }}</td>
                <td>{{ doctor.email }}</td>
                <td>{{ doctor.specialization }}</td>
                <td>{{ doctor.availability || 'Not set' }}</td>
                <td>
                  <button class="btn btn-sm btn-warning me-2" @click="editDoctor(doctor)">
                    Edit
                  </button>
                  <button class="btn btn-sm btn-danger" @click="blacklistDoctor(doctor.id)">
                    Blacklist
                  </button>
                </td>
              </tr>
              <tr v-if="doctors.length === 0">
                <td colspan="6" class="text-center text-muted">No doctors found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="modal fade" id="doctorModal" tabindex="-1" aria-hidden="true" ref="doctorModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Doctor' : 'Add Doctor' }}</h5>
            <button type="button" class="btn-close" @click="closeDoctorModal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="submitDoctorForm">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="doctorForm.username" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="doctorForm.email" type="email" class="form-control" required />
              </div>

              <div class="mb-3" v-if="!isEditMode">
                <label class="form-label">Password</label>
                <input v-model="doctorForm.password" type="password" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Specialization</label>
                <input v-model="doctorForm.specialization" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Availability</label>
                <input v-model="doctorForm.availability" type="text" class="form-control" placeholder='{"monday":"9AM-5PM"}' />
              </div>

              <button type="submit" class="btn btn-success">
                {{ isEditMode ? 'Update Doctor' : 'Add Doctor' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";

export default {
  name: "AdminDashboard",
  data() {
    return {
      dashboard: {},
      doctors: [],
      doctorSearch: "",
      error: "",
      successMessage: "",
      isEditMode: false,
      selectedDoctorId: null,
      doctorModalInstance: null,
      doctorForm: {
        username: "",
        email: "",
        password: "",
        specialization: "",
        availability: ""
      }
    };
  },
  mounted() {
    this.fetchDashboard();
    this.fetchDoctors();
    this.doctorModalInstance = new Modal(this.$refs.doctorModal);
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return {
        Authorization: `Bearer ${token}`
      };
    },

    async fetchDashboard() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/dashboard", {
          headers: this.getAuthHeader()
        });
        this.dashboard = res.data.dashboard;
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to load dashboard";
      }
    },

    async fetchDoctors() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/doctors", {
          headers: this.getAuthHeader()
        });
        this.doctors = res.data.doctors || [];
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to load doctors";
      }
    },

    async searchDoctors() {
      if (!this.doctorSearch.trim()) {
        this.fetchDoctors();
        return;
      }

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/search/doctors?q=${encodeURIComponent(this.doctorSearch)}`,
          { headers: this.getAuthHeader() }
        );
        this.doctors = res.data.doctors || [];
      } catch (err) {
        this.error = err.response?.data?.error || "Doctor search failed";
      }
    },

    openAddDoctorModal() {
      this.isEditMode = false;
      this.selectedDoctorId = null;
      this.doctorForm = {
        username: "",
        email: "",
        password: "",
        specialization: "",
        availability: ""
      };
      this.doctorModalInstance.show();
    },

    editDoctor(doctor) {
      this.isEditMode = true;
      this.selectedDoctorId = doctor.id;
      this.doctorForm = {
        username: doctor.name,
        email: doctor.email,
        password: "",
        specialization: doctor.specialization,
        availability: doctor.availability || ""
      };
      this.doctorModalInstance.show();
    },

    closeDoctorModal() {
      this.doctorModalInstance.hide();
    },

    async submitDoctorForm() {
      this.error = "";
      this.successMessage = "";

      try {
        if (this.isEditMode) {
          await axios.put(
            `http://127.0.0.1:5000/api/admin/doctors/${this.selectedDoctorId}`,
            {
              username: this.doctorForm.username,
              email: this.doctorForm.email,
              specialization: this.doctorForm.specialization,
              availability: this.doctorForm.availability
            },
            { headers: this.getAuthHeader() }
          );
          this.successMessage = "Doctor updated successfully";
        } else {
          await axios.post(
            "http://127.0.0.1:5000/api/admin/doctors",
            this.doctorForm,
            { headers: this.getAuthHeader() }
          );
          this.successMessage = "Doctor added successfully";
        }

        this.closeDoctorModal();
        this.fetchDoctors();
        this.fetchDashboard();
      } catch (err) {
        this.error = err.response?.data?.error || "Doctor form submission failed";
      }
    },

    async blacklistDoctor(doctorId) {
      if (!confirm("Are you sure you want to blacklist this doctor?")) return;

      try {
        await axios.post(
          `http://127.0.0.1:5000/api/admin/doctors/${doctorId}/blacklist`,
          {},
          { headers: this.getAuthHeader() }
        );
        this.successMessage = "Doctor blacklisted successfully";
        this.fetchDoctors();
        this.fetchDashboard();
      } catch (err) {
        this.error = err.response?.data?.error || "Failed to blacklist doctor";
      }
    }
  }
};
</script>