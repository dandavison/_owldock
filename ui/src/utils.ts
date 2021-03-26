import { CountrySerializer } from "./api-types";

interface ImgProps {
  src: string;
  srcset: string;
  width: string;
  height: string;
  alt: string;
}

interface DimensionsSeries {
  "1x": string;
  "2x": string;
  "3x": string;
}

interface DimensionsTable {
  "16x12": DimensionsSeries;
  "64x48": DimensionsSeries;
  [index: string]: DimensionsSeries;
}

const dimensionsTable: DimensionsTable = {
  "64x48": {
    "1x": "64x48",
    "2x": "128x96",
    "3x": "192x144"
  },
  "16x12": {
    "1x": "16x12",
    "2x": "32x24",
    "3x": "48x36"
  }
};

// TODO: create use enum for dimensions
export function makeCountryFlagImgProps(
  country: CountrySerializer,
  dimensions: string
): ImgProps {
  const code = country.code.toLowerCase();
  const dimensionSeries =
    dimensionsTable[dimensions] || dimensionsTable["16x12"];
  return {
    src: `https://flagcdn.com/${dimensionSeries["1x"]}/${code}.png`,
    srcset: `
                  https://flagcdn.com/${dimensionSeries["2x"]}/${code}.png  2x,
                  https://flagcdn.com/${dimensionSeries["3x"]}/${code}.png 3x
                `,
    width: "64",
    height: "48",
    alt: country.name
  };
}

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
