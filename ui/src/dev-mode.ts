import Cookies from "js-cookie";

export function devModeUrl(url: string): string {
  const username = Cookies.get("username");
  if (username) {
    const urlObj = new URL(url);
    const params = new URLSearchParams(urlObj.search);
    params.set("username", username);
    urlObj.search = params.toString();
    return urlObj.toString();
  } else {
    return url;
  }
}

function makeFetchWrapper(fetch: any) {
  function fetchWrapper(url: string, init: any) {
    return fetch(devModeUrl(url), init);
  }
  return fetchWrapper;
}

window.fetch = makeFetchWrapper(window.fetch) as any;
