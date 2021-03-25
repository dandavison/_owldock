<template>
  <section class="section">
    <p class="m-4 is-size-2">New case</p>
    <case-header
      @select:employee="(employee) => (this.employee = employee)"
      :hostCountry="hostCountry"
    >
    </case-header>
    <case-form
      v-if="employee"
      :employee="employee"
      @select:host-country="(country) => (this.hostCountry = country)"
    >
    </case-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import CaseHeader from "../components/CaseHeader.vue";
import EmployeeSelector from "../components/EmployeeSelector.vue";
import { CountrySerializer, EmployeeSerializer } from "../api-types";
import CaseForm from "../components/CaseForm.vue";

export default Vue.extend({
  components: { CaseHeader, EmployeeSelector, CaseForm },
  data() {
    return {
      employee: null as EmployeeSerializer | null,
      hostCountry: null as CountrySerializer | null,
    };
  },
});
</script>
