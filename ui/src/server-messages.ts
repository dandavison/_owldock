import { NotificationProgrammatic as Notification } from "buefy";

interface JsonResponse {
  data: object | object[];
  messages: string[];
  errors: string[];
}

const A_VERY_LONG_TIME = 1000 * 60 * 60 * 24;

export function showMessages({ messages, errors }: JsonResponse): void {
  for (let message of errors) {
    Notification.open({
      message,
      type: "is-warning",
      hasIcon: true,
      position: "is-top-left",
      duration: A_VERY_LONG_TIME
    });
  }
  for (let message of messages) {
    Notification.open({
      message,
      type: "is-info",
      hasIcon: true,
      position: "is-top-left",
      duration: A_VERY_LONG_TIME
    });
  }
}
