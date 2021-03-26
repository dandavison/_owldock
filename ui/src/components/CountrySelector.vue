<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          ref="autocomplete"
          v-model="input"
          :data="filteredCandidates"
          field="name"
          @select="(country) => $emit('change:country', country)"
          :openOnFocus="true"
          dropdown-position="bottom"
          max-height="100vh"
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
import Vue from "vue";
import { CountrySerializer } from "../api-types";
import { inputMatchesString } from "../utils";
import { dismissMobileKeyboardOnDropdownScroll } from "../componentUtils";

export default Vue.extend({
  props: { label: String },

  data() {
    return {
      countries: [] as CountrySerializer[],
      input: "",
    };
  },

  created() {
    fetch(`${process.env.VUE_APP_SERVER_URL}/api/countries/`)
      .then((resp) => resp.json())
      .then((data) => (this.countries = data));
  },

  mounted() {
    dismissMobileKeyboardOnDropdownScroll(this, "autocomplete");
  },

  computed: {
    filteredCandidates(): CountrySerializer[] {
      return this.countries
        .filter((country) => inputMatchesString(this.input, country.name))
        .map((country) => {
          return Object.assign(country, {
            displayName: `${country.unicode_flag} ${country.name}`,
          });
        });
    },
  },
});
</script>
