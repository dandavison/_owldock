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
