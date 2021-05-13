<template>
  <b-select @input="handleInput">
    <option :value="HomeOrHostCountry.Unspecified">
      {{ HomeOrHostCountry.Unspecified }}
    </option>
    <option :value="HomeOrHostCountry.HostCountry">
      {{ HomeOrHostCountry.HostCountry }}
    </option>
    <option :value="HomeOrHostCountry.HomeCountry">
      {{ HomeOrHostCountry.HomeCountry }}
    </option>
  </b-select>
</template>

<script lang="ts">
import Vue from "vue";

import { HomeOrHostCountry } from "@/immigration/rules/base";

import eventBus from "@/event-bus";

export default Vue.extend({
  props: {
    id: String,
  },

  data() {
    return { HomeOrHostCountry };
  },

  methods: {
    handleInput(value: string): void {
      eventBus.$emit("update:contract-or-payroll-location", value, this.id);
    },
  },
});
</script>
