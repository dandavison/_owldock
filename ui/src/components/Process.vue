<template>
  <div class="media">
    <div class="media-left">
      <figure class="image is-4x3">
        <img v-bind="makeFlagImgProps(case_.process.route.host_country)" />
      </figure>
    </div>

    <div class="media-content">
      <p class="title is-size-6">
        {{ case_.process.route.name }}
      </p>
      <case-steps v-if="showSteps" :steps="case_.steps"></case-steps>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { CaseSerializer } from "../api-types";
import CaseSteps from "./CaseSteps.vue";

import { makeFlagImgProps } from "../flags";

export default Vue.extend({
  props: {
    case_: Object as PropType<CaseSerializer>,
    showSteps: { type: Boolean, default: true },
  },

  components: { CaseSteps },

  data() {
    return {
      makeFlagImgProps,
    };
  },
});
</script>
