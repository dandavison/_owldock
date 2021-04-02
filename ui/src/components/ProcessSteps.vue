<template>
  <div>
    <h3 class="subtitle is-5 mb-2">Steps</h3>
    <ol class="ml-6">
      <li v-for="step of steps" :key="step.sequence_number">
        {{ step.service.name }}
      </li>
    </ol>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessStepSerializer } from "../api-types";

export default Vue.extend({
  props: { steps: Array as PropType<ProcessStepSerializer[]> },
});
</script>
