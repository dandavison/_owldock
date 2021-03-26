<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          v-model="input"
          field="computedName"
          :data="filteredCandidates"
          @select="(employee) => $emit('change:employee', employee)"
          :openOnFocus="true"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        >
          <template slot-scope="props">
            {{ props.option.user.first_name }} {{ props.option.user.last_name }}
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
      // TODO: why is this called with input === undefined?
      if (!this.input) {
        return [];
      }
      return this.employees
        .filter((e) =>
          inputMatchesString(
            this.input,
            `${e.user.first_name} ${e.user.last_name}`
          )
        )
        .map((e) =>
          Object.assign(e, {
            computedName: `${e.user.first_name} ${e.user.last_name}`,
          })
        );
    },
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/client-contact/employees/`)
      .then((resp) => resp.json())
      .then((data) => (this.employees = data));
  },
});
</script>
