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
