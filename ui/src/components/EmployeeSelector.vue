<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field>
        <b-autocomplete
          type="text"
          v-model="inputEmployeeName"
          placeholder="Select an employee"
          :data="filteredCandidates"
          @select="handleSelect"
          :open-on-focus="true"
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
import Vue from "vue";
import { EmployeeSerializer } from "../api-types";

export default Vue.extend({
  data() {
    return {
      inputEmployeeName: "",
      employees: [] as EmployeeSerializer[],
    };
  },

  computed: {
    filteredCandidates(): EmployeeSerializer[] {
      // TODO: why is this called after selecting with inputEmployeeName === undefined?
      if (!this.inputEmployeeName) {
        return [];
      } else {
        return this.employees.filter((e) => isMatch(e, this.inputEmployeeName));
      }
    },
  },

  mounted() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/client-contact/employees/`)
      .then((resp) => resp.json())
      .then((data) => (this.employees = data));
  },

  methods: {
    handleSelect(employee: EmployeeSerializer) {
      this.$emit("select:employee", employee.id);
    },
  },
});

function isMatch(employee: EmployeeSerializer, name: string): boolean {
  // TODO
  return `${employee.user.first_name} ${employee.user.last_name}`
    .toLowerCase()
    .startsWith(name.toLowerCase());
}
</script>

<style>
.autocomplete .icon.has-text-danger,
.autocomplete .icon.has-text-success {
  display: none;
}
</style>