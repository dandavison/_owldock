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
            <applicant :applicant="props.row"></applicant>
          </b-table-column>
        </b-table>
      </b-tab-item>

      <b-tab-item label="Selected">
        <applicant v-if="selected && selected.employer" :applicant="selected">
        </applicant>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { Role } from "../role";
import { Applicant as IApplicant } from "../autogenerated-interfaces/client";
import Applicant from "../components/Applicant.vue";
import http from "../http";

export default Vue.extend({
  props: { role: String as PropType<Role> },
  components: { Applicant },
  data() {
    return {
      rows: [] as IApplicant[],
      selected: {},
    };
  },

  async created(): Promise<void> {
    this.fetchApplicantList();
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
    async fetchApplicantList(): Promise<void> {
      switch (this.role) {
        case Role.ClientContact:
          var url = `${process.env.VUE_APP_SERVER_URL}/api/client-contact/list-applicants/`;
          break;
        case Role.ProviderContact:
          url = `${process.env.VUE_APP_SERVER_URL}/api/provider-contact/list-applicants/`;
          break;
        default:
          return;
      }
      this.rows = (await http.fetchDataOrNull(url)) || [];
    },

    navigateToRowDetailView(row: IApplicant): void {
      this.$router.push(`/portal/applicant/${row.uuid}`);
    },
  },
});
</script>
