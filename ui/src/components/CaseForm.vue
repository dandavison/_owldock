<template>
  <section class="section">
    <form>
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
      <b-field label="Target entry date">
        <b-input v-model="form.target_entry_date"></b-input>
      </b-field>
      <!-- <b-field label="End date of assignment"><b-input></b-input></b-field> -->
      <b-field label="Service required">
        <b-input v-model="form.service"></b-input>
      </b-field>
      <b-field label="Process">
        <b-input v-model="form.process"></b-input>
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
import Vue from "vue";
import Cookies from "js-cookie";

import { makeCountryFlagImgProps } from "../utils";
import { CaseSerializer, CountrySerializer } from "../api-types";

export default Vue.extend({
  props: { employeeId: Number },

  data() {
    return {
      form: {
        employee: this.employeeId,
        type: "",
        status: "UNASSIGNED",
        host_country: "",
        progress: 0,
        process: "",
        service: "",
        target_entry_date: "",
      } as CaseSerializer,
      inputHostCountry: "",
      countries: [] as CountrySerializer[],
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
  },

  methods: {
    handleSelectHostCountry(country: CountrySerializer) {
      this.form.host_country = country;
      this.$emit("select:host-country", country);
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
  },
});

function inputMatchesCountry(
  input: string,
  country: CountrySerializer
): boolean {
  return country.name.toLowerCase().startsWith(input.toLowerCase());
}
</script>
