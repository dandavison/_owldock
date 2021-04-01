<template>
  <div class="media">
    <div class="media-left">
      <figure class="image is-4x3">
        <img v-bind="makeFlagImgProps(process.route.host_country)" />
      </figure>
    </div>

    <div class="media-content">
      {{ process.route.name }}
      <process-steps v-if="showSteps" :steps="process.steps"></process-steps>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { ProcessSerializer } from "../api-types";
import ProcessSteps from "./ProcessSteps.vue";

import { makeFlagImgProps } from "../flags";

export default Vue.extend({
  props: {
    process: Object as PropType<ProcessSerializer>,
    showSteps: { type: Boolean, default: true },
  },

  components: { ProcessSteps },

  data() {
    return {
      makeFlagImgProps,
    };
  },
});
</script>
