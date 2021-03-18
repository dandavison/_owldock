<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiate new work</p>
    <employee-selector @select:employee="(id) => (this.employeeId = id)">
    </employee-selector>
    <immigration-task-form v-if="employeeId" :employeeId="employeeId">
    </immigration-task-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import EmployeeSelector from "../components/EmployeeSelector.vue";
import ImmigrationTaskForm from "../components/ImmigrationTaskForm.vue";

export default Vue.extend({
  components: { EmployeeSelector, ImmigrationTaskForm },
  data() {
    return {
      employeeId: null as number | null,
    };
  },
});
</script>



    
