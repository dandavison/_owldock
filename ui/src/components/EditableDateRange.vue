<template>
  <b-datepicker
    v-if="dateRangeEditable && state === State.Selecting"
    :range="true"
    :mobile-native="false"
    @input="handleInputDateRange"
  >
  </b-datepicker>
  <div v-else @click="handleClick">{{ dateRange[0] }} - {{ dateRange[1] }}</div>
</template>

<script lang="ts">
import Vue from "vue";

import { isClientContact } from "@/role";
import eventBus from "@/event-bus";

enum State {
  Displaying,
  Selecting,
}

export default Vue.extend({
  props: {
    dateRange: Array,
    dateRangeEditable: Boolean,
  },

  data() {
    return {
      state: State.Selecting,
      State,
    };
  },

  created() {
    if (this.hasDateRange) {
      this.state = State.Displaying;
    }
  },

  computed: {
    hasDateRange(): boolean {
      return Boolean(this.dateRange[0] && this.dateRange[1]);
    },

    canUpdateDateRange(): boolean {
      return isClientContact();
    },
  },

  methods: {
    handleInputDateRange(dateRange: [Date, Date]): void {
      eventBus.$emit("update:date-range", dateRange);
    },

    handleClick() {
      if (this.state === State.Displaying) {
        if (this.canUpdateDateRange) {
          this.state = State.Selecting;
        }
      }
    },
  },
});
</script>
