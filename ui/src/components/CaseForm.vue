<template>
  <section class="section">
    <form @submit="fakeSubmit">
      <b-field label="Host country">
        <b-autocomplete
          v-model="inputHostCountry"
          :data="filteredHostCountryCandidates"
          field="name"
          @select="handleSelectHostCountry"
          :openOnFocus="true"
        >
          <template slot-scope="props">
            <span class="mr-2">{{ props.option.unicode_flag }}</span>
            <span>{{ props.option.name }}</span>
          </template>
        </b-autocomplete>
      </b-field>

      <b-field label="Target dates">
        <b-datepicker
          placeholder="Click to select..."
          v-model="dateRange"
          @select="handleSelectDateRange"
          range
        >
        </b-datepicker>
      </b-field>

      <fieldset :disabled="processes.length === 0">
        <b-field label="Route">
          <b-autocomplete
            v-model="inputRoute"
            :data="filteredProcessCandidatesForRouteSelection"
            field="route.name"
            @select="handleSelectProcessForRouteSelection"
            :openOnFocus="true"
          >
            <template slot-scope="props">
              <span class="mr-2">{{ props.option.route.name }}</span>
            </template>
          </b-autocomplete>
        </b-field>
      </fieldset>

      <fieldset :disabled="routeProcesses.length === 0">
        <b-field label="Processes">
          <b-autocomplete
            v-model="inputProcess"
            :data="routeProcesses"
            field="route.name"
            :openOnFocus="true"
          >
            <template slot-scope="props">
              <span class="mr-2">{{ props.option.route.name }}</span>
            </template>
          </b-autocomplete>
        </b-field>
      </fieldset>

      <fieldset :disabled="!isValid()">
        <div class="field is-grouped pt-4">
          <div class="control">
            <button class="button is-link" @click="handleSubmit">Submit</button>
          </div>
        </div>
      </fieldset>
    </form>
  </section>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import Cookies from "js-cookie";

import { makeCountryFlagImgProps } from "../utils";
import {
  CaseSerializer,
  CountrySerializer,
  EmployeeSerializer,
  ProcessSerializer,
} from "../api-types";

export default Vue.extend({
  props: { employee: Object as PropType<EmployeeSerializer> },

  data() {
    return {
      form: {
        employee: this.employee,
        process: {},
        target_entry_date: "",
        target_exit_date: "",
      } as CaseSerializer,
      dateRange: [] as string[],
      inputHostCountry: "",
      inputRoute: "",
      inputProcess: "",
      countries: [] as CountrySerializer[],
      // All processes matching country, employee nationalities & home country, dates
      processes: [] as ProcessSerializer[],
      // Subset of those processes matching selected route
      routeProcesses: [] as ProcessSerializer[],
      makeCountryFlagImgProps,
    };
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/countries/`)
      .then((resp) => resp.json())
      .then((data) => (this.countries = data));
  },

  computed: {
    /// Return countries matching input country name fragment.
    filteredHostCountryCandidates(): CountrySerializer[] {
      return this.countries.filter((country) =>
        inputMatchesString(this.inputHostCountry, country.name)
      );
    },

    /// Return processes with route matching input route name fragment,
    /// uniquified on route name.
    filteredProcessCandidatesForRouteSelection(): ProcessSerializer[] {
      const processes = [];
      const seen = new Set();
      for (let process of this.processes) {
        let name = process.route.name;
        if (inputMatchesString(this.inputRoute, name)) {
          if (!seen.has(name)) {
            seen.add(name);
            processes.push(process);
          }
        }
      }
      return processes;
    },
  },

  methods: {
    handleSelectHostCountry(country: CountrySerializer) {
      if (!country) {
        // FIXME: why
        console.log("ERROR: country is", JSON.stringify(country));
        return;
      }
      this.$emit("select:host-country", country);
      if (this.employee.nationalities) {
        const nationalityCodes = this.employee.nationalities.map(
          (country) => country.code
        );
        fetch(
          `${process.env.VUE_APP_SERVER_URL}/api/processes/?host_country=${
            country.code
          }&nationalities=${nationalityCodes.join(",")}`
        )
          .then((resp) => resp.json())
          .then((data) => (this.processes = data));
      }
    },

    handleSelectProcessForRouteSelection(process: ProcessSerializer): void {
      if (!process) {
        // FIXME: why
        console.log("ERROR: process is", JSON.stringify(process));
        return;
      }
      this.routeProcesses = this.processes.filter(
        (p) => p.route.name === process.route.name
      );
    },

    handleSelectDateRange(): void {
      this.form.target_entry_date = this.dateRange[0] || "";
      this.form.target_exit_date = this.dateRange[1] || "";
    },

    isValid(): boolean {
      // TODO
      const emptyValues = Object.values(this.form).filter(
        (val) => `${val}`.length === 0
      );
      return emptyValues.length === 0;
    },

    handleSubmit(): void {
      if (!this.isValid()) {
        console.log("Not submitting: form data is not valid");
        return;
      }

      const headers = {
        "Content-Type": "application/json",
      } as any;
      const csrf_token = Cookies.get("csrftoken");
      if (csrf_token) {
        headers["X-CSRFToken"] = csrf_token;
      }

      fetch(`${process.env.VUE_APP_SERVER_URL}/api/cases/`, {
        method: "POST",
        headers,
        body: JSON.stringify(this.form),
      });
    },

    fakeSubmit(event: Event): void {
      // FIXME: prevent submit correctly
      console.log("fakeSubmit", event);
      event.stopPropagation();
      event.preventDefault();
    },
  },
});

function inputMatchesString(input: string, string: string): boolean {
  return string.toLowerCase().startsWith(input.toLowerCase());
}
</script>
