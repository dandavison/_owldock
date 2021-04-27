<template>
  <fieldset
    v-if="canUpdate && state === State.Selecting"
    :disabled="editingSpec.disabled"
  >
    <b-datepicker
      :range="true"
      :disabled="editingSpec.disabled"
      :mobile-native="false"
      @input="handleInputDateRange"
    >
    </b-datepicker>
  </fieldset>
  <div v-else @click="handleClick">
    {{ dateRange[0] }} -<br />{{ dateRange[1] }}
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { EditingSpec, State } from "../editable-component";
import { isClientContact } from "@/role";
import eventBus from "@/event-bus";

export default Vue.extend({
  props: {
    dateRange: Array,
    editingSpec: Object as PropType<EditingSpec>,
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

    canUpdate(): boolean {
      return isClientContact() && this.editingSpec.editable;
    },
  },

  methods: {
    handleInputDateRange(dateRange: [Date, Date]): void {
      eventBus.$emit("update:date-range", dateRange);
      this.state = State.Displaying;
    },

    handleClick() {
      if (this.state === State.Displaying) {
        if (this.canUpdate) {
          this.state = State.Selecting;
        }
      }
    },
  },
});
</script>
