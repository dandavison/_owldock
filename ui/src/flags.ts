// https://flagpedia.net/download/api
import { isMobile } from "mobile-device-detect";

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

function makeDimensionString(
  width: number,
  height: number,
  scale: number
): string {
  return `${width * scale}x${height * scale}`;
}

function makeDimensionSeries(width: number, height: number): DimensionsSeries {
  return {
    "1x": makeDimensionString(width, height, 1),
    "2x": makeDimensionString(width, height, 2),
    "3x": makeDimensionString(width, height, 3)
  };
}

// TODO: enforce valid values at compile time using an enum.
function makeWavingFlagImgProps(country: CountrySerializer): ImgProps {
  const code = country.code.toLowerCase();
  if (isMobile) {
    var width = 24;
  } else {
    var width = 64;
  }
  var height = (width * 3) / 4;
  const dimensionSeries = makeDimensionSeries(width, height);
  return {
    src: `https://flagcdn.com/${dimensionSeries["1x"]}/${code}.png`,
    srcset: `
                    https://flagcdn.com/${dimensionSeries["2x"]}/${code}.png  2x,
                    https://flagcdn.com/${dimensionSeries["3x"]}/${code}.png 3x
                  `,
    width: `${width}`,
    height: `${height}`,
    alt: country.name
  };
}

export const makeFlagImgProps = makeWavingFlagImgProps;
