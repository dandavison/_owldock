<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiate new work</p>
    <employee-selector @select:employee="(id) => (this.employeeId = id)">
    </employee-selector>
    <case-form v-if="employeeId" :employeeId="employeeId">
    </case-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import EmployeeSelector from "../components/EmployeeSelector.vue";
import CaseForm from "../components/CaseForm.vue";

export default Vue.extend({
  components: { EmployeeSelector, CaseForm },
  data() {
    return {
      employeeId: null as number | null,
    };
  },
});
</script>



    
