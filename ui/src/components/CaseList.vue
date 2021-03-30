<template>
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
        :per-page="50"
      >
        <b-table-column
          field="applicantNameData"
          label="Applicant"
          v-slot="props"
        >
          {{ props.row.applicantNameDisplay }}
        </b-table-column>

        <b-table-column
          field="applicantNationalitiesData"
          label="Nationalities"
          v-slot="props"
        >
          {{ props.row.applicantNationalitiesDisplay }}
        </b-table-column>

        <b-table-column
          field="process.route.host_country.name"
          label="Host country"
          v-slot="props"
        >
          {{ props.row.process.route.host_country.unicode_flag }}
        </b-table-column>

        <b-table-column label="Process" v-slot="props">
          {{ props.row.process.route.name }}
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
          label="Target entry date"
          v-slot="props"
        >
          {{ new Date(props.row.target_entry_date).toDateString() }}
        </b-table-column>

        <b-table-column field="progress" label="Progress" v-slot="props">
          0 / {{ props.row.process.steps.length }}
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
</template>

<script lang="ts">
import Vue from "vue";
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { CaseSerializer } from "../api-types";
import { applicantUnicodeFlags } from "@/methods";

export default Vue.extend({
  data() {
    return {
      rows: [] as CaseSerializer[],
      selected: {},
    };
  },

  async created(): Promise<void> {
    const resp = await fetch(
      `${process.env.VUE_APP_SERVER_URL}/api/client-contact/list-cases/`
    );
    const data = await resp.json();
    this.rows = data.map(this.transformRow);
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

    transformRow(row: CaseSerializer): CaseSerializer {
      const applicantName = `${row.applicant.user.first_name} ${row.applicant.user.last_name}`;
      return Object.assign(row, {
        applicantNameData: applicantName,
        applicantNameDisplay: applicantName,
        applicantNationalitiesData: row.applicant.nationalities.join(", "),
        applicantNationalitiesDisplay: applicantUnicodeFlags(row.applicant),
      });
    },
  },
});
</script>
