import Cookies from "js-cookie";

import { showMessages } from "./server-messages";

export default {
  get(url: string, init: any = {}): Promise<Response> {
    return fetch(this.transformUrl(url), init);
  },

  post(url: string, init: any = {}): Promise<Response> {
    const headers = {
      "Content-Type": "application/json",
    } as any;
    const csrf_token = Cookies.get("csrftoken");
    if (csrf_token) {
      headers["X-CSRFToken"] = csrf_token;
    }
    if (init.headers === undefined) {
      init.headers = {};
    }
    Object.assign(init.headers, headers);
    Object.assign(init, { method: "POST" });
    return fetch(this.transformUrl(url), init);
  },

  async fetchDataOrNull(url: string, init: any = {}): Promise<any> {
    const httpResponse = await this.get(url, init);
    if (httpResponse.ok) {
      const response = await httpResponse.json();
      showMessages(response);
      return response.data;
    } else {
      return null;
    }
  },

  // TODO: make vaguely elegant
  async postFetchDataOrNull(url: string, init: any = {}): Promise<any> {
    const httpResponse = await this.post(url, init);
    if (httpResponse.ok) {
      const response = await httpResponse.json();
      showMessages(response);
      return response.data;
    } else {
      return null;
    }
  },

  transformUrl(url: string): string {
    if (!/https?:\/\//.test(url)) {
      url = `${process.env.VUE_APP_SERVER_URL}${url}`;
    }
    return url;
  },
};
