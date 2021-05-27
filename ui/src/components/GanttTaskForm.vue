<template>
  <div>
    <h1 class="title is-5">{{ task.title }}</h1>
    <div class="level">
      <div class="level-left">
        <div class="field">
          <p class="control">
            <b-field label="Depends on">
              <b-select
                @input="handleInput"
                :value="dependsOnIds"
                native-size="10"
                multiple
              >
                <option v-for="t of otherTasks" :key="t.id" :value="t.id">
                  {{ t.title }}
                </option>
              </b-select>
            </b-field>
          </p>
        </div>
      </div>
      <div class="level-right">
        <div class="fieldset">
          <div class="field">
            <p class="control">
              <b-field label="Minimum duration (days)">
                <b-input
                  :value="task.duration[0]"
                  @input="
                    (value) =>
                      eventBus.$emit('update:task-duration', task.id, 0, value)
                  "
                  :class="{ 'has-error': !valid }"
                />
              </b-field>
            </p>
          </div>
          <div class="field">
            <p class="control">
              <b-field label="Maximum duration (days)">
                <b-input
                  :value="task.duration[1]"
                  @input="
                    (value) =>
                      eventBus.$emit('update:task-duration', task.id, 1, value)
                  "
                  :class="{ 'has-error': !valid }"
                />
              </b-field>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { Task } from "./Gantt.vue";

import eventBus from "@/event-bus";

export default Vue.extend({
  props: { task: Object as PropType<Task>, tasks: Array as PropType<Task[]> },

  data() {
    return {
      valid: true,
      eventBus,
      dummy: [],
    };
  },

  computed: {
    otherTasks(): Task[] {
      return this.tasks.filter((t) => t.id !== this.task.id);
    },

    dependsOnIds(): number[] {
      return this.task.dependsOn;
    },
  },

  methods: {
    handleInput(value: string): void {
      eventBus.$emit("update:task-depends-on", this.task.id, value);
    },
  },
});
</script>
