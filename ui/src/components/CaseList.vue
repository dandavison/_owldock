<template>
  <!-- class="section" on the following div makes the table rows vertically aligned -->
  <div>
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
          <b-table-column label="Applicant" v-slot="props">
            <applicant :applicant="props.row.applicant"></applicant>
          </b-table-column>

          <b-table-column
            label="Provider"
            v-if="role !== Role.ProviderContact"
            v-slot="props"
          >
            <provider-contact :provider_contact="props.row.provider_contact">
            </provider-contact>
          </b-table-column>

          <b-table-column label="Route" v-slot="props">
            <process :process="props.row.process" :showSteps="false"> </process>
          </b-table-column>
        </b-table>
      </b-tab-item>

      <b-tab-item label="Selected">
        <case v-if="isGenuineCaseObject(selected)" :case_="selected"></case>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { Role } from "../role";
import { CaseSerializer } from "../api-types";
import Applicant from "../components/Applicant.vue";
import Case from "../components/Case.vue";
import ProviderContact from "../components/ProviderContact.vue";
import Process from "../components/Process.vue";
import { processIsNull, providerContactIsNull } from "../factories";

export default Vue.extend({
  props: { role: Number as PropType<Role> },
  components: { Applicant, Case, ProviderContact, Process },
  data() {
    return {
      rows: [] as CaseSerializer[],
      selected: {},
      processIsNull,
      providerContactIsNull,
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
      this.rows = await resp.json();
    },

    navigateToRowDetailView(row: CaseSerializer): void {
      this.$router.push(`/portal/case/${row.id}`);
    },

    // TODO: The 'selected' feature of buefy table seems to be being triggered
    // with an empty/non-genuine Case object.
    isGenuineCaseObject(case_: CaseSerializer): boolean {
      return !!case_.applicant;
    },
  },
});
</script>
