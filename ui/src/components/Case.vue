<template>
  <div>
    <div class="card" style="overflow: visible">
      <div class="card-content">
        <div class="media">
          <div class="media-left">
            <figure
              v-for="nationality of case_.applicant.nationalities"
              :key="nationality.code"
              class="image is-4x3"
            >
              <img v-bind="makeFlagImgProps(nationality)" />
            </figure>
          </div>

          <div class="media-content">
            <p class="title is-size-6-mobile">
              {{ case_.applicant.user.first_name }}
              {{ case_.applicant.user.last_name }}
            </p>
            <p class="subtitle is-6">
              <a :href="`mailto:${case_.applicant.user.email}`">
                {{ case_.applicant.user.email }}
              </a>
            </p>
          </div>

          <div v-if="haveHostCountry" class="media-right">
            <figure class="image is-4x3">
              <img
                v-bind="makeFlagImgProps(case_.process.route.host_country)"
              />
            </figure>
          </div>
        </div>
        <process
          v-if="haveProcess"
          :process="case_.process"
          :showRoute="false"
          :showSteps="showSteps"
          class="mt-4"
        >
        </process>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// <div v-if="haveProcess" class="">
//   <span class="pl-3">{{ case_.process.route.name }}</span>
// </div>

// <div v-if="haveProviderContact" class="">
//   <p class="title is-4">
//     {{ case_.provider_contact.user.first_name }}
//     {{ case_.provider_contact.user.last_name }}
//   </p>
//   <p class="subtitle is-6">
//     <a :href="`mailto:${case_.provider_contact.user.email}`">
//       {{ case_.provider_contact.user.email }}
//     </a>
//   </p>
// </div>

import Vue, { PropType } from "vue";

import ApplicantSelector from "./ApplicantSelector.vue";
import Process from "./Process.vue";
import { CaseSerializer, ApplicantSerializer } from "../api-types";
import {
  countryIsNull,
  applicantIsNull,
  processIsNull,
  providerContactIsNull,
} from "../factories";
import { makeWavingFlagImgProps as makeFlagImgProps } from "../flags";

export default Vue.extend({
  props: {
    case_: Object as PropType<CaseSerializer>,
    showSteps: { type: Boolean, default: true },
  },

  components: { ApplicantSelector, Process },

  data() {
    return {
      applicant: null as ApplicantSerializer | null,
      makeFlagImgProps,
    };
  },

  computed: {
    haveApplicant(): boolean {
      return !applicantIsNull(this.case_.applicant);
    },

    haveHostCountry(): boolean {
      return !countryIsNull(this.case_.process.route.host_country);
    },

    haveProcess(): boolean {
      let ret = !processIsNull(this.case_.process);
      return ret;
    },

    haveProviderContact(): boolean {
      let ret = !providerContactIsNull(this.case_.provider_contact);
      return ret;
    },
  },

  methods: {
    handleSelectApplicant(applicant: ApplicantSerializer) {
      this.$emit("select:applicant", applicant);
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