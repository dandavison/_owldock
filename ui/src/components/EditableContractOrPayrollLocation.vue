<template>
  <b-select @input="handleInput">
    <option :value="HomeOrHostCountry.None">
      {{ HomeOrHostCountryDisplayName.get(HomeOrHostCountry.Unspecified) }}
    </option>
    <option :value="HomeOrHostCountry.HostCountry">
      {{ HomeOrHostCountryDisplayName.get(HomeOrHostCountry.HostCountry) }}
    </option>
    <option :value="HomeOrHostCountry.HomeCountry">
      {{ HomeOrHostCountryDisplayName.get(HomeOrHostCountry.HomeCountry) }}
    </option>
  </b-select>
</template>

<script lang="ts">
import Vue from "vue";

import {
  HomeOrHostCountry,
  HomeOrHostCountryDisplayName,
} from "@/immigration/rules/base";

import eventBus from "@/event-bus";

export default Vue.extend({
  props: {
    id: String,
  },

  data() {
    return { HomeOrHostCountry, HomeOrHostCountryDisplayName };
  },

  methods: {
    handleInput(value: string): void {
      eventBus.$emit("update:contract-or-payroll-location", value, this.id);
    },
  },
});
</script>
