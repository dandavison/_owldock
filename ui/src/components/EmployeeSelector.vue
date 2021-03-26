<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          v-model="input"
          field="displayName"
          :data="filteredCandidates"
          @select="(employee) => $emit('change:employee', employee)"
          :openOnFocus="true"
          dropdown-position="bottom"
        >
          <template slot-scope="props">
            {{ props.option.displayName }}
          </template>
        </b-autocomplete>
      </b-field>
    </p>
  </div>
</template>

<script lang="ts">
import { inputMatchesString } from "@/utils";
import Vue from "vue";
import { EmployeeSerializer } from "../api-types";

export default Vue.extend({
  props: { label: String },

  data() {
    return {
      input: "",
      employees: [] as EmployeeSerializer[],
    };
  },

  computed: {
    filteredCandidates(): EmployeeSerializer[] {
      return this.employees
        .filter((employee) =>
          inputMatchesString(
            this.input,
            `${employee.user.first_name} ${employee.user.last_name}`
          )
        )
        .map((employee) => {
          const flags = employee.nationalities
            .map((nationality) => nationality.unicode_flag)
            .join(" ");
          return Object.assign(employee, {
            displayName: `${flags} ${employee.user.first_name} ${employee.user.last_name}`,
          });
        });
    },
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/client-contact/employees/`)
      .then((resp) => resp.json())
      .then((data) => (this.employees = data));
  },
});
</script>
