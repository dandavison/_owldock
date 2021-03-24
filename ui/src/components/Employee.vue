<template>
  <div>
    <div
      v-if="employee"
      class="card"
      style="overflow: visible"
      @click="handleClick"
    >
      <div class="card-content">
        <div class="media">
          <div class="media-left">
            <figure class="image is-4x3">
              <img
                v-bind="makeCountryFlagImgProps(employee.home_country, '64x48')"
              />
            </figure>
          </div>

          <div class="media-content">
            <p class="title is-4">
              {{ employee.user.first_name }} {{ employee.user.last_name }}
            </p>
            <p class="subtitle is-6">
              <a :href="`mailto:${employee.user.email}`">
                {{ employee.user.email }}
              </a>
            </p>
          </div>

          <div v-if="hostCountry" class="media-right">
            <figure class="image is-4x3">
              <img
                v-bind="makeCountryFlagImgProps(hostCountry.code, '64x48')"
              />
            </figure>
          </div>
        </div>
      </div>
    </div>
    <employee-selector v-else @select:employee="handleSelect">
    </employee-selector>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { makeCountryFlagImgProps } from "../utils";
import { CountrySerializer, EmployeeSerializer } from "../api-types";
import EmployeeSelector from "./EmployeeSelector.vue";

export default Vue.extend({
  props: { hostCountry: Object as PropType<CountrySerializer> },

  components: { EmployeeSelector },

  data() {
    return {
      employee: null as EmployeeSerializer | null,
      makeCountryFlagImgProps,
    };
  },

  methods: {
    handleSelect(employee: EmployeeSerializer) {
      this.employee = employee;
      this.$emit("select:employee", employee);
    },

    handleClick() {
      this.employee = null;
    },
  },
});
</script>

<style scoped>
a,
a:hover {
  color: currentColor;
}
</style>