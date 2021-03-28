<template>
  <section class="section">
    <p class="m-4 is-size-2">Active cases</p>
    <b-tabs>
      <b-tab-item label="Table">
        <b-table
          ref="table"
          :data="rows"
          :selected.sync="selected"
          focusable
          hoverable
          paginated
          @dblclick="navigateToRowDetailView"
          :per-page="10"
        >
          <b-table-column field="firstName" label="Name" v-slot="props">
            {{ props.row.employee.user.first_name }}
          </b-table-column>

          <b-table-column field="lastName" label="Surname" v-slot="props">
            {{ props.row.employee.user.last_name }}
          </b-table-column>

          <b-table-column
            field="homeCountry"
            label="Home country"
            v-slot="props"
          >
            {{ props.row.employee.home_country }}
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
            {{ props.row.status }}
          </b-table-column>

          <b-table-column field="service" label="Service" v-slot="props">
            {{ props.row.service }}
          </b-table-column>

          <b-table-column field="process" label="Process" v-slot="props">
            {{ props.row.process.name }}
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
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { CaseSerializer } from "../api-types";

export default Vue.extend({
  data() {
    return {
      rows: [],
      selected: {},
    };
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/client-contact/list-cases/`)
      .then((resp) => resp.json())
      .then((data) => (this.rows = data));
  },

  mounted() {
    this.$el.querySelector("table")?.addEventListener("keydown", (event) => {
      if (event.code === "Enter") {
        let table = this.$refs.table as BTableInstance;
        if (table.selected) {
          this.navigateToRowDetailView(table.selected);
        }
      }
    });
  },

  methods: {
    navigateToRowDetailView(row: CaseSerializer): void {
      this.$router.push(`/portal/case/${row.id}`);
    },
  },
});
</script>
