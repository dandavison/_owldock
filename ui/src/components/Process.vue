<template>
  <div class="card">
    <span class="mr-2">
      {{ process.nationality.unicode_flag }}
      <i class="fas fa-long-arrow-alt-right"></i>
      {{ process.route.host_country.unicode_flag }}
    </span>
    <div v-for="step of process.steps" :key="step.sequence_number" class="card">
      <div class="level">
        <span class="icon">
          <i class="fas fa-briefcase"></i>
        </span>
        <p class="card-header-title">{{ step.service.name }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessSerializer } from "../api-types";

export default Vue.extend({
  props: { process: Object as PropType<ProcessSerializer> },

  created() {
    console.log("Process component: ", this.process);
  },
});
</script>
