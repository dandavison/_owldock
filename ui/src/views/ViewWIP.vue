<template>
  <section class="section">
    <p class="m-4 is-size-2">Work in progress</p>
    <b-table :data="rows" :columns="columns"> </b-table>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      rows: [
        {
          firstName: "John",
          lastName: "Smith",
          homeCountry: "USA",
          hostCountry: "Greece",
          dateInitiated: "01/01/2021",
          targetDate: "01/03/2021",
          progress: "50%",
          currentStatus: "Application Submitted",
          service: "Immigration",
          caseType: "Initial",
        },
      ],
      columns: [
        { field: "firstName", label: "Name" },
        { field: "lastName", label: "Surname" },
        { field: "homeCountry", label: "Home country" },
        { field: "hostCountry", label: "Host country" },
        { field: "dateInitiated", label: "Date initiated" },
        { field: "targetDate", label: "Target date to enter" },
        { field: "progress", label: "Progress" },
        { field: "currentStatus", label: "Current status" },
        { field: "service", label: "Service" },
        { field: "caseType", label: "Case type" },
      ],
    };
  },
});
</script>
