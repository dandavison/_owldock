<template>
  <div>
    <div class="card" style="overflow: visible">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <applicant :applicant="case_.applicant"></applicant>
          </div>

          <div class="level-item">
            <provider-contact
              v-if="haveProviderContact"
              :provider_contact="case_.provider_contact"
            >
            </provider-contact>
          </div>
        </div>

        <div class="level-right">
          <div class="level-item">
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
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import Applicant from "./Applicant.vue";
import ApplicantSelector from "./ApplicantSelector.vue";
import Process from "./Process.vue";
import { CaseSerializer, ApplicantSerializer } from "../api-types";
import {
  applicantIsNull,
  processIsNull,
  providerContactIsNull,
} from "../factories";
import ProviderContact from "./ProviderContact.vue";

export default Vue.extend({
  props: {
    case_: Object as PropType<CaseSerializer>,
    showSteps: { type: Boolean, default: true },
  },

  components: { Applicant, ApplicantSelector, Process, ProviderContact },

  data() {
    return {
      applicant: null as ApplicantSerializer | null,
    };
  },

  computed: {
    haveApplicant(): boolean {
      return !applicantIsNull(this.case_.applicant);
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

