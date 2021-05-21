<template>
  <svg v-bind="svgProps" id="gantt"></svg>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import * as d3Array from "d3-array";
import * as d3Axis from "d3-axis";
import * as d3Scale from "d3-scale";
import * as d3Selection from "d3-selection";
const d3 = Object.assign({}, d3Array, d3Axis, d3Scale, d3Selection);

export interface Task {
  time: [number, number];
  title: string;
  text: string;
  progress: number;
}

interface Box {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export default Vue.extend({
  props: { tasks: Array as PropType<Task[]>, width: Number },

  data() {
    return {
      taskRect: { height: 50, gap: 10 },
      margin: { left: 20, top: 10, right: 30, bottom: 30 } as Box,
    };
  },

  watch: {
    tasks: function (): void {
      this.barChart();
    },
  },

  mounted(): void {
    this.barChart();
  },

  methods: {
    barChart(): void {
      if (this.tasks.length === 0) {
        return;
      }
      const [x, y] = [this.x, this.y];
      const svg = d3.select("#gantt");

      // An SVG g container for each row
      const bars = svg
        .selectAll("g")
        .data(this.tasks)
        .join("g")
        .attr(
          "transform",
          (_: Task, i: number) => `translate(0,${y(i as any)})`
        );

      // A rect in each row, representing a step, extending horizontally from
      // start to end time.
      bars
        .append("rect")
        .attr("class", "task-rect")
        .attr("transform", (d: Task) => `translate(${x(d.time[0])},0)`)
        .attr("width", (d: Task) => x(d.time[1]) - x(d.time[0]))
        .attr("height", y.bandwidth() - this.taskRect.gap)
        .attr("rx", 5)
        .attr("ry", 5);

      // Task title inside each rect, upper left
      bars
        .append("text")
        .attr("class", "task-title")
        .attr("transform", (d: Task) => `translate(${x(d.time[0])},0)`)
        .attr("x", 5)
        .attr("y", 0.3 * (y.bandwidth() - this.taskRect.gap))
        .attr("dy", "0.35em")
        .text((d: Task) => d.title);

      // Task text inside each rect, lower left
      bars
        .append("text")
        .attr("class", "task-text")
        .attr("transform", (d: Task) => `translate(${x(d.time[0])},0)`)
        .attr("x", 5)
        .attr("y", 0.7 * (y.bandwidth() - this.taskRect.gap))
        .attr("dy", "0.35em")
        .text((d: Task) => `Day ${d.time[0] + 1} - ${d.time[1]}`);

      // Horizontal time axis at bottom
      svg
        .append("g")
        .call(d3.axisBottom(x))
        .attr(
          "transform",
          `translate(0,${y.range()[1] + this.margin.bottom / 3})`
        );
    },
  },

  computed: {
    x(): d3Scale.ScaleLinear<number, number, never> {
      const margin = this.margin as Box;
      return d3
        .scaleLinear()
        .domain([0, Math.max(...this.tasks.map((d) => d.time[1] || 0))])
        .range([margin.left, this.width - margin.right]);
    },

    y(): d3Scale.ScaleBand<string> {
      const margin = this.margin as Box;
      return d3
        .scaleBand()
        .domain(d3.range(this.tasks.length) as any)
        .range([
          margin.top,
          margin.top + this.taskRect.height * this.tasks.length,
        ]);
    },

    svgProps(): Record<string, number | string> {
      const margin = this.margin as Box;
      return {
        width: this.width,
        height: this.y.range()[1] + margin.bottom,
        "font-family": "sans-serif",
        "font-size": "10",
        "text-anchor": "start",
      };
    },
  },
});
</script>

<style>
.task-rect {
  fill: #f3f3f3;
  stroke: #cccccc;
  stroke-width: 1;
}
.task-title {
  font-weight: bold;
  font-size: 1.3em;
}
.task-progress {
  fill: red;
  stroke: red;
  stroke-width: 1;
}
</style>