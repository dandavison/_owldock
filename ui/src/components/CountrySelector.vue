<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          v-model="input"
          :data="filteredCandidates"
          field="name"
          @select="(country) => $emit('change:country', country)"
          :openOnFocus="true"
        >
          <template slot-scope="props">
            <span class="mr-2">{{ props.option.unicode_flag }}</span>
            <span>{{ props.option.name }}</span>
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

  computed: {
    filteredCandidates(): CountrySerializer[] {
      return this.countries.filter((country) =>
        inputMatchesString(this.input, country.name)
      );
    },
  },
});
</script>
