<template>
  <process-steps-gantt v-if="process" :process="process" :editable="true" />
</template>

<script lang="ts">
import Vue from "vue";

import ProcessStepsGantt from "@/components/ProcessStepsGantt.vue";
import { ProcessRuleSet as IProcessRuleSet } from "@/autogenerated-interfaces/immigration";
import http from "../http";

export default Vue.extend({
  props: { id: String },
  components: { ProcessStepsGantt },
  data() {
    return {
      process: null as IProcessRuleSet | null,
    };
  },

  async created(): Promise<void> {
    this.process = (await http.fetchDataOrNull(
      `/api/process/${this.id}`
    )) as IProcessRuleSet;
  },
});
</script>
