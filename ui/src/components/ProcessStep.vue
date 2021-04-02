<template>
  <div>
    <div>
      <div class="card">
        <header class="card-header">
          <p class="card-header-title">
            {{ step.sequence_number }}. {{ step.service.name }}
          </p>
          <button class="card-header-icon" @click="showDetail = !showDetail">
            <span class="icon">
              <i class="fas fa-angle-down"></i>
            </span>
          </button>
        </header>
        <div v-if="showDetail" class="card-content">
          <div class="content">
            [Additional information for step {{ step.sequence_number }}]
          </div>
        </div>
        <footer v-if="showDetail" class="card-footer">
          <a href="#" class="card-footer-item">
            <i class="fas fa-upload"></i> <span class="ml-2">Upload file</span>
          </a>
        </footer>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessStepSerializer } from "../api-types";

export default Vue.extend({
  props: { step: Object as PropType<ProcessStepSerializer> },

  data() {
    return {
      showDetail: false,
    };
  },
});
</script>

<style scoped>
</style>