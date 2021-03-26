<template>
  <div>
    <div class="card" style="overflow: visible" @click="handleClick">
      <div class="card-content">
        <div class="media">
          <div class="media-left">
            <figure
              v-for="nationality of case_.employee.nationalities"
              :key="nationality.code"
              class="image is-4x3"
            >
              <img v-bind="makeCountryFlagImgProps(nationality, '64x48')" />
            </figure>
          </div>

          <div class="media-content">
            <p class="title is-4">
              {{ case_.employee.user.first_name }}
              {{ case_.employee.user.last_name }}
            </p>
            <p class="subtitle is-6">
              <a :href="`mailto:${case_.employee.user.email}`">
                {{ case_.employee.user.email }}
              </a>
            </p>
          </div>

          <div v-if="haveHostCountry" class="media-right">
            <figure class="image is-4x3">
              <img
                v-bind="
                  makeCountryFlagImgProps(
                    case_.process.route.host_country,
                    '64x48'
                  )
                "
              />
            </figure>
          </div>
        </div>
      </div>
      <process v-if="haveProcess" :process="case_.process" class="mt-4">
      </process>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import EmployeeSelector from "./EmployeeSelector.vue";
import Process from "./Process.vue";
import { CaseSerializer, EmployeeSerializer } from "../api-types";
import { countryIsNull, processIsNull } from "../factories";
import { makeCountryFlagImgProps } from "../utils";

export default Vue.extend({
  props: { case_: Object as PropType<CaseSerializer> },

  components: { EmployeeSelector, Process },

  data() {
    return {
      employee: null as EmployeeSerializer | null,
      makeCountryFlagImgProps,
    };
  },

  computed: {
    haveHostCountry(): boolean {
      return !countryIsNull(this.case_.process.route.host_country);
    },

    haveProcess(): boolean {
      let ret = !processIsNull(this.case_.process);
      return ret;
    },
  },

  methods: {
    handleSelectEmployee(employee: EmployeeSerializer) {
      this.$emit("select:employee", employee);
    },

    handleClick() {
      this.$emit("select:employee", NullEmployee());
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