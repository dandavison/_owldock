<template>
  <section class="section">
    <p class="m-4 is-size-2">New case</p>
    <employee
      @select:employee="(employee) => (this.employee = employee)"
      :hostCountry="hostCountry"
    ></employee>
    <case-form
      v-if="employee"
      :employeeId="employee.id"
      @select:host-country="(country) => (this.hostCountry = country)"
    >
    </case-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Employee from "../components/Employee.vue";
import EmployeeSelector from "../components/EmployeeSelector.vue";
import { CountrySerializer, EmployeeSerializer } from "../api-types";
import CaseForm from "../components/CaseForm.vue";

export default Vue.extend({
  components: { Employee, EmployeeSelector, CaseForm },
  data() {
    return {
      employee: null as EmployeeSerializer | null,
      hostCountry: null as CountrySerializer | null,
    };
  },
});
</script>
