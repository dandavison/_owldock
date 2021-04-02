<template>
  <div>
    <h3 class="subtitle is-5 mb-2">Steps</h3>
    <ul>
      <li v-for="step of steps" :key="step.sequence_number">
        <process-step :step="step"></process-step>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import ProcessStep from "./ProcessStep.vue";
import { ProcessStepSerializer } from "../api-types";

export default Vue.extend({
  components: { ProcessStep },

  props: { steps: Array as PropType<ProcessStepSerializer[]> },
});
</script>
