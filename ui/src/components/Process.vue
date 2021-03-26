<template>
  <div class="card">
    <div class="card-content">
      <h2 class="subtitle">
        <span>
          {{ process.nationality.unicode_flag }}
          <i class="fas fa-long-arrow-alt-right"></i>
          {{ process.route.host_country.unicode_flag }}
        </span>
        <span class="pl-3">{{ process.route.name }}</span>
      </h2>
      <ol class="ml-6">
        <li v-for="step of process.steps" :key="step.sequence_number">
          {{ step.service.name }}
        </li>
      </ol>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessSerializer } from "../api-types";

export default Vue.extend({
  props: { process: Object as PropType<ProcessSerializer> },
});
</script>
