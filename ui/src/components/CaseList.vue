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
          <b-table-column v-slot="props">
            <case
              style="width: 100%"
              :case_="props.row"
              :showSteps="false"
            ></case>
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
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import BTable from "buefy/src/components/table";
type BTableInstance = InstanceType<typeof BTable>;

import { Role } from "../role";
import { CaseSerializer } from "../api-types";
import Case from "../components/Case.vue";

export default Vue.extend({
  props: { role: Number as PropType<Role> },
  components: { Case },
  data() {
    return {
      rows: [] as CaseSerializer[],
      selected: {},
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
  },
});
</script>
