<template>
  <div
    v-if="deleted.length === 0 && modified.length === 0 && added.length === 0"
    class="is-warning"
  >
    No changes detected!
  </div>
  <div v-else class="content">
    <div v-if="deleted.length > 0" class="box content">
      <h1 class="title is-5">Deleted steps</h1>
      <ul>
        <li v-for="task of deleted" :key="task.id">
          {{ task.title }}
        </li>
      </ul>
    </div>
    <div v-if="modified.length > 0" class="box content">
      <h1 class="title is-5">Modified steps</h1>
      <ul>
        <li v-for="{ taskA, description } of modified" :key="taskA.id">
          {{ taskA.title }}
          <ul>
            <li v-for="text of description" :key="text">{{ text }}</li>
          </ul>
        </li>
      </ul>
    </div>
    <div v-if="added.length > 0" class="box content">
      <h1 class="title is-5">Added steps</h1>
      <ul>
        <li v-for="task of added" :key="task.id">
          {{ task.title }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { Task } from "./Gantt.vue";

export default Vue.extend({
  props: {
    oldTasks: Array as PropType<Task[]>,
    newTasks: Array as PropType<Task[]>,
  },

  data() {
    return {
      deleted: setMinus(this.oldTasks, this.newTasks),
      added: setMinus(this.newTasks, this.oldTasks),
      modified: taggedSetIntersection(this.oldTasks, this.newTasks)
        .map(([a, b]) => diffObjects(a, b, ["duration", "dependsOn"]))
        .filter(({ description }) => description.length > 0),
    };
  },
});

function setMinus(a: Task[], b: Task[]): Task[] {
  const bkeys = new Set(b.map((t) => t.id));
  const result: Task[] = [];
  for (const ta of a) {
    if (!bkeys.has(ta.id)) {
      result.push(ta);
    }
  }
  return result;
}

function taggedSetIntersection(a: Task[], b: Task[]): [Task, Task][] {
  const k2b = new Map(b.map((t) => [t.id, t]));
  const result: [Task, Task][] = [];
  for (const ta of a) {
    let tb = k2b.get(ta.id);
    if (tb !== undefined) {
      result.push([ta, tb]);
    }
  }
  return result;
}

function diffObjects(
  a: Task,
  b: Task,
  keys: string[]
): { taskA: Task; taskB: Task; description: string[] } {
  const description: string[] = [];
  for (const k of keys) {
    if (JSON.stringify(a[k]) !== JSON.stringify(b[k])) {
      description.push(`${k}: ${a[k]} → ${b[k]}`);
    }
  }
  return { taskA: a, taskB: b, description };
}
</script>

<style scoped></style>
