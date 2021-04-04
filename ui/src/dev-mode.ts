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

function makeFetchWrapper(fetch: any): any {
  async function fetchWrapper(url: string, init: any): Promise<any> {
    const response = await fetch(devModeUrl(url), init);
    if (!response.ok) {
      alert(`
      ${response.status}

      ${init.method || "GET"} ${url}

      Request headers:

      ${JSON.stringify(init.headers)}

      Request body:

      ${JSON.stringify(init.body)}
      `);
    }
    return response;
  }
  return fetchWrapper;
}

window.fetch = makeFetchWrapper(window.fetch);
