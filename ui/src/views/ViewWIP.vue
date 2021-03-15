<template>
  <section class="section">
    <p class="m-4 is-size-2">Work in progress</p>
    <b-tabs>
      <b-tab-item label="Table">
        <b-table
          :data="rows"
          :selected.sync="selected"
          focusable
          hoverable
          paginated
          :per-page="10"
        >
          <b-table-column field="firstName" label="Name" v-slot="props">
            {{ props.row.person__first_name }}
          </b-table-column>
          <b-table-column field="lastName" label="Surname" v-slot="props">
            {{ props.row.person__last_name }}
          </b-table-column>
          <b-table-column
            field="homeCountry"
            label="Home country"
            v-slot="props"
          >
            {{ props.row.person__home_country }}
          </b-table-column>
          <b-table-column
            field="hostCountry"
            label="Host country"
            v-slot="props"
          >
            {{ props.row.host_country }}
          </b-table-column>
          <b-table-column
            field="dateInitiated"
            label="Date initiated"
            v-slot="props"
          >
            {{ new Date(props.row.created_at).toDateString() }}
          </b-table-column>
          <b-table-column
            field="targetDate"
            label="Target date to enter"
            v-slot="props"
          >
            {{ new Date(props.row.target_entry_date).toDateString() }}
          </b-table-column>
          <b-table-column field="progress" label="Progress" v-slot="props">
            {{ props.row.progress }}%
          </b-table-column>
          <b-table-column
            field="currentStatus"
            label="Current status"
            v-slot="props"
          >
            {{ props.row.current_status }}
          </b-table-column>
          <b-table-column field="service" label="Service" v-slot="props">
            {{ props.row.service }}
          </b-table-column>
          <b-table-column field="caseType" label="Case type" v-slot="props">
            {{ props.row.case_type }}
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
    return {
      rows: [],
      selected: {},
    };
  },

  created() {
    fetch("http://localhost:8000/api/person-immigration-tasks/")
      .then((resp) => resp.json())
      .then((data) => (this.rows = data));
  },
});
</script>
