<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiate new work</p>
    <employee-selector @select:employee="(emp) => (this.employee = emp)">
    </employee-selector>
    <employee v-if="employee" :employee="employee"></employee>
    <case-form v-if="employee" :employeeId="employee.id"> </case-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Employee from "../components/Employee.vue";
import EmployeeSelector from "../components/EmployeeSelector.vue";
import { EmployeeSerializer } from "../api-types";
import CaseForm from "../components/CaseForm.vue";

export default Vue.extend({
  components: { Employee, EmployeeSelector, CaseForm },
  data() {
    return {
      employee: null as EmployeeSerializer | null,
    };
  },
});
</script>
