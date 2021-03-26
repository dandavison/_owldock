import Vue from "vue";

export function dismissMobileKeyboardOnDropdownScroll(
  vm: Vue,
  autocompleteRef: string
): void {
  const autocomplete = vm.$refs[autocompleteRef] as any;
  const input = autocomplete?.$refs.input.$refs.input as HTMLElement;
  const dropdown = autocomplete?.$refs.dropdown as HTMLElement;
  const dropdownContent = dropdown?.querySelector(
    ".dropdown-content"
  ) as HTMLElement;
  if (input && dropdownContent) {
    dropdownContent.onscroll = () => {
      // The purpose of this handler is to cause the soft keyboard of
      // mobile devices to be dismissed when the user starts scrolling.

      // On iOS and Safari, a single onscroll event is emitted
      // *after* selecting a dropdown item. Since at that point the
      // dropdown is closed, we do not want this handler to run.
      if (autocomplete.isActive) {
        input.blur();
      }
    };
  }
}
