<template>
  <div>
    <div class="media" v-if="haveHostCountry">
      <div class="media-right">
        <figure class="image is-4x3">
          <img v-bind="makeFlagImgProps(process.route.host_country)" />
        </figure>
      </div>
    </div>

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

import { countryIsNull } from "../factories";
import { makeFlagImgProps } from "../flags";

export default Vue.extend({
  props: {
    process: Object as PropType<ProcessSerializer>,
    showRoute: { type: Boolean, default: true },
    showSteps: { type: Boolean, default: true },
  },

  components: { ProcessSteps },

  data() {
    return {
      makeFlagImgProps,
    };
  },

  computed: {
    haveHostCountry(): boolean {
      return !countryIsNull(this.process.route.host_country);
    },
  },
});
</script>
