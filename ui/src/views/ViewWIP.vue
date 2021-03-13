<template>
  <section class="section">
    <p class="m-4 is-size-2">Work in progress</p>
    <b-tabs>
      <b-tab-item label="Table">
        <b-table :data="rows" :selected.sync="selected">
          <b-table-column field="firstName" label="Name" v-slot="props">
            {{ props.row.firstName }}
          </b-table-column>
          <b-table-column field="lastName" label="Surname" v-slot="props">
            {{ props.row.lastName }}
          </b-table-column>
          <b-table-column
            field="homeCountry"
            label="Home country"
            v-slot="props"
          >
            {{ props.row.homeCountry }}
          </b-table-column>
          <b-table-column
            field="hostCountry"
            label="Host country"
            v-slot="props"
          >
            {{ props.row.hostCountry }}
          </b-table-column>
          <b-table-column
            field="dateInitiated"
            label="Date initiated"
            v-slot="props"
          >
            {{ props.row.dateInitiated }}
          </b-table-column>
          <b-table-column
            field="targetDate"
            label="Target date to enter"
            v-slot="props"
          >
            {{ props.row.targetDate }}
          </b-table-column>
          <b-table-column field="progress" label="Progress" v-slot="props">
            {{ props.row.progress }}
          </b-table-column>
          <b-table-column
            field="currentStatus"
            label="Current status"
            v-slot="props"
          >
            {{ props.row.currentStatus }}
          </b-table-column>
          <b-table-column field="service" label="Service" v-slot="props">
            {{ props.row.service }}
          </b-table-column>
          <b-table-column field="caseType" label="Case type" v-slot="props">
            {{ props.row.caseType }}
          </b-table-column>
        </b-table>
      </b-tab-item>

      <b-tab-item label="Selected">
        <ul>
          <li>Milestones completed</li>
          <li>Documents</li>
          <li>Exchange documents</li>
          <li>Send notification / message to provider</li>
        </ul>
      </b-tab-item>
    </b-tabs>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    const rows = [
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
    ];
    return {
      selected: rows[0],
      rows: rows,
    };
  },
});
</script>
