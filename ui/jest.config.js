module.exports = {
  preset: "@vue/cli-plugin-unit-jest/presets/typescript-and-babel",
  setupFiles: ["./src/__tests__/setup.js"],
  testMatch: ["**/__tests__/*.test.[jt]s"],
};
