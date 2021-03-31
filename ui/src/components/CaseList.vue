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

        <b-table-column
          v-if="role !== Role.ProviderContact"
          field="providerContactName"
          label="Provider Contact"
          v-slot="props"
        >
          {{ props.row.providerContactName }}
        </b-table-column>

        <b-table-column
          v-if="role !== Role.ProviderContact"
          label="Provider"
          v-slot="props"
        >
          {{ props.row.provider_contact.provider.name }}
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
import Vue, { PropType } from "vue";
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { Role } from "../role";
import { CaseSerializer } from "../api-types";
import { applicantUnicodeFlags } from "@/methods";

export default Vue.extend({
  props: { role: Number as PropType<Role> },

  data() {
    return {
      rows: [] as CaseSerializer[],
      selected: {},
      Role,
    };
  },

  async created(): Promise<void> {
    this.fetchCaseList();
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
    async fetchCaseList(): Promise<void> {
      switch (this.role) {
        case Role.ClientContact:
          var url = `${process.env.VUE_APP_SERVER_URL}/api/client-contact/list-cases/`;
          break;
        case Role.ProviderContact:
          var url = `${process.env.VUE_APP_SERVER_URL}/api/provider-contact/list-cases/`;
          break;
        case Role.Invalid:
          return;
      }
      const resp = await fetch(url);
      const data = await resp.json();
      this.rows = data.map(this.transformRow);
    },

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
        providerContactName: `${row.provider_contact.user.first_name} ${row.provider_contact.user.last_name}`,
      });
    },
  },
});
</script>
