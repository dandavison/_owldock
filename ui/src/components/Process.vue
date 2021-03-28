<template>
  <div>
    <h2 v-if="showRoute" class="subtitle">
      <span class="pl-3">{{ process.route.name }}</span>
    </h2>
    <process-steps v-if="showSteps" :steps="process.steps"></process-steps>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessSerializer } from "../api-types";
import ProcessSteps from "./ProcessSteps.vue";

export default Vue.extend({
  props: {
    process: Object as PropType<ProcessSerializer>,
    showRoute: { type: Boolean, default: true },
    showSteps: { type: Boolean, default: true },
  },

  components: { ProcessSteps },
});
</script>
