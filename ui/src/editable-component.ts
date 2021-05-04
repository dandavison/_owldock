/*
  There are several components named Editable*.vue. Each of these implements
  editing and display of some node in the Case document. Each Editable*.vue
  component has two child components: one responsible for display, and one for
  editing, and each has a mini state machine governing which component is
  active. The various Editable*.vue components are thus similar in
  implementation, and some shared aspects of their implementation are provided
  by this module.
*/
import Vue from "vue";
import { BAutocomplete } from "buefy/src/components/autocomplete";
type BAutocompleteType = InstanceType<typeof BAutocomplete>;

export enum State {
  Displaying,
  Selecting,
}

export interface EditingSpec {
  // Should the selector widget be shown at all?
  editable: boolean;
  // Should the selector widget be disabled when shown?
  disabled: boolean;
}

export interface CaseEditingSpec {
  hostCountry: EditingSpec;
  dateRange: EditingSpec;
  applicant?: EditingSpec;
  route?: EditingSpec;
  provider?: EditingSpec;
  steps?: { provider: EditingSpec };
  [index: string]: EditingSpec | { provider: EditingSpec } | undefined;
}

export function defaultEditingSpecFactory(): EditingSpec {
  return {
    editable: false,
    disabled: false,
  };
}

export function defaultCaseEditingSpecFactory(): CaseEditingSpec {
  return {
    applicant: defaultEditingSpecFactory(),
    hostCountry: defaultEditingSpecFactory(),
    dateRange: defaultEditingSpecFactory(),
    route: defaultEditingSpecFactory(),
    provider: defaultEditingSpecFactory(),
    steps: { provider: defaultEditingSpecFactory() },
  };
}

interface EditableComponent extends Vue {
  state: State;
  State: typeof State;
  canUpdate: boolean;
  hasDisplayable: boolean;
}

export class EditableComponentProxy {
  vm: EditableComponent;

  constructor(vm: EditableComponent) {
    this.vm = vm;
  }

  handleDisplayerClick(): void {
    if (this.vm.canUpdate) {
      this.vm.state = State.Selecting;
      // Focus the input element so that the dropdown opens.
      this.vm.$nextTick(() => {
        const selector = this.vm.$refs.selector as Vue;
        if (selector) {
          const autocomplete = selector.$refs.autocomplete as BAutocompleteType;
          const input: HTMLElement = autocomplete.$refs.input.$refs.input;
          input.focus();
        }
      });
    }
  }

  handleSelectorBlur(): void {
    // Hack: Changing state to Displaying will hide the autocomplete input
    // element. However, we need to give it a chance to emit its `select` event,
    // and it does not do this when it is hidden (at least, not on MacOS
    // Chrome). So, we delay the state change to give time for the `select`
    // event to fire. I think that it should be possible to effect this delay
    // using $nextTick, but that didn't work in practice. There is some
    // animation in the buefy autocomplete code that may be relevant.
    const vm = this.vm;
    setTimeout(() => {
      if (vm.hasDisplayable) {
        vm.state = vm.State.Displaying;
      }
    }, 101);
  }
}
