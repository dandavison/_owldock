interface ImgProps {
  src: string;
  srcset: string;
  width: string;
  height: string;
  alt: string;
}

export function makeCountryFlagImgProps(countryCode: string): ImgProps {
  let code = countryCode.toLowerCase();
  return {
    src: `https://flagcdn.com/64x48/${code}.png`,
    srcset: `
                  https://flagcdn.com/128x96/${code}.png  2x,
                  https://flagcdn.com/192x144/${code}.png 3x
                `,
    width: "64",
    height: "48",
    alt: code
  };
}
