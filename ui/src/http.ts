import Cookies from "js-cookie";

export default {
  async get(url: string, init: any = {}): Promise<Response> {
    return fetch(this.transformUrl(url), init);
  },

  async post(url: string, init: any = {}): Promise<Response> {
    const headers = {
      "Content-Type": "application/json"
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

  transformUrl(url: string): string {
    if (!/https?:\/\//.test(url)) {
      url = `${process.env.VUE_APP_SERVER_URL}${url}`;
    }
    return url;
  }
};
