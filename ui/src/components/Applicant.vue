<template>
  <div class="media">
    <div class="media-left">
      <figure
        v-for="nationality of applicant.nationalities"
        :key="nationality.code"
        class="image is-4x3"
      >
        <img v-bind="makeFlagImgProps(nationality)" />
      </figure>
    </div>

    <div class="media-content">
      <p class="title is-size-6">
        {{ applicant.user.first_name }}
        {{ applicant.user.last_name }}
      </p>
      <p class="subtitle is-size-6">
        <a :href="`mailto:${applicant.user.email}`" target="#">
          {{ applicant.user.email }}
        </a>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { ApplicantSerializer } from "@/api-types";
import Vue, { PropType } from "vue";

import { makeFlagImgProps } from "../flags";

export default Vue.extend({
  props: { applicant: Object as PropType<ApplicantSerializer> },

  data() {
    return {
      makeFlagImgProps,
    };
  },
});
</script>

<style scoped>
a,
a:hover {
  color: currentColor;
}
</style>