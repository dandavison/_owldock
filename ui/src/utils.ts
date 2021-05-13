export function inputMatchesString(input: string, string: string): boolean {
  return string.toLowerCase().startsWith(input.toLowerCase());
}

/// Convert a timezone-aware Date object to a YYYY-MM-DD format string.
export function dateToYYYYMMDD(date: Date): string {
  // toISOString is going to convert to UTC, so we must change the
  // input aware-time T to a different time T' such that the non-timezone
  // part of the printed representation of UTC(T') is the same as that of T.
  // https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd#comment52948402_29774197
  const offset = date.getTimezoneOffset() * 60 * 1000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
}

export const english = {
  /// Return items formatted as English list with Oxford comma.
  list(items: string[]): string {
    if (items.length > 1) {
      items = [...items];
      const last = items[items.length - 1];
      items[items.length - 1] = `and ${last}`;
    }
    return items.join(", ");
  },
  /// Return English quantified noun.
  /// q(1, "day") === "1 day"
  /// q(2, "day") === "2 days"
  q(quantity: number, singularForm: string, pluralForm?: string): string {
    if (quantity === 1) {
      return `${quantity} ${singularForm}`;
    } else {
      pluralForm = pluralForm ?? `${singularForm}s`;
      return `${quantity} ${pluralForm}`;
    }
  },
};
