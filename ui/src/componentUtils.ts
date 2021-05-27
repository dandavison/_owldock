import Vue from "vue";
import { BAutocomplete } from "buefy/src/components/autocomplete";

type BAutocompleteType = InstanceType<typeof BAutocomplete>;

export function dismissMobileKeyboardOnDropdownScroll(
  vm: Vue,
  autocompleteRef: string
): void {
  const autocomplete = vm.$refs[autocompleteRef] as BAutocompleteType;
  const input = autocomplete?.$refs.input.$refs.input;
  const dropdown = autocomplete?.$refs.dropdown;
  const dropdownContent = dropdown?.querySelector(".dropdown-content");
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

export async function renderComponentToString(vm: Vue): Promise<string> {
  const el = document.createElement("div");
  vm.$mount(el);
  await vm.$nextTick();
  return vm.$el.innerHTML;
}
