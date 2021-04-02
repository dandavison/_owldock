<template>
  <div>
    <div class="card" style="overflow: visible">
      <div class="card-content">
        <applicant :applicant="case_.applicant"></applicant>

        <provider-contact
          v-if="haveProviderContact"
          :provider_contact="case_.provider_contact"
        >
        </provider-contact>

        <process
          v-if="haveProcess"
          :process="case_.process"
          :showSteps="showSteps"
        >
        </process>
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
      return !processIsNull(this.case_.process);
    },

    haveProviderContact(): boolean {
      return !providerContactIsNull(this.case_.provider_contact);
    },
  },

  methods: {
    handleSelectApplicant(applicant: ApplicantSerializer) {
      this.$emit("select:applicant", applicant);
    },
  },
});
</script>

