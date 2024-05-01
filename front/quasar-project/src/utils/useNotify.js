import { Notify } from "quasar";

export function notify(message, type = "negative") {
  Notify.create({
    message,
    type,
    timeout: 650,
  });
}
