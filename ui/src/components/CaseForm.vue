<template>
  <section class="section">
    <form @submit="fakeSubmit">
      <b-field label="Host country">
        <b-autocomplete
          v-model="inputHostCountry"
          :data="filteredHostCountryCandidates"
          :openOnFocus="true"
          @select="handleSelectHostCountry"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        >
          <template slot-scope="props">
            <span class="mr-2">{{ props.option.unicode_flag }}</span>
            <span>{{ props.option.name }}</span>
          </template>
        </b-autocomplete>
      </b-field>
      <b-field label="Route">
        <b-autocomplete
          v-model="inputRoute"
          :data="filteredRouteCandidates"
          :openOnFocus="true"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        >
          <template slot-scope="props">
            <span class="mr-2">{{ props.option.name }}</span>
            <span class="mr-2">
              {{ props.option.nationality.unicode_flag }}
            </span>
            <span><i class="fas fa-long-arrow-alt-right"></i></span>
            <span> {{ props.option.host_country.unicode_flag }} </span>
          </template>
        </b-autocomplete>
      </b-field>
      <b-field label="Target entry date">
        <b-input v-model="form.target_entry_date"></b-input>
      </b-field>
      <!-- <b-field label="End date of assignment"><b-input></b-input></b-field> -->
      <b-field label="Service required">
        <b-input v-model="form.service"></b-input>
      </b-field>
      <div class="field is-grouped">
        <div class="control">
          <button class="button is-link" @click="handleSubmit">Submit</button>
        </div>
        <div class="control">
          <button class="button is-link is-light">Cancel</button>
        </div>
      </div>
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
  RouteSerializer,
} from "../api-types";

export default Vue.extend({
  props: { employee: Object as PropType<EmployeeSerializer> },

  data() {
    return {
      form: {
        employee: this.employee,
        host_country: {},
        route: {},
        target_entry_date: "",
      } as CaseSerializer,
      inputHostCountry: "",
      inputRoute: "",
      countries: [] as CountrySerializer[],
      routes: [] as RouteSerializer[],
      makeCountryFlagImgProps,
    };
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/countries/`)
      .then((resp) => resp.json())
      .then((data) => (this.countries = data));
  },

  computed: {
    filteredHostCountryCandidates(): CountrySerializer[] {
      // TODO: why is this called after selecting with inputEmployeeName === undefined?
      if (!this.inputHostCountry) {
        return [];
      } else {
        return this.countries.filter((country) =>
          inputMatchesCountry(this.inputHostCountry, country)
        );
      }
    },

    filteredRouteCandidates(): RouteSerializer[] {
      // TODO: why is this called after selecting with inputEmployeeName === undefined?
      if (!this.inputRoute) {
        return [];
      } else {
        return this.routes.filter((route) =>
          inputMatchesRoute(this.inputRoute, route)
        );
      }
    },
  },

  methods: {
    handleSelectHostCountry(country: CountrySerializer) {
      this.form.host_country = country;
      this.$emit("select:host-country", country);
      if (this.employee.nationalities) {
        const nationalityCodes = this.employee.nationalities.map(
          (country) => country.code
        );
        fetch(
          `${process.env.VUE_APP_SERVER_URL}/api/routes/?host_country=${
            country.code
          }&nationalities=${nationalityCodes.join(",")}`
        )
          .then((resp) => resp.json())
          .then((data) => (this.routes = data));
      }
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
      console.log("fakeSubmit", event);
      event.stopPropagation();
      event.preventDefault();
    },
  },
});

function inputMatchesCountry(
  input: string,
  country: CountrySerializer
): boolean {
  return country.name.toLowerCase().startsWith(input.toLowerCase());
}

function inputMatchesRoute(input: string, route: RouteSerializer): boolean {
  return route.name.toLowerCase().startsWith(input.toLowerCase());
}
</script>
